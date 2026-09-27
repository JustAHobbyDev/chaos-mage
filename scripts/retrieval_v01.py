"""Shared offline formats for retrieval v0.1; no ground truth or network access."""
import hashlib
import os
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
BENCH = ROOT / "benchmark/retrieval-v0.1"
PRIVATE = ROOT / ".runtime/retrieval-v0.1"
CORPUS = "9a5bc7e626d1e5f27d6ecec224f70dbc08a6a3a2"
BENCHMARK = "a3793f671b5cf3796071f887d7fc086f53d81d28"
PROTOCOL = "c0daa4ef06f7c077d87e7e3232a72fefabac7308"
FIELDS = ("state", "operation", "signal", "inference", "limit")
IDS = {f"CAND-{n:02}" for n in range(1, 15)}
INSTRUCTION = (
    "Rank the three instruments whose operational structure is most applicable "
    "to this target. Prefer structural fit over vocabulary or source-domain "
    "resemblance. Return exactly three opaque IDs in ranked order, with an "
    "optional short structural rationale after the ranking."
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


class StrictLoader(yaml.SafeLoader):
    def compose_node(self, parent, index):
        if self.check_event(yaml.AliasEvent):
            raise ValueError("YAML aliases are not allowed")
        return super().compose_node(parent, index)


def unique_mapping(loader, node):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=True)
        require(isinstance(key, str), "Mapping keys must be strings")
        require(key not in result, "Duplicate mapping key")
        result[key] = loader.construct_object(value_node, deep=True)
    return result


StrictLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def parse_yaml(text):
    return yaml.load(text, Loader=StrictLoader)


def read_yaml(path):
    return parse_yaml(path.read_text(encoding="utf-8"))


class Dumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True


def represent_string(dumper, value):
    return dumper.represent_scalar("tag:yaml.org,2002:str", value,
                                   style="|" if "\n" in value else None)


Dumper.add_representer(str, represent_string)


def yaml_bytes(value):
    return yaml.dump(value, Dumper=Dumper, allow_unicode=True, sort_keys=False,
                     width=100).encode("utf-8")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write_new(path, data, private=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                 0o600 if private else 0o644)
    with os.fdopen(fd, "wb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def validate_candidates(candidates, arm):
    require(isinstance(candidates, list) and len(candidates) == 14, "Expected 14 candidates")
    found = []
    for candidate in candidates:
        keys = {"id", "instrument"} if arm == "schema" else {"id", "name", "practice"}
        require(isinstance(candidate, dict) and set(candidate) == keys, "Candidate keys differ")
        require(isinstance(candidate["id"], str), "ID must be a string")
        found.append(candidate["id"])
        values = candidate["instrument"] if arm == "schema" else {
            key: candidate[key] for key in ("name", "practice")}
        require(isinstance(values, dict), "Candidate representation must be a mapping")
        if arm == "schema":
            require(set(values) == set(FIELDS), "Schema keys differ")
        require(all(isinstance(v, str) and v.strip() for v in values.values()),
                "Representation values must be nonempty strings")
    require(len(set(found)) == 14 and set(found) == IDS, "Candidate IDs differ")


def validate_packet(packet):
    require(isinstance(packet, dict) and set(packet) == {
        "experiment", "arm", "target_id", "run", "target_domain", "target",
        "candidates", "instruction"}, "Packet keys differ")
    require(packet["experiment"] == "retrieval-v0.1", "Wrong experiment")
    require(packet["arm"] in ("schema", "baseline"), "Unknown arm")
    require(packet["target_id"] in {f"TARGET-{n:02}" for n in range(1, 11)}, "Unknown target")
    require(type(packet["run"]) is int and packet["run"] in (1, 2, 3), "Unknown repetition")
    require(all(isinstance(packet[k], str) and packet[k].strip()
                for k in ("target", "target_domain")), "Missing target text/domain")
    require(packet["instruction"] == INSTRUCTION, "Ranking instruction differs")
    validate_candidates(packet["candidates"], packet["arm"])


def parse_ranking(raw, packet):
    """Shape only. Never sorts, repairs, scores, or resolves candidate identities."""
    try:
        value = parse_yaml(raw)
        require(isinstance(value, dict), "Response must be a mapping")
        require(set(value) in ({"ranking"}, {"ranking", "rationale"}), "Response keys differ")
        ranking = value["ranking"]
        require(isinstance(ranking, list) and len(ranking) == 3, "Expected exactly three IDs")
        require(all(isinstance(item, str) for item in ranking), "IDs must be strings")
        require(len(set(ranking)) == 3, "Duplicate IDs")
        require(set(ranking) <= {c["id"] for c in packet["candidates"]}, "Unknown IDs")
        require("rationale" not in value or isinstance(value["rationale"], str),
                "Rationale must be a string")
        return {"validation_status": "valid", "parsed_ranking": ranking,
                "rationale": value.get("rationale"), "validation_error": None}
    except (ValueError, yaml.YAMLError, TypeError) as exc:
        # Never echo raw response content in diagnostics.
        return {"validation_status": "malformed", "parsed_ranking": None,
                "rationale": None, "validation_error": type(exc).__name__}
