"""Conservative pre-send reservations and descriptive usage estimates."""
from decimal import Decimal
import json


def estimate(prompt, output, pricing):
    long = prompt > pricing['long_context_above_tokens']
    ip = pricing['long_context_input_per_million' if long else 'input_per_million']
    op = pricing['long_context_output_per_million' if long else 'output_including_thinking_per_million']
    return (Decimal(prompt) * Decimal(ip) + Decimal(output) * Decimal(op)) / Decimal(1000000)


def reserve(body, pricing):
    prompt = len(json.dumps(body, ensure_ascii=False).encode()) + 4096
    return {'input_token_upper_estimate': prompt, 'output_token_cap': 32768,
            'reserved_usd': str(estimate(prompt, 32768, pricing))}


def account(usage, pricing):
    if not isinstance(usage, dict):
        raise ValueError('Missing usage metadata')
    required = ['promptTokenCount', 'candidatesTokenCount', 'thoughtsTokenCount', 'totalTokenCount']
    if any(type(usage.get(k)) is not int or usage[k] < 0 for k in required):
        raise ValueError('Missing or invalid token usage')
    p, c, t, total = (usage[k] for k in required)
    if p + c + t != total or usage.get('toolUsePromptTokenCount', 0):
        raise ValueError('Ambiguous usage accounting or tool use')
    if usage.get('serviceTier') not in (None, 'standard'):
        raise ValueError('Unexpected billing service tier')
    return {'input_tokens': p, 'output_tokens': c, 'thinking_tokens': t,
            'billable_output_tokens': c + t, 'total_tokens': total,
            'estimated_usd': str(estimate(p, c + t, pricing)),
            'billable_interpretation': 'prompt at full input rate; candidates + thoughts at output rate',
            'estimate_not_invoice': True}
