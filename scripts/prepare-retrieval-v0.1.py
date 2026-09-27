#!/usr/bin/env python3
"""Offline preparation/verification. Never opens the target answer key."""
import argparse
from datetime import datetime, timezone
import hashlib
import hmac
import platform
import random
import secrets
import subprocess

import yaml

from retrieval_v01 import (ROOT, BENCH, PRIVATE, CORPUS, BENCHMARK, PROTOCOL,
                           FIELDS, INSTRUCTION, read_yaml, parse_yaml, require,
                           sha, yaml_bytes, write_new, validate_candidates, validate_packet)

VERSION = "0.1.0"


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args])


def frozen_inputs():
    paths = git("ls-tree", "-r", "--name-only", CORPUS, "instruments/").decode().splitlines()
    accepted = []
    for path in sorted(paths):
        if path.endswith(".yaml"):
            record = parse_yaml(git("show", f"{CORPUS}:{path}"))
            if record["extraction"]["status"] == "accepted":
                require(set(record["instrument"]) == set(FIELDS), "Frozen schema differs; stop")
                accepted.append((path, record))
    require(len(accepted) == 14, "Eligible candidate count is not 14; stop")
    manifest_path = "benchmark/retrieval-v0.1/manifest.yaml"
    manifest_bytes = git("show", f"{BENCHMARK}:{manifest_path}")
    require((ROOT / manifest_path).read_bytes() == manifest_bytes, "Target manifest differs; stop")
    targets = []
    for item in parse_yaml(manifest_bytes)["targets"]:
        path = "benchmark/retrieval-v0.1/" + item["file"]
        raw = git("show", f"{BENCHMARK}:{path}")
        require((ROOT / path).read_bytes() == raw, "Committed target differs; stop")
        _, front, narrative = raw.decode("utf-8").split("---", 2)
        meta = parse_yaml(front)
        require(meta == {"target_id": item["id"], "target_domain": item["domain"],
                         "status": "frozen"}, "Target metadata differs; stop")
        targets.append({"target_id": item["id"], "target_domain": item["domain"],
                        "target": narrative.strip()})
    require({t["target_id"] for t in targets} == {f"TARGET-{n:02}" for n in range(1, 11)}
            and len(targets) == 10, "Target set differs; stop")
    return accepted, sorted(targets, key=lambda t: t["target_id"])


def shuffled(items, seed, label):
    # Separate PRNG state per label; never reuse one packet's permutation as input.
    derived = hmac.new(bytes.fromhex(seed), label.encode(), hashlib.sha256).digest()
    result = list(items)
    random.Random(int.from_bytes(derived, "big")).shuffle(result)
    return result


def representations(accepted, seed):
    key, schema, baseline = {}, [], []
    for index, (path, record) in enumerate(shuffled(accepted, seed, "candidate-ids"), 1):
        cid = f"CAND-{index:02}"
        extraction = record["extraction"]
        key[cid] = {"extraction_id": extraction["id"], "name": extraction["name"],
                    "practice": extraction["practice"], "frozen_file": path}
        schema.append({"id": cid, "instrument": record["instrument"]})
        baseline.append({"id": cid, "name": extraction["name"], "practice": extraction["practice"]})
    return {"version": "0.1", "candidates": key}, {"schema": schema, "baseline": baseline}


def packets(targets, arms, seed):
    """Only public targets, arm representations, and ordering seed enter this builder."""
    result = {}
    for target in targets:
        for arm in ("baseline", "schema"):
            for run in (1, 2, 3):
                path = f"{arm}/{target['target_id']}-run-{run}.yaml"
                packet = {"experiment": "retrieval-v0.1", "arm": arm,
                          "target_id": target["target_id"], "run": run,
                          "target_domain": target["target_domain"], "target": target["target"],
                          "candidates": shuffled(arms[arm], seed, "packet:" + path),
                          "instruction": INSTRUCTION}
                validate_packet(packet)
                result[path] = packet
    return result


def integrity(path):
    return {"path": str(path.relative_to(ROOT)), "sha256": sha(path.read_bytes())}


