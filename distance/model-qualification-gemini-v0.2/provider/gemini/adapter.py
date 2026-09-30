"""Native Gemini, one HTTP attempt; authentication never enters artifacts."""
import json
import os
import urllib.error
import urllib.request

MODEL = 'gemini-3.1-pro-preview'
BASE = 'https://generativelanguage.googleapis.com/v1beta'
ROUTE = 'models/' + MODEL + ':generateContent'


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError('Redirect rejected')


def request_body(packet, schema, cfg):
    required = {'requested_model': MODEL, 'endpoint': BASE, 'route': ROUTE,
                'thinking_level': 'high', 'service_tier': 'standard', 'max_output_tokens': 32768, 'temperature': 1.0,
                'tools': [], 'history_messages': 0}
    if any(cfg.get(k) != v for k, v in required.items()):
        raise ValueError('Frozen Gemini configuration/model mismatch')
    return {'serviceTier': 'standard', 'contents': [{'role': 'user', 'parts': [{'text': packet}]}],
            'generationConfig': {'thinkingConfig': {'thinkingLevel': 'high'},
                'temperature': 1.0, 'maxOutputTokens': 32768,
                'responseMimeType': 'application/json', 'responseJsonSchema': schema}}


def request(body, timeout, save, sent):
    key = os.environ.get('GEMINI_API_KEY')
    if not key:
        raise ValueError('Gemini environment credential unavailable')
    req = urllib.request.Request(BASE + '/' + ROUTE,
        data=json.dumps(body, ensure_ascii=False).encode(),
        headers={'x-goog-api-key': key, 'Content-Type': 'application/json'})
    sent()
    try:
        response = urllib.request.build_opener(NoRedirect).open(req, timeout=timeout)
    except urllib.error.HTTPError as exc:
        response = exc
    with response:
        raw = response.read()
        headers = {k: v for k, v in response.headers.items()
                   if k.lower() in ('content-type', 'x-request-id', 'request-id', 'date')}
        meta = json.dumps({'status': response.status, 'headers': headers}).encode()
        if key.encode() in raw or key.encode() in meta:
            save('credential-reflection.json', b'{"body_withheld":true}\n')
            raise ValueError('Provider reflected credential; evidence withheld')
        save('http-body.json', raw)
        save('http-metadata.json', meta)
        if response.status != 200:
            raise ValueError('Gemini HTTP ' + str(response.status))
    return json.loads(raw)


def parse_response(value, session):
    version = value.get('modelVersion')
    if version != MODEL:
        raise ValueError('Missing or mismatched Gemini model identity')
    candidates = value.get('candidates', [])
    if len(candidates) != 1 or candidates[0].get('finishReason') != 'STOP':
        raise ValueError('Incomplete, blocked or multiple Gemini completions')
    candidate = candidates[0]
    if candidate.get('groundingMetadata') or candidate.get('urlContextMetadata'):
        raise ValueError('External context observed')
    parts = candidate.get('content', {}).get('parts', [])
    if not parts or any(set(p) - {'text', 'thought', 'thoughtSignature'} for p in parts):
        raise ValueError('Missing text or tool/non-text output')
    # Thought summaries are not requested and never become experimental judgments.
    text = ''.join(p['text'] for p in parts if not p.get('thought') and isinstance(p.get('text'), str))
    if not text:
        raise ValueError('Missing structured content')
    return text, {'session_id': session, 'requested_model': MODEL,
        'returned_model_identifiers': [version], 'response_id': value.get('responseId'),
        'model_metadata_provenance': [{'value': version, 'source': 'HTTP response.modelVersion'}],
        'verified_served_snapshot': None,
        'snapshot_limitation': 'Preview identifier does not establish immutable served weights',
        'usage': value.get('usageMetadata'), 'harness_retries': 0,
        'internal_retry_observability': 'No internal retry events exposed; hidden retries unobservable'}
