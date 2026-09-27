#!/usr/bin/env python3
"""One isolated measurement, opt-in only. Default checks input without networking."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import socket
import subprocess
import time
import urllib.error
import urllib.request

from retrieval_v01 import (ROOT, BENCH, PRIVATE, read_yaml, parse_yaml, sha,
                           require, validate_packet, parse_ranking, write_new)


def checked_file(entry):
    path = ROOT / entry["path"]
    data = path.read_bytes()
    require(sha(data) == entry["sha256"], "Frozen artifact hash differs")
    return data


def load_input(packet_name):
    manifest = read_yaml(BENCH / "execution-manifest.yaml")
    pm = parse_yaml(checked_file(manifest["packet_manifest"]))
    config = parse_yaml(checked_file(manifest["execution_configuration"]))
    checked_file(manifest["execution_document"])
    for entry in manifest["support_files"]:
        checked_file(entry)
    matches = [r for r in pm["packets"] if r["path"] == packet_name]
    require(len(matches) == 1, "Choose one exact packet path from the frozen manifest")
    entry = matches[0]
    path = BENCH / "retrieval-packets" / packet_name
    require(path.resolve().is_relative_to((BENCH / "retrieval-packets").resolve()), "Invalid packet path")
    raw = path.read_bytes()
    require(sha(raw) == entry["sha256"], "Packet hash differs")
    packet = parse_yaml(raw)
    validate_packet(packet)
    require(all(packet[k] == entry[k] for k in ("target_id", "arm", "run")), "Packet metadata differs")
    return packet, raw.decode("utf-8"), config, pm


def request_body(packet_text, config):
    # No candidate files, Git data, environment, prior responses, or conversation ID.
    return {"model": config["requested_model"],
            "instructions": config["system_instruction"],
            "input": [{"role": "user", "content": [{"type": "input_text", "text": packet_text}]}],
            "reasoning": {"effort": config["reasoning_effort"]},
            "service_tier": config["service_tier"],
            "max_output_tokens": config["max_output_tokens"],
            "text": {"format": {"type": "text"}, "verbosity": config["text_verbosity"]},
            "tools": [], "tool_choice": "none", "store": False,
            "stream": False, "truncation": "disabled"}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def transport(body, api_key, timeout):
    request = urllib.request.Request("https://api.openai.com/v1/responses", data=body,
        headers={"Authorization": "Bearer " + api_key, "Content-Type": "application/json"}, method="POST")
    # Ignore inherited proxies/endpoint overrides and never forward credentials on redirects.
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    try:
        with opener.open(request, timeout=timeout) as response:
            return response.status, response.read().decode("utf-8"), response.headers.get("x-request-id")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", errors="replace"), exc.headers.get("x-request-id")


def interpret(raw, packet, config):
    result = {"served_model": None, "serving_metadata": {}, "raw_response": raw,
              "parsed_ranking": None, "validation_status": "malformed", "validation_error": None}
    try:
        envelope = json.loads(raw)
        require(isinstance(envelope, dict), "Provider response is not an object")
        result["served_model"] = envelope.get("model")
        result["serving_metadata"] = {k: envelope.get(k) for k in (
            "id", "created_at", "status", "model", "service_tier", "system_fingerprint",
            "usage", "reasoning", "temperature", "top_p", "max_output_tokens",
            "incomplete_details", "error")}
        output = envelope.get("output", [])
        require(isinstance(output, list), "Provider output is not an array")
        require(all(isinstance(item, dict) and item.get("type") in ("message", "reasoning")
                    for item in output), "Unexpected output/tool item")
        messages = [item for item in output if item.get("type") == "message"]
        content = [part for message in messages for part in message.get("content", [])]
        if any(part.get("type") == "refusal" for part in content):
            result["validation_status"] = "refused"
            return result
        if envelope.get("status") != "completed":
            result["validation_status"] = "incomplete"
            return result
        require(len(messages) == 1 and messages[0].get("role") == "assistant", "Expected one assistant message")
        require(len(content) == 1 and content[0].get("type") == "output_text", "Expected one output text")
        result["response_text"] = content[0]["text"]
        parsed = parse_ranking(result["response_text"], packet)
        result.update(parsed)
        if (envelope.get("model") != config["requested_model"]
                or envelope.get("service_tier") != config["service_tier"]):
            result["validation_status"] = "configuration_mismatch"
        return result
    except (ValueError, KeyError, TypeError, AttributeError):
        result["validation_error"] = "Invalid provider envelope"
        return result


def now():
    return datetime.now(timezone.utc).isoformat()


def store_record(path, record):
    write_new(path, (json.dumps(record, ensure_ascii=False, indent=2) + "\n").encode(), private=True)


def measure(packet, text, config, directory, send=transport, sleep=time.sleep):
    """Exclusive reservation protects against concurrent and repeated submissions."""
    api_key = os.environ.get("OPENAI_API_KEY")
    require(bool(api_key), "OPENAI_API_KEY is required only for later execution")
    directory.mkdir(mode=0o700, parents=True, exist_ok=False)
    body = json.dumps(request_body(text, config), ensure_ascii=False).encode("utf-8")
    base = {k: packet[k] for k in ("target_id", "arm", "run")} | {
        "packet_sha256": sha(text.encode("utf-8")), "requested_model": config["requested_model"],
        "provider": config["provider"], "configuration": config, "request_sha256": sha(body)}
    store_record(directory / "reservation.json", base | {"reserved_at": now()})
    policy = config["retry_policy"]
    for attempt in range(1, policy["max_attempts"] + 1):
        record = base | {"attempt": attempt, "started_at": now(), "served_model": None,
                         "raw_response": None, "parsed_ranking": None, "http_status": None,
                         "request_id": None, "validation_status": "provider_error"}
        retry = False
        try:
            status, raw, request_id = send(body, api_key, config["timeout_seconds"])
            record.update(http_status=status, request_id=request_id, raw_response=raw)
            if status == 200:
                record.update(interpret(raw, packet, config))
            else:
                retry = status in policy["retry_http_statuses"]
        except (urllib.error.URLError, socket.timeout, ConnectionError, OSError) as exc:
            # Exception messages may contain infrastructure details; preserve type only.
            record["transport_error"] = type(exc).__name__
            retry = policy["retry_transport_errors"]
        record["finished_at"] = now()
        store_record(directory / f"attempt-{attempt}.json", record)
        if not retry or attempt == policy["max_attempts"]:
            store_record(directory / "result.json", record)
            return record["validation_status"]
        sleep(policy["delays_seconds"][attempt - 1])


def assert_committed():
    # Bind local hashes to the checked-out preparation commit; no unstaged config overrides.
    paths = ["benchmark/retrieval-v0.1/execution-manifest.yaml"]
    manifest = read_yaml(BENCH / "execution-manifest.yaml")
    paths += [entry["path"] for entry in manifest["support_files"]]
    paths += [manifest[k]["path"] for k in ("execution_configuration", "execution_document", "packet_manifest")]
    for path in paths:
        committed = subprocess.check_output(["git", "-C", str(ROOT), "show", f"HEAD:{path}"])
        require(committed == (ROOT / path).read_bytes(), "Uncommitted execution artifact; stop")


def enforce_order(packet_name, pm):
    # Prior local statuses gate scheduling only; no prior content enters the model request.
    for path in pm["execution_order"]:
        arm, filename = path.split("/")
        directory = PRIVATE / "results" / arm / Path(filename).stem
        if path == packet_name:
            require(not directory.exists(), "Run already reserved; never overwrite/restart")
            return
        result_path = directory / "result.json"
        require(result_path.exists(), "Follow frozen execution_order; an earlier run is unfinished")
        prior = json.loads(result_path.read_text())
        require(prior["validation_status"] in ("valid", "malformed", "refused", "incomplete"),
                "Earlier infrastructure/configuration failure requires operator review")
    raise ValueError("Packet missing from execution order")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", help="Manifest-relative path, e.g. schema/TARGET-01-run-1.yaml")
    parser.add_argument("--execute", action="store_true", help="Send a measurement (later phase only)")
    args = parser.parse_args()
    packet, text, config, pm = load_input(args.packet)
    if not args.execute:
        request_body(text, config)
        print("Offline check passed; no request sent and no result created.")
        return
    assert_committed()
    enforce_order(args.packet, pm)
    directory = PRIVATE / "results" / packet["arm"] / Path(args.packet).stem
    status = measure(packet, text, config, directory)
    print(f"Immutable private record written; validation_status={status}")


if __name__ == "__main__":
    main()
