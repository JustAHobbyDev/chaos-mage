"""Frozen H schemas, exact excerpt checks, and deterministic viability rule."""
import hashlib
import json
from pathlib import Path
import jsonschema

FIELDS = ['state', 'operation', 'signal', 'inference', 'limit']
CLAIM = ['SUPPORTED', 'CONDITIONAL_WARRANT', 'UNSUPPORTED', 'UNCERTAIN']
ARTIFACT = ['KEEP_WITH_WARRANT_FLAGS', 'KEEP_WITH_REDUCED_SCOPE', 'CORE_INVALID', 'UNCERTAIN_LOAD_BEARING']
MECHANISM = ['SURVIVES', 'PARTIALLY_SURVIVES', 'DOES_NOT_SURVIVE', 'UNCERTAIN']
TARGET = ['SUBSTANTIALLY_SURVIVES', 'REDUCED_BUT_MATERIAL', 'NO_MATERIAL_CONTRIBUTION', 'UNCERTAIN']
CASCADE = ['LOCAL', 'BRANCH', 'GLOBAL', 'UNCERTAIN']
REMAINDER = ['DISTINCTIVE_REMAINDER', 'GENERIC_REMAINDER', 'NO_REMAINDER', 'UNCERTAIN']

def require(ok, message):
    if not ok:
        raise ValueError(message)

def unique(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'Duplicate JSON key: ' + key)
        result[key] = value
    return result

def read(path):
    return json.loads(Path(path).read_text(), object_pairs_hook=unique,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))

def digest(data):
    return hashlib.sha256(data).hexdigest()

def sha(path):
    return digest(Path(path).read_bytes())

def obj(properties):
    return {'type': 'object', 'additionalProperties': False,
            'required': list(properties), 'properties': properties}

def arr(items):
    return {'type': 'array', 'items': items}

def enum(values):
    return {'type': 'string', 'enum': values}

T = {'type': 'string', 'minLength': 1, 'pattern': r'\S'}
BOOL = {'type': 'boolean'}
SPAN = obj({'source_field': enum([p + f for p in ['mapping.', 'source.instrument.'] for f in FIELDS]), 'exact_text': T})
SPANS = arr(SPAN)
ANCHOR = obj({'text': T, 'source_spans': SPANS})

def component(values):
    return obj({'status': enum(values), 'rationale': T})

def schema(stage):
    if stage == 'claim-warrant':
        return obj({'claim_id': T, 'status': enum(CLAIM), 'rationale': T,
                    'signal_basis': SPANS, 'stated_empirical_relation': SPANS,
                    'uncertainty': arr(T)})
    require(stage == 'ablation', 'Unknown stage')
    return obj({'artifact_viability': obj({
        'case_id': T, 'unsupported_claim_ids': arr(T),
        'mechanism_survival': component(MECHANISM),
        'target_contribution_survival': component(TARGET),
        'dependency_cascade': obj({'status': enum(CASCADE), 'rationale': T,
            'failed_claims': arr(ANCHOR), 'failed_actions_or_inquiries': arr(ANCHOR),
            'surviving_claims': arr(ANCHOR), 'surviving_actions_or_inquiries': arr(ANCHOR)}),
        'remainder_check': component(REMAINDER),
        'strongest_surviving_target_inference': obj({
            'text': {'anyOf': [T, {'type': 'null'}]}, 'source_spans': SPANS, 'why_warranted': T}),
        'central_bridge': obj({'deleted_claim_is_required_for_all_material_contributions': enum(['yes', 'no', 'uncertain']), 'rationale': T}),
        'per_claim_dependencies': arr(obj({'claim_id': T, 'dependent_claims': arr(ANCHOR),
            'dependent_actions_or_inquiries': arr(ANCHOR), 'rationale': T})),
        'structural_conflict': obj({'present': BOOL, 'resolved': BOOL, 'explanation': T}),
        'artifact_status': enum(ARTIFACT), 'rationale': T})})

def derive(mechanism, target, conflict=None):
    require(mechanism in MECHANISM and target in TARGET, 'Unknown decisive dimension')
    if mechanism == 'DOES_NOT_SURVIVE' or target == 'NO_MATERIAL_CONTRIBUTION':
        result = 'CORE_INVALID'
    elif mechanism == 'UNCERTAIN' or target == 'UNCERTAIN':
        result = 'UNCERTAIN_LOAD_BEARING'
    elif target == 'SUBSTANTIALLY_SURVIVES' and mechanism == 'SURVIVES':
        result = 'KEEP_WITH_WARRANT_FLAGS'
    else:
        result = 'KEEP_WITH_REDUCED_SCOPE'
    if conflict and conflict['present'] and not conflict['resolved']:
        result = 'UNCERTAIN_LOAD_BEARING'
    return result

def cited_spans(spans, candidate, deleted=(), surviving=False, mapping_only=False):
    proofs = []
    for span in spans:
        field = span['source_field']
        if mapping_only:
            require(field.startswith('mapping.'), 'Citation must reference mapping')
        text = candidate
        for key in field.split('.'):
            text = text[key]
        quote = span['exact_text']
        locations = []
        cursor = 0
        while True:
            start = text.find(quote, cursor)
            if start < 0:
                break
            end = start + len(quote)
            if not surviving or not any(a['source_field'] == field and start < a['span_end'] and end > a['span_start'] for a in deleted):
                locations.append({'start': start, 'end': end})
            cursor = start + 1
        require(bool(locations), 'Missing exact/surviving excerpt: ' + field)
        proofs.append({'source_field': field, 'sha256': digest(quote.encode()), 'locations': locations})
    return proofs

def validate(value, stage, identity, candidate, unsupported=()):
    jsonschema.Draft202012Validator(schema(stage)).validate(value)
    if stage == 'claim-warrant':
        require(value['claim_id'] == identity, 'Wrong claim identity')
        require(bool(value['signal_basis']), 'Missing signal citation')
        cited_spans(value['signal_basis'], candidate)
        conditional = value['status'] == 'CONDITIONAL_WARRANT'
        require(conditional == bool(value['stated_empirical_relation']), 'Conditional relation coverage')
        cited_spans(value['stated_empirical_relation'], candidate, mapping_only=True)
        require(value['status'] != 'UNCERTAIN' or bool(value['uncertainty']), 'Missing uncertainty explanation')
        return
