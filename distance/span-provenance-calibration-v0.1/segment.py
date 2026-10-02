"""Neutral, deterministic structure/sentence segmentation; no semantic inputs."""
import argparse
import hashlib
import json
from pathlib import Path
import re

FIELDS = ('state', 'operation', 'signal', 'inference', 'limit')
VERSION = 'h5-neutral-v1'
LIST = re.compile(r'^(\s*)(?:[-+*]|\d+[.)])\s+')
DELIMITER = re.compile(r'^\s*\|\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|\s*$')
ABBREVIATIONS = frozenset('mr mrs ms dr prof sr jr st vs etc fig eq no approx inc dept'.split())


def canonical_hash(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(',', ':')).encode()).hexdigest()


def trimmed(text, start, end):
    while start < end and text[start].isspace():
        start += 1
    while end > start and text[end - 1].isspace():
        end -= 1
    return start, end


def blocks(text):
    """Identify authored blocks. Ranges are harness-only Python character indices."""
    lines = []
    pos = 0
    for line in text.splitlines(keepends=True):
        lines.append((pos, pos + len(line), line.rstrip('\r\n')))
        pos += len(line)
    result, stack = [], []
    i = 0
    while i < len(lines):
        start, end, line = lines[i]
        if not line.strip():
            i += 1
            continue
        # Only unmistakable pipe tables are interpreted as tables.
        if (line.strip().startswith('|') and line.strip().endswith('|')
                and i + 1 < len(lines) and DELIMITER.fullmatch(lines[i + 1][2])):
            header = len(result)
            result.append({'kind': 'table_header', 'range': trimmed(text, start, end),
                           'delimiter_text': lines[i + 1][2]})
            i += 2
            while i < len(lines) and lines[i][2].strip().startswith('|') and lines[i][2].strip().endswith('|'):
                result.append({'kind': 'table_row', 'range': trimmed(text, *lines[i][:2]),
                               'header_block': header})
                i += 1
            stack = []
            continue
        match = LIST.match(line)
        if match:
            indent = len(match[1].expandtabs(4))
            while stack and stack[-1][0] >= indent:
                stack.pop()
            parent = stack[-1][1] if stack else None
            index = len(result)
            i += 1
            # Indented continuation belongs to the current item, not a new role.
            while i < len(lines):
                continuation = lines[i][2]
                if (not continuation.strip() or LIST.match(continuation)
                        or len(continuation) - len(continuation.lstrip()) <= indent):
                    break
                end = lines[i][1]
                i += 1
            block = {'kind': 'list_item', 'range': trimmed(text, start, end)}
            if parent is not None:
                block['parent_block'] = parent
            result.append(block)
            stack.append((indent, index))
            continue
        stack = []
        i += 1
        while i < len(lines) and lines[i][2].strip() and not LIST.match(lines[i][2]):
            if (lines[i][2].strip().startswith('|') and i + 1 < len(lines)
                    and DELIMITER.fullmatch(lines[i + 1][2])):
                break
            end = lines[i][1]
            i += 1
        result.append({'kind': 'paragraph', 'range': trimmed(text, start, end)})
    return result


def sentence_ranges(text, start, end):
    """Deliberately coarse English splitting; never consult words for semantic roles."""
    ranges, diagnostics = [], []
    cursor = start
    for match in re.finditer(r'[.!?]+(?=\s+\S)', text[start:end]):
        a, b = start + match.start(), start + match.end()
        following = text[b:end].lstrip()
        prefix = text[start:a]
        token = re.search(r'[\w.]+$', prefix)
        word = token[0] if token else ''
        reasons = []
        if not following[0].isupper():
            reasons.append('nonuppercase_next_sentence')
        if len(match[0]) > 1:
            reasons.append('repeated_terminal_punctuation')
        if match[0] == '.' and (word.lower() in ABBREVIATIONS or len(word) == 1 or '.' in word):
            reasons.append('possible_abbreviation_or_initial')
        # Quotes and brackets are structural, not logical-scope parsing.
        if any(prefix.count(left) != prefix.count(right) for left, right in [('(', ')'), ('[', ']'), ('{', '}'), ('“', '”')]):
            reasons.append('open_or_ambiguous_delimiter')
        if prefix.count('"') % 2 or prefix.count('‘') != prefix.count('’'):
            reasons.append('open_or_ambiguous_quote')
        if reasons:
            diagnostics.append({'position': a, 'reasons': reasons})
            continue
        ranges.append(trimmed(text, cursor, b))
        cursor = b
    if cursor < end:
        ranges.append(trimmed(text, cursor, end))
    return ranges, diagnostics


def segment(packet_id, mapping):
    if set(mapping) != set(FIELDS) or not all(isinstance(mapping[f], str) for f in FIELDS):
        raise ValueError('Expected exactly five string-valued source fields')
    spans, ambiguities = {}, []
    for field in FIELDS:
        source = mapping[field]
        block_first = {}
        for index, block in enumerate(blocks(source)):
            start, end = block['range']
            ranges, uncertain = (sentence_ranges(source, start, end) if block['kind'] == 'paragraph'
                                 else ([(start, end)], []))
            ambiguities.extend({'field': field, 'block_index': index, **d} for d in uncertain)
            for sentence_index, (a, b) in enumerate(ranges):
                source_id = f'P{len(spans) + 1:03d}'
                block_first.setdefault(index, source_id)
                span = {'field': field, 'block_index': index, 'sentence_index': sentence_index,
                        'kind': block['kind'], 'text': source[a:b], 'source_range': [a, b]}
                for key in ('parent', 'header'):
                    if key + '_block' in block:
                        span[key + '_id'] = block_first[block[key + '_block']]
                if 'delimiter_text' in block:
                    span['delimiter_text'] = block['delimiter_text']
                spans[source_id] = span
    return {'schema_version': VERSION, 'packet_id': packet_id,
            'mapping_sha256': canonical_hash(mapping), 'spans': spans,
            'ambiguities': ambiguities}


def verify_table(table, mapping):
    if table != segment(table['packet_id'], mapping):
        raise ValueError('INTEGRITY_SPAN_TABLE: table differs from deterministic source derivation')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    args = parser.parse_args()
    value = json.loads(args.source.read_text())
    print(json.dumps(segment(value['case_id'], value['mapping']), indent=2, ensure_ascii=False))
