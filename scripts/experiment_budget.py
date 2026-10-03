#!/usr/bin/env python3
"""Cumulative forecasts and reservations; approval only below 30% allowance."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import hashlib
import json
from pathlib import Path
import sqlite3
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_POLICY = ROOT / 'docs/experiment-budget-policy.json'
DEFAULT_LEDGER = ROOT / '.runtime/experiment-budget.sqlite3'


class BudgetError(ValueError):
    pass


class ApprovalRequired(BudgetError):
    pass


def require(condition, message):
    if not condition:
        raise BudgetError(message)


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                                     allow_nan=False).encode()).hexdigest()


def dollars(value):
    try:
        number = Decimal(str(value))
    except InvalidOperation as exc:
        raise BudgetError('Invalid dollar amount') from exc
    require(number.is_finite() and number >= 0, 'Dollar amounts must be finite and nonnegative')
    return number


def count(value):
    require(type(value) is int and value >= 0, 'Session counts must be nonnegative integers')
    return value


def name(value):
    require(isinstance(value, str) and bool(value.strip()), 'A nonempty identifier is required')
    return value


def forecast(plan, policy):
    """Costs and workload remain visible advisories, never zero estimates."""
    name(plan['experiment_id'])
    name(plan['description'])
    name(plan['execution_fingerprint'])
    require(plan['version'] == 1 and policy['version'] == 1, 'Unsupported format version')
    require(type(plan.get('execution_allowed', False)) is bool, 'execution_allowed must be boolean')
    require(isinstance(plan['stages'], list) and bool(plan['stages']), 'Stages are required')
    threshold = dollars(policy.get('cost_advisory_above_usd', policy.get('approval_above_usd', '10')))
    session_threshold = count(policy.get('session_advisory_above', policy.get('approval_above_sessions', 100)))
    seen, sessions, costs, unknown_counts, unknown_costs = set(), 0, Decimal(0), [], []
    rows = []
    for stage in plan['stages']:
        sid = name(stage['id'])
        require(sid not in seen, 'Duplicate stage: ' + sid)
        seen.add(sid)
        n, cost = stage['sessions'], stage['estimated_cost_usd']
        if n is None:
            unknown_counts.append(sid)
        else:
            sessions += count(n)
        if cost is None:
            unknown_costs.append(sid)
        else:
            name(stage['estimate_basis'])
            costs += dollars(cost)
        rows.append({'stage': sid, 'sessions': n, 'estimated_cost_usd': cost})
    reasons = []
    if unknown_counts:
        reasons.append('Unknown session count: ' + ', '.join(unknown_counts))
    if unknown_costs:
        reasons.append('Unknown cost: ' + ', '.join(unknown_costs))
    if costs > threshold:
        reasons.append(f'Forecast exceeds ${threshold}')
    if sessions > session_threshold:
        reasons.append(f'Forecast exceeds {session_threshold} sessions')
    return {
        'experiment_id': plan['experiment_id'], 'plan_sha256': digest(plan),
        'policy_sha256': digest(policy), 'stages': rows,
        'known_sessions': sessions, 'session_count_complete': not unknown_counts,
        'known_estimated_cost_usd': str(costs), 'cost_estimate_complete': not unknown_costs,
        'approval_required': False, 'reasons': [], 'advisories': reasons,
        'billing_limitation': 'Forecast only. Codex sessions are not billable API request counts. '
            'This gate cannot observe subscription credits, top-ups, internal retries, or actual charges.',
    }


def current_allowance():
    import codex_usage as usage
    return usage.normalize(usage.read_limits(), 'local-codex-account')


def allowance_status(snapshot):
    # Reuse the same freshness and strict <30% predicate as the usage CLI.
    # Zero work here is only a way to isolate the allowance predicate; no
    # cost or consumption prediction from this call is exposed as a forecast.
    import codex_usage as usage
    report = usage.predict({'stages': [{'id': 'allowance-check', 'sessions': 0}]},
                           snapshot, {'version': 1, 'samples': []})
    return {'approval_required': report['approval_required'],
            'refresh_required': report['refresh_required'],
            'approval_below_remaining_percent': report['approval_below_remaining_percent'],
            'snapshot_sha256': report['snapshot_sha256'],
            'captured_at': snapshot['captured_at'],
            'windows': [{k: w[k] for k in ('bucket', 'slot', 'remaining_percent', 'resets_at')}
                        for w in report['windows']]}


class Gate:
    """Every worker reserves before launching. SQLite serializes concurrent workers."""
    def __init__(self, ledger=DEFAULT_LEDGER, usage_reader=None):
        self.usage_reader = usage_reader or current_allowance
        self.path = Path(ledger)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as db:
            db.executescript('''
                CREATE TABLE IF NOT EXISTS approvals (
                    experiment TEXT, plan_hash TEXT, policy_hash TEXT,
                    reference TEXT NOT NULL, at TEXT NOT NULL,
                    PRIMARY KEY(experiment, plan_hash, policy_hash));
                CREATE TABLE IF NOT EXISTS reservations (
                    experiment TEXT, session TEXT, stage TEXT NOT NULL,
                    plan_hash TEXT NOT NULL, at TEXT NOT NULL,
                    command_json TEXT NOT NULL, state TEXT NOT NULL,
                    observed_cost TEXT, returncode INTEGER,
                    PRIMARY KEY(experiment, session));
                CREATE TABLE IF NOT EXISTS blocks (
                    experiment TEXT PRIMARY KEY, reason TEXT NOT NULL, at TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS audit (
                    sequence INTEGER PRIMARY KEY, at TEXT NOT NULL, event TEXT NOT NULL,
                    experiment TEXT NOT NULL, details TEXT NOT NULL);
            ''')

    @contextmanager
    def connect(self):
        db = sqlite3.connect(self.path, timeout=30, isolation_level=None)
        db.row_factory = sqlite3.Row
        try:
            yield db
        finally:
            db.close()

    @contextmanager
    def transaction(self):
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            try:
                yield db
                db.execute('COMMIT')
            except BaseException:
                db.execute('ROLLBACK')
                raise

    def audit(self, db, event, experiment, details):
        db.execute('INSERT INTO audit(at,event,experiment,details) VALUES (?,?,?,?)',
                   (now(), event, experiment, json.dumps(details, sort_keys=True)))

    def approve(self, plan, policy, reference):
        """Record actual user authorization; callers must never manufacture consent."""
        report = forecast(plan, policy)
        name(reference)
        with self.transaction() as db:
            db.execute('INSERT INTO approvals VALUES (?,?,?,?,?)',
                       (plan['experiment_id'], report['plan_sha256'], report['policy_sha256'], reference, now()))
            self.audit(db, 'APPROVAL', plan['experiment_id'], {**report, 'reference': reference})
        return report

    def status_in(self, db, plan, policy, allowance):
        report = forecast(plan, policy)
        experiment = plan['experiment_id']
        rows = db.execute('SELECT * FROM reservations WHERE experiment=?', (experiment,)).fetchall()
        approval = db.execute('SELECT reference FROM approvals WHERE experiment=? AND plan_hash=? AND policy_hash=?',
                             (experiment, report['plan_sha256'], report['policy_sha256'])).fetchone()
        block = db.execute('SELECT reason FROM blocks WHERE experiment=?', (experiment,)).fetchone()
        consumed = {}
        for row in rows:
            consumed[row['stage']] = consumed.get(row['stage'], 0) + 1
        stages = {s['id']: s for s in plan['stages']}
        reasons = []
        if allowance['refresh_required']:
            reasons.append('Refresh account allowance; missing/stale/reset-crossed readings cannot be approved away')
        elif allowance['approval_required'] and not approval:
            reasons.append('Approval required: remaining usage is below 30%')
        advisories = list(report['advisories'])
        if block:
            reasons.append('Experiment blocked: ' + block['reason'])
        for sid, used in consumed.items():
            if sid not in stages or stages[sid]['sessions'] is None or used > stages[sid]['sessions']:
                reasons.append('Plan omits or shrinks previously reserved work: ' + sid)
        # Observed overruns require reforecasting, not a separate approval trigger.
        for sid, stage in stages.items():
            cost = stage['estimated_cost_usd']
            if cost is None or not stage['sessions']:
                continue
            expected = dollars(cost) / stage['sessions']
            if any(r['observed_cost'] is not None and dollars(r['observed_cost']) > expected
                   for r in rows if r['stage'] == sid):
                advisories.append('Observed cost exceeds stage forecast; revise plan: ' + sid)
        return {**report, 'approval_required': allowance['approval_required'],
                'refresh_required': allowance['refresh_required'], 'usage_gate': allowance,
                'advisories': advisories, 'reserved_sessions': len(rows), 'reserved_by_stage': consumed,
                'approval_reference': approval['reference'] if approval else None,
                'allowed': not reasons, 'blocking_reasons': reasons}

    def status(self, plan, policy):
        allowance = allowance_status(self.usage_reader())
        with self.transaction() as db:
            return self.status_in(db, plan, policy, allowance)

    def reserve(self, plan, policy, stage, session, command):
        name(session)
        require(bool(command) and all(isinstance(s, str) for s in command), 'Command argv is required')
        error = None
        allowance = allowance_status(self.usage_reader())
        with self.transaction() as db:
            status = self.status_in(db, plan, policy, allowance)
            experiment = plan['experiment_id']
            stages = {s['id']: s for s in plan['stages']}
            if not plan.get('execution_allowed', False):
                error = 'Forecast-only plan; execution is not authorized by this plan'
            elif not status['allowed']:
                error = '; '.join(status['blocking_reasons'])
            elif stage not in stages:
                error = 'Undeclared stage'
            elif stages[stage]['sessions'] is None:
                error = 'Resolve this stage session count in the cumulative plan before dispatch'
            elif status['reserved_by_stage'].get(stage, 0) >= stages[stage]['sessions']:
                error = 'Stage session limit reached; revise the cumulative plan before more work'
            elif db.execute('SELECT 1 FROM reservations WHERE experiment=? AND session=?',
                            (experiment, session)).fetchone():
                error = 'Session already reserved; no automatic retry'
            if error:
                self.audit(db, 'DENIED', experiment, {'stage': stage, 'session': session, 'reason': error})
            else:
                db.execute('INSERT INTO reservations VALUES (?,?,?,?,?,?,?,?,?)',
                           (experiment, session, stage, status['plan_sha256'], now(),
                            json.dumps(command), 'RESERVED', None, None))
                self.audit(db, 'RESERVED', experiment, {'stage': stage, 'session': session,
                                                      'plan_sha256': status['plan_sha256'],
                                                      'usage_gate': allowance})
        if error:
            if error == 'Approval required: remaining usage is below 30%':
                raise ApprovalRequired(error)
            raise BudgetError('EXECUTION GATE: ' + error)

    def finish(self, experiment, session, returncode):
        with self.transaction() as db:
            result = db.execute("UPDATE reservations SET state='FINISHED', returncode=? "
                                "WHERE experiment=? AND session=? AND state='RESERVED'",
                                (returncode, experiment, session))
            require(result.rowcount == 1, 'Missing or already finished reservation')
            self.audit(db, 'FINISHED', experiment, {'session': session, 'returncode': returncode})

    def observe_cost(self, experiment, session, cost):
        cost = str(dollars(cost))
        with self.transaction() as db:
            row = db.execute('SELECT observed_cost FROM reservations WHERE experiment=? AND session=?',
                             (experiment, session)).fetchone()
            require(row is not None, 'Unknown reservation')
            require(row['observed_cost'] is None or dollars(cost) >= dollars(row['observed_cost']),
                    'Observed cost cannot decrease')
            db.execute('UPDATE reservations SET observed_cost=? WHERE experiment=? AND session=?',
                       (cost, experiment, session))
            self.audit(db, 'OBSERVED_COST', experiment, {'session': session, 'cost_usd': cost})

    def block(self, experiment, reason):
        name(experiment)
        name(reason)
        with self.transaction() as db:
            db.execute('INSERT INTO blocks VALUES (?,?,?)', (experiment, reason, now()))
            self.audit(db, 'BLOCKED', experiment, {'reason': reason})


def launch(gate, plan, policy, stage, session, command):
    # Reserve BEFORE creating a subprocess. Failure/crash consumes the reservation.
    gate.reserve(plan, policy, stage, session, command)
    process = subprocess.run(command, check=False)
    gate.finish(plan['experiment_id'], session, process.returncode)
    return process.returncode


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--policy', type=Path, default=DEFAULT_POLICY)
    parser.add_argument('--ledger', type=Path, default=DEFAULT_LEDGER)
    parser.add_argument('--usage-snapshot', type=Path, help='Fresh normalized account snapshot; otherwise read live allowance')
    sub = parser.add_subparsers(dest='action', required=True)
    for action in ('check', 'approve', 'launch'):
        p = sub.add_parser(action)
        p.add_argument('--plan', required=True, type=Path)
        if action == 'approve':
            p.add_argument('--reference', required=True, help='Where the user granted this exact approval')
        if action == 'launch':
            p.add_argument('--stage', required=True)
            p.add_argument('--session', required=True)
            p.add_argument('command', nargs=argparse.REMAINDER)
    p = sub.add_parser('observe-cost')
    p.add_argument('--experiment', required=True)
    p.add_argument('--session', required=True)
    p.add_argument('--usd', required=True)
    p = sub.add_parser('block')
    p.add_argument('--experiment', required=True)
    p.add_argument('--reason', required=True)
    args = parser.parse_args(argv)
    try:
        reader = (lambda: json.loads(args.usage_snapshot.read_text())) if args.usage_snapshot else None
        gate = Gate(args.ledger, usage_reader=reader)
        if args.action == 'block':
            gate.block(args.experiment, args.reason)
            return 0
        if args.action == 'observe-cost':
            gate.observe_cost(args.experiment, args.session, args.usd)
            return 0
        plan = json.loads(args.plan.read_text())
        policy = json.loads(args.policy.read_text())
        report = gate.status(plan, policy)
        print(json.dumps(report, indent=2), file=sys.stderr, flush=True)
        if args.action == 'check':
            return 0 if report['allowed'] else (2 if report['blocking_reasons'] ==
                ['Approval required: remaining usage is below 30%'] else 1)
        if report['refresh_required']:
            return 1
        if args.action == 'approve':
            require(sys.stdin.isatty(), 'Approval requires an interactive operator terminal; no piped auto-approval')
            phrase = 'approve ' + report['plan_sha256']
            print('Approve only after reviewing the complete forecast above.\nType: ' + phrase, file=sys.stderr)
            require(input().strip() == phrase, 'Approval canceled')
            gate.approve(plan, policy, args.reference)
            return 0
        command = args.command[1:] if args.command[:1] == ['--'] else args.command
        return launch(gate, plan, policy, args.stage, args.session, command)
    except ApprovalRequired as exc:
        print('APPROVAL REQUIRED: ' + str(exc), file=sys.stderr)
        return 2
    except (BudgetError, KeyError, TypeError, OSError, sqlite3.Error, ValueError) as exc:
        print('BUDGET GATE STOP: ' + str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