def prepare():
    accepted, targets = frozen_inputs()  # Stop on eligibility error before any writes.
    outputs = [BENCH / "candidates", BENCH / "retrieval-packets",
               BENCH / "execution-manifest.yaml", PRIVATE / "candidate-key.yaml",
               PRIVATE / "retrieval-seed.yaml"]
    require(not any(path.exists() for path in outputs), "Preparation exists; use --verify, never regenerate")
    require(not any((PRIVATE / "results").rglob("*.*")), "Results already exist; cannot prepare")
    PRIVATE.mkdir(parents=True, exist_ok=True)
    seed = secrets.token_hex(32)
    seed_record = {"version": "0.1", "randomization_seed": seed,
                   "generator": "scripts/prepare-retrieval-v0.1.py", "generator_version": VERSION,
                   "generator_sha256": sha(__file_bytes()),
                   "generated_at": datetime.now(timezone.utc).isoformat(),
                   "python": platform.python_version(), "pyyaml": yaml.__version__,
                   "algorithm": "HMAC-SHA256 labeled seeds; Python Random.shuffle"}
    write_new(PRIVATE / "retrieval-seed.yaml", yaml_bytes(seed_record), private=True)
    key, arms = representations(accepted, seed)
    write_new(PRIVATE / "candidate-key.yaml", yaml_bytes(key), private=True)
    for arm, name in (("schema", "schema-arm"), ("baseline", "name-practice-arm")):
        validate_candidates(arms[arm], arm)
        write_new(BENCH / f"candidates/{name}.yaml", yaml_bytes(arms[arm]))
    records = []
    for path, packet in packets(targets, arms, seed).items():
        data = yaml_bytes(packet)
        write_new(BENCH / "retrieval-packets" / path, data)
        records.append({k: packet[k] for k in ("target_id", "arm", "run")} |
                       {"path": path, "sha256": sha(data)})
    packet_manifest = {"version": "0.1", "status": "frozen-before-retrieval", "packet_count": 60,
                       "packets": records,
                       "execution_order": shuffled([r["path"] for r in records], seed, "execution-order")}
    write_new(BENCH / "retrieval-packets/manifest.yaml", yaml_bytes(packet_manifest))
    support = [ROOT / "scripts" / name for name in (
        "prepare-retrieval-v0.1.py", "run-retrieval-v0.1.py", "retrieval_v01.py",
        "requirements-retrieval-v0.1.txt", "test_retrieval_v01.py")]
    manifest = {"version": "0.1", "status": "prepared-before-retrieval",
                "protocol_commit": PROTOCOL, "benchmark_commit": BENCHMARK, "corpus_snapshot": CORPUS,
                "candidate_count": 14,
                "candidate_files": {
                    "schema_arm": integrity(BENCH / "candidates/schema-arm.yaml"),
                    "name_practice_arm": integrity(BENCH / "candidates/name-practice-arm.yaml")},
                "retrieval_runs": {"expected": 60, "prepared": 60},
                "packet_manifest": integrity(BENCH / "retrieval-packets/manifest.yaml"),
                "execution_configuration": integrity(BENCH / "execution-config.yaml"),
                "execution_document": integrity(BENCH / "RETRIEVAL-EXECUTION.md"),
                "support_files": [integrity(p) for p in support],
                "generation_environment": {"python": platform.python_version(), "pyyaml": yaml.__version__}}
    write_new(BENCH / "execution-manifest.yaml", yaml_bytes(manifest))
    for arm in ("schema", "baseline"):
        (PRIVATE / "results" / arm).mkdir(parents=True, exist_ok=True, mode=0o700)
    verify(private=True)


def __file_bytes():
    from pathlib import Path
    return Path(__file__).read_bytes()


