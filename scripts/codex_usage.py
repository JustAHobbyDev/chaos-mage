#!/usr/bin/env python3
"""Read Codex allowance without starting a turn; forecast from matched usage batches."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import selectors
import signal
import subprocess
import sys
import tempfile
import time

APPROVAL_BELOW_REMAINING_PERCENT = 30


class UsageError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise UsageError(message)


def stamp():
    return datetime.now(timezone.utc).isoformat()


def epoch(value):
    date = datetime.fromisoformat(value)
    require(date.tzinfo is not None, 'Timestamp must include a timezone')
    return date.timestamp()


def number(value, minimum=0, maximum=math.inf):
    require(type(value) in (int, float) and math.isfinite(value)
            and minimum <= value <= maximum, 'Invalid numeric value')
    return value


def canonical_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                                     allow_nan=False).encode()).hexdigest()


def read_limits(cli='codex', timeout=30):
    """Allowlisted RPCs only: no thread, turn, reset redemption, or billing writes."""
    with tempfile.TemporaryDirectory(prefix='codex-allowance-') as cwd:
        process = subprocess.Popen([cli, 'app-server', '--stdio'], stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                   cwd=cwd, start_new_session=True)
        selector = selectors.DefaultSelector()
        selector.register(process.stdout, selectors.EVENT_READ)
        pending = bytearray()
        deadline = time.monotonic() + timeout

        def send(message):
            process.stdin.write((json.dumps(message) + '\n').encode())
            process.stdin.flush()

        def receive(request_id):
            while time.monotonic() < deadline:
                while b'\n' in pending:
                    line, _, tail = pending.partition(b'\n')
                    pending[:] = tail
                    message = json.loads(line)
                    if message.get('id') == request_id:
                        require('error' not in message, 'Codex account read failed; check CLI authentication')
                        return message['result']
                require(selector.select(max(0, deadline - time.monotonic())), 'Codex account read timed out')
                chunk = os.read(process.stdout.fileno(), 65536)
                require(chunk, 'Codex app-server closed before the account response')
                pending.extend(chunk)
            raise UsageError('Codex account read timed out')

        try:
            send({'id': 1, 'method': 'initialize', 'params': {
                'clientInfo': {'name': 'chaos_mage_usage_forecast', 'version': '0.1.0'}}})
            receive(1)
            send({'method': 'initialized', 'params': {}})
            send({'id': 2, 'method': 'account/rateLimits/read'})
            return receive(2)
        finally:
            selector.close()
            if process.poll() is None:
                os.killpg(process.pid, signal.SIGTERM)
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait()
            process.stdin.close()
            process.stdout.close()


def normalize(result, scope, captured_at=None):
    require(bool(scope.strip()), 'An account scope label is required')
    buckets = result.get('rateLimitsByLimitId')
    if not buckets:
        single = result.get('rateLimits')
        buckets = {single.get('limitId') or 'codex': single} if single else {}
    windows = []
    for bucket_id, bucket in buckets.items():
        for slot in ('primary', 'secondary'):
            window = bucket.get(slot)
            if window is None:
                continue
            used = number(window['usedPercent'], maximum=100)
            duration = number(window['windowDurationMins'], minimum=1)
            reset = number(window['resetsAt'], minimum=1)
            windows.append({'bucket': bucket_id, 'slot': slot, 'plan_type': bucket.get('planType'),
                            'duration_minutes': duration, 'used_percent': used, 'resets_at': reset})
    resets = result.get('rateLimitResetCredits') or {}
    available = resets.get('availableCount')
    if available is not None:
        require(type(available) is int and available >= 0, 'Invalid reset count')
    # Do not retain reset redemption IDs, identity data, credit balances or auth.
    return {'version': 1, 'captured_at': captured_at or stamp(), 'account_scope': scope,
            'windows': windows, 'available_reset_credits': available,
            'reset_credit_expirations': [c.get('expiresAt') for c in resets.get('credits') or []],
            'source': 'Codex account/rateLimits/read'}


def window_key(snapshot, window):
    return (snapshot['account_scope'], window['bucket'], window['slot'],
            window['duration_minutes'], window['plan_type'])


def sample_rate(sample, current, window, as_of, calibration_age_days=30):
    """Percentage points/session interval; reject resets and censored observations."""
    require(sample.get('isolated_account_work') is True, 'Concurrent/unattributed account work')
    sessions = sample['sessions']
    require(type(sessions) is int and sessions > 0, 'Invalid sample session count')
    before, after = sample['before'], sample['after']
    start, end = epoch(before['captured_at']), epoch(after['captured_at'])
    require(start < end <= as_of, 'Invalid/future sample interval')
    require(as_of - end <= calibration_age_days * 86400, 'Calibration sample too old')
    key = window_key(current, window)
    a = next((w for w in before['windows'] if window_key(before, w) == key), None)
    b = next((w for w in after['windows'] if window_key(after, w) == key), None)
    require(a is not None and b is not None, 'Different account, plan, bucket or window')
    require(a['resets_at'] == b['resets_at'] and end < a['resets_at'], 'Sample crosses a reset')
    u, v = number(a['used_percent'], maximum=100), number(b['used_percent'], maximum=100)
    require(v >= u and v < 100, 'Usage decreased or saturated at 100%; sample is censored')
    # Whole-percentage telemetry may round both endpoints; allow +/- one point
    # of uncertainty in their difference. No artificial precision at zero delta.
    delta = v - u
    return max(0, delta - 1) / sessions, (delta + 1) / sessions, (end - start) / sessions


def predict(plan, snapshot, calibration, reserve_points=10, as_of=None,
            max_snapshot_age_seconds=300, headroom=1.25):
    as_of = time.time() if as_of is None else as_of
    reserve_points = number(reserve_points, maximum=100)
    number(headroom, minimum=1)
    require(calibration['version'] == snapshot['version'] == 1, 'Unsupported usage format')
    require(isinstance(plan['stages'], list) and bool(plan['stages']), 'Missing stages')
    age = as_of - epoch(snapshot['captured_at'])
    global_reasons = []
    if not 0 <= age <= max_snapshot_age_seconds:
        global_reasons.append('Usage snapshot is stale or future-dated; read again')
    if not snapshot['windows']:
        global_reasons.append('No allowance windows returned; cannot assume unlimited usage')
    results, excluded = [], []
    stage_ids = set()
    for stage in plan['stages']:
        require(stage['id'] not in stage_ids, 'Duplicate stage')
        stage_ids.add(stage['id'])
        require(stage['sessions'] is None or type(stage['sessions']) is int and stage['sessions'] >= 0,
                'Invalid session count')
    # Forecast a complete prospective plan. To forecast a remainder, construct an
    # explicitly separate usage-only plan; never shrink the financial gate plan.
    for window in snapshot['windows']:
        used = number(window['used_percent'], maximum=100)
        remaining = 100 - used
        usable = max(0, remaining - reserve_points)
        low, high, seconds, reasons, stages = 0.0, 0.0, 0.0, list(global_reasons), []
        if window['resets_at'] <= as_of:
            reasons.append('Window reset has passed; refresh instead of assuming a full allowance')
        for stage in plan['stages']:
            n = stage['sessions']
            if n == 0:
                continue
            profile = stage.get('usage_profile')
            if n is None or not profile:
                reasons.append('Unknown session count or usage profile: ' + stage['id'])
                continue
            rates = []
            for sample in calibration['samples']:
                if sample.get('usage_profile') != profile:
                    continue
                try:
                    rates.append(sample_rate(sample, snapshot, window, as_of))
                except (UsageError, KeyError, TypeError) as exc:
                    excluded.append({'stage': stage['id'], 'bucket': window['bucket'],
                                     'slot': window['slot'], 'reason': str(exc)})
            if not rates:
                reasons.append('No comparable calibration: ' + stage['id'])
                continue
            per_low = min(r[0] for r in rates)
            per_high = max(r[1] for r in rates) * headroom
            lo, hi = n * per_low, n * per_high
            low += lo
            high += hi
            seconds += n * max(r[2] for r in rates)
            stages.append({'stage': stage['id'], 'sessions': n, 'calibration_batches': len(rates),
                           'predicted_percentage_points': [round(lo, 3), round(hi, 3)],
                           'sessions_fit_if_only_this_profile': math.floor(usable / per_high)
                           if per_high else None})
        risk = ('UNKNOWN' if reasons else 'LOW' if high <= usable else
                'HIGH' if low > usable else 'BORDERLINE')
        results.append({
            'bucket': window['bucket'], 'slot': window['slot'],
            'window_duration_minutes': window['duration_minutes'],
            'used_percent': used, 'remaining_percent': remaining,
            'usable_percentage_points_after_reserve': usable,
            'resets_at': window['resets_at'], 'seconds_until_reset': max(0, window['resets_at'] - as_of),
            'predicted_percentage_points': None if reasons else [round(low, 3), round(high, 3)],
            'percent_of_remaining_allowance': None if reasons or remaining == 0 else
                [round(low / remaining * 100, 2), round(high / remaining * 100, 2)],
            'predicted_remaining_percent': None if reasons else
                [round(max(0, remaining - high), 3), round(max(0, remaining - low), 3)],
            'risk_to_reserve': risk,
            'exhaustion_scenario': 'UNKNOWN' if reasons else 'ABOVE_OBSERVED_RANGE' if high < remaining
                else 'WITHIN_OBSERVED_RANGE' if low < remaining else 'EXPECTED_FROM_ALL_OBSERVED_RATES',
            'estimated_seconds_at_observed_throughput': None if reasons else round(seconds),
            'may_cross_scheduled_reset': None if reasons else as_of + seconds >= window['resets_at'],
            'stages': stages, 'reasons': reasons,
        })
    # Forecast uncertainty is advisory. Approval depends on observed remaining
    # allowance, not predicted consumption or the separate planning reserve.
    refresh_required = bool(global_reasons) or any(w['resets_at'] <= as_of for w in results)
    approval_required = not refresh_required and any(
        w['remaining_percent'] < APPROVAL_BELOW_REMAINING_PERCENT for w in results)
    report = {
        'version': 1, 'forecast_at': datetime.fromtimestamp(as_of, timezone.utc).isoformat(),
        'plan_sha256': canonical_hash(plan), 'snapshot_sha256': canonical_hash(snapshot),
        'calibration_sha256': canonical_hash(calibration), 'reserve_percentage_points': reserve_points,
        'rate_headroom_multiplier': headroom, 'available_reset_credits': snapshot['available_reset_credits'],
        'reset_credit_expirations': snapshot['reset_credit_expirations'],
        'windows': results, 'approval_required': approval_required,
        'approval_below_remaining_percent': APPROVAL_BELOW_REMAINING_PERCENT,
        'refresh_required': refresh_required,
        'global_reasons': global_reasons, 'excluded_samples': excluded,
        'exhaustion_probability': None,
        'interpretation': 'Observed-rate scenarios, not a calibrated probability or guaranteed bound. '
            'No reset is assumed or redeemed; concurrent account work can consume the same allowance.',
    }
    report['report_sha256'] = canonical_hash(report)
    return report


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write('\n')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    p = sub.add_parser('snapshot')
    p.add_argument('--scope', required=True, help='Stable local account label; use a new label if switching accounts')
    p.add_argument('--out', required=True, type=Path)
    p.add_argument('--cli', default='codex')
    p = sub.add_parser('forecast')
    p.add_argument('--plan', required=True, type=Path)
    p.add_argument('--snapshot', required=True, type=Path)
    p.add_argument('--calibration', required=True, type=Path)
    p.add_argument('--reserve-points', type=float, default=None)
    p.add_argument('--out', required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        if args.action == 'snapshot':
            value = normalize(read_limits(args.cli), args.scope)
        else:
            policy = json.loads((Path(__file__).resolve().parents[1] /
                                 'docs/experiment-budget-policy.json').read_text())
            reserve = (args.reserve_points if args.reserve_points is not None else
                       policy['usage_reserve_percentage_points'])
            value = predict(json.loads(args.plan.read_text()), json.loads(args.snapshot.read_text()),
                            json.loads(args.calibration.read_text()), reserve)
        save(args.out, value)
        print(json.dumps(value, indent=2))
        return forecast_exit_code(value)
    except (UsageError, KeyError, TypeError, OSError, ValueError) as exc:
        print('USAGE FORECAST STOP: ' + str(exc), file=sys.stderr)
        return 1


def forecast_exit_code(report):
    """Bad/missing readings need refresh, not an approval override."""
    if report.get('refresh_required'):
        return 1
    return 2 if report.get('approval_required') else 0


if __name__ == '__main__':
    sys.exit(main())
