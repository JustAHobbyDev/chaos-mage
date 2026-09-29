"""Direct Meta API adapter; one HTTP request, no SDK retries or agent tools."""
import json
import os
import urllib.error
import urllib.request

MODEL = 'muse-spark-1.3-contributor'
BASE = 'https://api.meta.ai/v1'


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError('Redirect rejected; credentials never forwarded')


def request_body(packet, schema, cfg):
    if cfg['requested_model'] != MODEL or cfg['endpoint'] != BASE:
        raise ValueError('Muse model/endpoint fallback rejected')
    return {'model': MODEL, 'messages': [{'role': 'user', 'content': packet}],
            'reasoning_effort': cfg['reasoning_effort'],
            'response_format': {'type': 'json_schema', 'json_schema': {
                'name': 'judgment', 'strict': True, 'schema': schema}}}


def request(route, body, timeout, save):
    if route not in ('models', 'chat/completions'):
        raise ValueError('Unapproved API route')
    key = os.environ['META_API_KEY']
    data = None if body is None else json.dumps(body, ensure_ascii=False).encode()
    req = urllib.request.Request(BASE + '/' + route, data=data, headers={
        'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'})
    try:
        response = urllib.request.build_opener(NoRedirect).open(req, timeout=timeout)
    except urllib.error.HTTPError as exc:
        response = exc
    with response:
        raw = response.read()
        # Never publish a reflected credential, even on a provider error.
        if key.encode() in raw:
            save('credential-reflection.json', b'{"body_withheld":true}\n')
            raise ValueError('Provider reflected credential; response withheld')
        save('http-body.json', raw)
        headers = {k: v for k, v in response.headers.items()
                   if k.lower() in ('content-type', 'x-request-id', 'request-id', 'date')}
        save('http-metadata.json', json.dumps({'status': response.status, 'headers': headers}).encode())
        if response.status != 200:
            raise ValueError('Meta HTTP ' + str(response.status))
    return json.loads(raw)


def parse_response(value, session):
    if value.get('model') != MODEL:
        raise ValueError('Muse model fallback or missing returned identifier')
    choices = value.get('choices', [])
    if len(choices) != 1 or choices[0].get('finish_reason') != 'stop':
        raise ValueError('Incomplete or multiple completions')
    msg = choices[0]['message']
    if msg.get('tool_calls') or msg.get('function_call') or msg.get('refusal'):
        raise ValueError('Tool activity or refusal')
    if not isinstance(msg.get('content'), str):
        raise ValueError('Missing structured content')
    return msg['content'], {
        'session_id': session, 'requested_model': MODEL,
        'returned_model_identifiers': [value['model']],
        'model_metadata_provenance': [{'value': value['model'], 'source': 'HTTP response.model'}],
        'response_id': value.get('id'), 'created': value.get('created'),
        'system_fingerprint': value.get('system_fingerprint'), 'usage': value.get('usage'),
        'verified_served_snapshot': None, 'tier': 'Contributor',
        'formatting_retries': {'observed_formatting_retries': 0,
            'observability': 'One HTTP response; hidden provider retries unobservable'},
        'internal_transport_retry_events': [], 'harness_retries': 0}
