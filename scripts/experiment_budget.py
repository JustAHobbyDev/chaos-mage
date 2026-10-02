#!/usr/bin/env python3
"""Offline forecasts and a durable, per-session approval gate. No provider SDKs."""
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
    """Missing prices or unknown downstream fan-out require review, never mean zero."""
    name(plan['experiment_id'])
    name(plan['description'])
    name(plan['execution_fingerprint'])
    require(plan['version'] == 1 and policy['version'] == 1, 'Unsupported format version')
    require(type(plan.get('execution_allowed', False)) is bool, 'execution_allowed must be boolean')
    require(isinstance(plan['stages'], list) and bool(plan['stages']), 'Stages are required')
    threshold = dollars(policy['approval_above_usd'])
    session_threshold = count(policy['approval_above_sessions'])
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
        'approval_required': bool(reasons), 'reasons': reasons,
        'billing_limitation': 'Forecast only. Codex sessions are not billable API request counts. '
            'This gate cannot observe subscription credits, top-ups, internal retries, or actual charges.',
    }


class Gate:
    """Every worker reserves before launching. SQLite serializes concurrent workers."""
    def __init__(self, ledger=DEFAULT_LEDGER):
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

    def status_in(self, db, plan, policy):
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
        reasons = [] if approval else list(report['reasons'])
        if block:
            reasons.append('Experiment blocked: ' + block['reason'])
        for sid, used in consumed.items():
            if sid not in stages or stages[sid]['sessions'] is None or used > stages[sid]['sessions']:
                reasons.append('Plan omits or shrinks previously reserved work: ' + sid)
        # Measured overruns invalidate even an existing approval for the forecast.
        # Unknown observations retain the original forecast; they are never treated as free.
        for sid, stage in stages.items():
            cost = stage['estimated_cost_usd']
            if cost is None or not stage['sessions']:
                continue
            expected = dollars(cost) / stage['sessions']
            if any(r['observed_cost'] is not None and dollars(r['observed_cost']) > expected
                   for r in rows if r['stage'] == sid):
                reasons.append('Observed cost exceeds stage forecast; revise plan: ' + sid)
        return {**report, 'reserved_sessions': len(rows), 'reserved_by_stage': consumed,
                'approval_reference': approval['reference'] if approval else None,
                'allowed': not reasons, 'blocking_reasons': reasons}

    def status(self, plan, policy):
        with self.transaction() as db:
            return self.status_in(db, plan, policy)

    def reserve(self, plan, policy, stage, session, command):
        name(session)
        require(bool(command) and all(isinstance(s, str) for s in command), 'Command argv is required')
        error = None
        with self.transaction() as db:
            status = self.status_in(db, plan, policy)
            experiment = plan['experiment_id']
            stages = {s['id']: s for s in plan['stages']}
            if not plan.get('execution_allowed', False):
                error = 'Forecast-only plan; execution is not authorized by this plan'
            elif not status['allowed']:
                error = '; '.join(status['blocking_reasons'])
            elif stage not in stages:
                error = 'Undeclared stage'
            elif stages[stage]['sessions'] is None:
                error = 'Resolve this stage session count and obtain any new approval before dispatch'
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
                                                      'plan_sha256': status['plan_sha256']})
        if error:
            raise BudgetError('APPROVAL GATE: ' + error)

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
        gate = Gate(args.ledger)
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
            return 0 if report['allowed'] else 2
        if args.action == 'approve':
            require(sys.stdin.isatty(), 'Approval requires an interactive operator terminal; no piped auto-approval')
            phrase = 'approve ' + report['plan_sha256']
            print('Approve only after reviewing the complete forecast above.\nType: ' + phrase, file=sys.stderr)
            require(input().strip() == phrase, 'Approval canceled')
            gate.approve(plan, policy, args.reference)
            return 0
        command = args.command[1:] if args.command[:1] == ['--'] else args.command
        return launch(gate, plan, policy, args.stage, args.session, command)
    except (BudgetError, KeyError, TypeError, OSError, sqlite3.Error, json.JSONDecodeError) as exc:
        print('BUDGET GATE STOP: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