def verify(private=False):
    accepted, targets = frozen_inputs()
    manifest = read_yaml(BENCH / "execution-manifest.yaml")
    require(manifest["candidate_count"] == 14 and manifest["retrieval_runs"] == {
        "expected": 60, "prepared": 60}, "Execution counts differ")
    require((manifest["protocol_commit"], manifest["benchmark_commit"], manifest["corpus_snapshot"])
            == (PROTOCOL, BENCHMARK, CORPUS), "Frozen references differ")
    for entry in [*manifest["candidate_files"].values(), manifest["packet_manifest"],
                  manifest["execution_configuration"], manifest["execution_document"],
                  *manifest["support_files"]]:
        require(sha((ROOT / entry["path"]).read_bytes()) == entry["sha256"], "Artifact hash differs")
    arms = {"schema": read_yaml(BENCH / "candidates/schema-arm.yaml"),
            "baseline": read_yaml(BENCH / "candidates/name-practice-arm.yaml")}
    for arm in arms:
        validate_candidates(arms[arm], arm)
    # Prove verbatim schema values and same ID association without printing identities.
    unmatched = list(accepted)
    baseline = {c["id"]: c for c in arms["baseline"]}
    for candidate in arms["schema"]:
        matches = [(p, d) for p, d in unmatched if d["instrument"] == candidate["instrument"]
                   and all(d["extraction"][k] == baseline[candidate["id"]][k] for k in ("name", "practice"))]
        require(len(matches) == 1, "Candidate does not match one frozen accepted record")
        unmatched.remove(matches[0])
    pm = read_yaml(BENCH / "retrieval-packets/manifest.yaml")
    expected = {(t["target_id"], a, r) for t in targets for a in arms for r in (1, 2, 3)}
    records = pm["packets"]
    require(pm["packet_count"] == 60 and len(records) == 60, "Packet count differs")
    require([(p["target_id"], p["arm"], p["run"]) for p in records] == sorted(expected),
            "Packet combinations/order differ")
    paths = {p["path"] for p in records}
    require(len(paths) == 60 and len(pm["execution_order"]) == 60
            and set(pm["execution_order"]) == paths, "Execution order differs")
    actual_paths = {str(p.relative_to(BENCH / "retrieval-packets"))
                    for p in (BENCH / "retrieval-packets").glob("*/*.yaml")}
    require(actual_paths == paths, "Unexpected/missing packet files")
    target_by_id = {t["target_id"]: t for t in targets}
    for entry in records:
        raw = (BENCH / "retrieval-packets" / entry["path"]).read_bytes()
        require(sha(raw) == entry["sha256"], "Packet hash differs")
        packet = parse_yaml(raw)
        validate_packet(packet)
        require(all(packet[k] == entry[k] for k in ("target_id", "arm", "run")), "Packet metadata differs")
        require(entry["path"] == f"{packet['arm']}/{packet['target_id']}-run-{packet['run']}.yaml",
                "Packet path differs")
        require(all(packet[k] == v for k, v in target_by_id[packet["target_id"]].items()), "Target differs")
        require(sorted(packet["candidates"], key=lambda c: c["id"]) == arms[packet["arm"]],
                "Packet representation differs")
    if private:
        seed_record = read_yaml(PRIVATE / "retrieval-seed.yaml")
        require(seed_record["generator_sha256"] == sha(__file_bytes()), "Generator changed since seed freeze")
        key, rebuilt = representations(accepted, seed_record["randomization_seed"])
        require(key == read_yaml(PRIVATE / "candidate-key.yaml") and rebuilt == arms, "Private replay differs")
        for path, packet in packets(targets, rebuilt, seed_record["randomization_seed"]).items():
            require(yaml_bytes(packet) == (BENCH / "retrieval-packets" / path).read_bytes(), "Shuffle replay differs")
        require(pm["execution_order"] == shuffled([p["path"] for p in records],
                seed_record["randomization_seed"], "execution-order"), "Execution-order replay differs")
    print("Validated: 14 snapshot candidates; 30 schema + 30 baseline packets; all hashes and isolation checks pass.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--prepare", action="store_true")
    mode.add_argument("--verify", action="store_true")
    parser.add_argument("--private-replay", action="store_true", help="Verify seed/key replay; never reads target key")
    args = parser.parse_args()
    if args.prepare:
        prepare()
    else:
        verify(args.private_replay)
