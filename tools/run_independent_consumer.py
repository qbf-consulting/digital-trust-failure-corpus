#!/usr/bin/env python3
"""Execute a separately implemented CLI and verify its captured output digest."""
import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from tools.execute_binding import ROOT, evaluate

def verify_capture(capture, target, request):
    """Verify recorded response, target source, and request digests against supplied bytes."""
    evidence = capture["evidence"]
    request_bytes = json.dumps(request, sort_keys=True, separators=(",", ":")).encode()
    checks = (
        (evidence["target_sha256"], hashlib.sha256(Path(target).read_bytes()).hexdigest()),
        (evidence["request_sha256"], hashlib.sha256(request_bytes).hexdigest()),
        (evidence["response_sha256"], hashlib.sha256(
            json.dumps(evidence["response"], sort_keys=True).encode()).hexdigest()),
    )
    return all(recorded == actual for recorded, actual in checks)


def run(target, request, case_version, case_revision, *, timeout=5):
    target = Path(target).resolve()
    request_bytes = json.dumps(request, sort_keys=True, separators=(",", ":")).encode()
    completed = subprocess.run([sys.executable, str(target)], input=request_bytes,
                               capture_output=True, timeout=timeout, check=False)
    if completed.returncode:
        raise RuntimeError("Target execution failed (exit code %s)" % completed.returncode)
    try:
        output = json.loads(completed.stdout)
    except (ValueError, UnicodeDecodeError) as exc:
        raise ValueError("Target returned invalid JSON") from exc
    if not isinstance(output, dict) or output.get("disposition") not in ("PASS", "DENY", "INDETERMINATE"):
        raise ValueError("Target returned invalid disposition")
    digest = hashlib.sha256(json.dumps(output, sort_keys=True).encode()).hexdigest()
    target_digest = hashlib.sha256(target.read_bytes()).hexdigest()
    binding = dict(binding_version="0.1.0", case_id="DTF-001", case_version=case_version,
                   case_revision=case_revision, adapter="fixture-v1",
                   scenario="separate-process authority decision", expected="DENY",
                   observed=output["disposition"], evidence=["sha256:"+digest])
    result = evaluate(binding)
    return dict(result=result, evidence=dict(
        target_sha256=target_digest, request_sha256=hashlib.sha256(request_bytes).hexdigest(),
        response_sha256=digest, response=output, timestamp=datetime.now(timezone.utc).isoformat(),
        command=[sys.executable, str(target)], exit_code=completed.returncode),
        limitation="Independent process, locally maintained demonstration target; not external adoption or authenticated authority.")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--target", type=Path, default=ROOT / "examples/independent-consumer/authority_target.py")
    p.add_argument("--request", type=Path, required=True)
    p.add_argument("--case-version", required=True)
    p.add_argument("--case-revision", required=True)
    a = p.parse_args()
    result = run(a.target, json.loads(a.request.read_text()), a.case_version, a.case_revision)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["result"]["test_verdict"] == "SATISFIED" else 1

if __name__ == "__main__":
    raise SystemExit(main())
