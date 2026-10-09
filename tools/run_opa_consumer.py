#!/usr/bin/env python3
"""OPA external-engine experiment. Local policy/fixture is not third-party DTFC adoption."""
import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def digest(data):
    return hashlib.sha256(data).hexdigest()

def evaluate_opa(opa, policy, request, timeout=15):
    opa, policy = Path(opa).resolve(), Path(policy).resolve()
    request_bytes = json.dumps(request, sort_keys=True, separators=(",", ":")).encode()
    version = subprocess.run([str(opa), "version"], capture_output=True, timeout=timeout, check=True)
    completed = subprocess.run(
        [str(opa), "eval", "--format=json", "--data", str(policy),
         "--stdin-input", "data.dtfc.authority.allow"],
        input=request_bytes, capture_output=True, timeout=timeout, check=True)
    data = json.loads(completed.stdout)
    results = data.get("result") if isinstance(data, dict) else None
    if not isinstance(results, list) or len(results) != 1 or not isinstance(results[0], dict):
        raise ValueError("OPA result missing exactly one decision result")
    expressions = results[0].get("expressions")
    if (not isinstance(expressions, list) or len(expressions) != 1
            or not isinstance(expressions[0], dict)
            or type(expressions[0].get("value")) is not bool):
        raise ValueError("OPA result missing a single boolean decision")
    disposition = "PASS" if expressions[0]["value"] else "DENY"
    return dict(disposition=disposition, target_version=version.stdout.decode(errors="replace").strip(),
                target_sha256=digest(opa.read_bytes()), policy_sha256=digest(policy.read_bytes()),
                input_sha256=digest(request_bytes), output_sha256=digest(completed.stdout),
                output=data, collected_at=datetime.now(timezone.utc).isoformat(),
                engine="OPA", policy_source="DTFC example", exit_code=completed.returncode)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--opa", required=True, type=Path)
    parser.add_argument("--policy", required=True, type=Path)
    parser.add_argument("--input", required=True, type=Path)
    args = parser.parse_args()
    request = json.loads(args.input.read_text())
    result = evaluate_opa(args.opa, args.policy, request)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["disposition"] == "DENY" else 1

if __name__ == "__main__":
    raise SystemExit(main())
