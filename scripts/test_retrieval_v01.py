"""Synthetic offline tests. Never writes to experimental result directories."""
import copy
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from retrieval_v01 import (BENCH, FIELDS, INSTRUCTION, parse_ranking,
                           read_yaml, validate_packet, yaml_bytes)

spec = importlib.util.spec_from_file_location("runner", Path(__file__).with_name("run-retrieval-v0.1.py"))
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


def fixture():
    return {"experiment": "retrieval-v0.1", "target_id": "TARGET-01", "target_domain": "synthetic test",
            "target": "Synthetic parser fixture, not an experimental target.", "arm": "schema", "run": 1,
            "candidates": [{"id": f"CAND-{i:02}", "instrument": {f: "synthetic" for f in FIELDS}}
                           for i in range(1, 15)], "instruction": INSTRUCTION}


class RetrievalTests(unittest.TestCase):
    def setUp(self):
        self.packet = fixture()
        self.config = read_yaml(BENCH / "execution-config.yaml")
        self.raw = "ranking: [CAND-03, CAND-01, CAND-02]\n"

    def envelope(self, text=None):
        return json.dumps({"model": self.config["requested_model"], "service_tier": "default",
                           "status": "completed", "output": [{"type": "message", "role": "assistant",
                           "content": [{"type": "output_text", "text": text or self.raw}]}]})

    def test_parser_preserves_order_and_optional_rationale(self):
        for text in (self.raw, self.raw + "rationale: synthetic explanation\n"):
            result = parse_ranking(text, self.packet)
            self.assertEqual(result["validation_status"], "valid")
            self.assertEqual(result["parsed_ranking"], ["CAND-03", "CAND-01", "CAND-02"])

    def test_parser_rejects_malformed(self):
        for text in ("", "[]", "ranking: [CAND-01, CAND-02]", "ranking: [CAND-01, CAND-01, CAND-02]",
                     "ranking: [CAND-01, CAND-02, CAND-99]", "ranking: [1, 2, 3]",
                     self.raw + "extra: unwanted", self.raw + "rationale: [bad]",
                     self.raw + self.raw, "```yaml\n" + self.raw + "```",
                     "ranking: &x [CAND-01, CAND-02, CAND-03]\nrationale: *x",
                     self.raw + "---\n" + self.raw):
            with self.subTest(text=text):
                self.assertEqual(parse_ranking(text, self.packet)["validation_status"], "malformed")

    def test_key_isolation_both_arms(self):
        validate_packet(self.packet)
        for key in ("name", "practice", "source", "notes", "ambiguities", "extraction_failures"):
            packet = copy.deepcopy(self.packet)
            packet["candidates"][0][key] = "forbidden"
            with self.assertRaises(ValueError):
                validate_packet(packet)
        packet = copy.deepcopy(self.packet)
        packet["arm"] = "baseline"
        packet["candidates"] = [{"id": c["id"], "name": "synthetic", "practice": "synthetic"}
                                 for c in packet["candidates"]]
        validate_packet(packet)
        for key in FIELDS:
            contaminated = copy.deepcopy(packet)
            contaminated["candidates"][0][key] = "forbidden"
            with self.assertRaises(ValueError):
                validate_packet(contaminated)

    def test_payload_has_only_packet_and_fixed_instructions(self):
        text = yaml_bytes(self.packet).decode()
        body = runner.request_body(text, self.config)
        self.assertEqual(body["input"], [{"role": "user", "content": [{"type": "input_text", "text": text}]}])
        self.assertEqual(body["instructions"], self.config["system_instruction"])
        self.assertEqual(body["tools"], [])
        self.assertEqual(body["tool_choice"], "none")
        self.assertFalse(body["store"])
        self.assertFalse({"previous_response_id", "conversation", "temperature", "top_p", "metadata"} & body.keys())

    def test_provider_envelope_failure_modes(self):
        self.assertEqual(runner.interpret(self.envelope(), self.packet, self.config)["validation_status"], "valid")
        for raw, status in (("[]", "malformed"), ("not json", "malformed")):
            self.assertEqual(runner.interpret(raw, self.packet, self.config)["validation_status"], status)
        for change, status in (({"status": "incomplete"}, "incomplete"),
                               ({"model": "different-model"}, "configuration_mismatch"),
                               ({"service_tier": "priority"}, "configuration_mismatch"),
                               ({"output": [{"type": "function_call"}]}, "malformed")):
            envelope = json.loads(self.envelope()) | change
            self.assertEqual(runner.interpret(json.dumps(envelope), self.packet, self.config)["validation_status"], status)

    def test_retry_capture_and_no_overwrite(self):
        with tempfile.TemporaryDirectory(prefix="retrieval-synthetic-") as tmp, patch.dict(os.environ, {"OPENAI_API_KEY": "synthetic"}):
            calls, delays = [], []

            def fake_send(body, key, timeout):
                calls.append(body)
                return (503, "synthetic unavailable", "synthetic-1") if len(calls) == 1 else (200, self.envelope(), "synthetic-2")

            directory = Path(tmp) / "synthetic-run"
            status = runner.measure(self.packet, yaml_bytes(self.packet).decode(), self.config,
                                    directory, send=fake_send, sleep=delays.append)
            self.assertEqual(status, "valid")
            self.assertEqual(calls[0], calls[1])
            self.assertEqual(delays, [5])
            self.assertTrue((directory / "attempt-1.json").exists())
            self.assertTrue((directory / "attempt-2.json").exists())
            before = (directory / "result.json").read_bytes()
            with self.assertRaises(FileExistsError):
                runner.measure(self.packet, self.raw, self.config, directory, send=fake_send)
            self.assertEqual((directory / "result.json").read_bytes(), before)
            self.assertEqual(len(calls), 2)

    def test_malformed_not_retried(self):
        with tempfile.TemporaryDirectory(prefix="retrieval-synthetic-") as tmp, patch.dict(os.environ, {"OPENAI_API_KEY": "synthetic"}):
            calls = []

            def fake_send(*args):
                calls.append(1)
                return 200, self.envelope("ranking: []"), None

            status = runner.measure(self.packet, yaml_bytes(self.packet).decode(), self.config,
                                    Path(tmp) / "synthetic-run", send=fake_send)
            self.assertEqual(status, "malformed")
            self.assertEqual(len(calls), 1)

    def test_exhausted_transport_retries(self):
        with tempfile.TemporaryDirectory(prefix="retrieval-synthetic-") as tmp, patch.dict(os.environ, {"OPENAI_API_KEY": "synthetic"}):
            calls, delays = [], []

            def fake_send(*args):
                calls.append(1)
                raise TimeoutError("synthetic")

            directory = Path(tmp) / "synthetic-run"
            status = runner.measure(self.packet, yaml_bytes(self.packet).decode(), self.config,
                                    directory, send=fake_send, sleep=delays.append)
            self.assertEqual(status, "provider_error")
            self.assertEqual(len(calls), 3)
            self.assertEqual(delays, [5, 20])
            self.assertEqual(len(list(directory.glob("attempt-*.json"))), 3)


if __name__ == "__main__":
    # Any accidental use of the real transport fails before a socket opens.
    with patch("socket.socket", side_effect=AssertionError("Network forbidden in offline tests")):
        unittest.main()
