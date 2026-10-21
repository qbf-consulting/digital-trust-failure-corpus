#!/usr/bin/env python3
"""Execute pinned RAHP optional R1–R3 reasoning on CPC-001's declared evidence boundary.

The optional profiles are NOT a terminal RAHP assessment/controller. All findings
must be interpreted within the synthetic-scaffold question.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[4]
CPC = BASE / "research/consumer-protection/cpc-001-agent-delegation-revocation"
CLAIM_FILES = {
    "C1": ["protection-contracts.yaml", "requirements-traceability.yaml", "examples/cpc-001/protected_resource.py"],
    "C2": ["protection-contracts.yaml", "requirements-traceability.yaml"],
    "C3": ["examples/cpc-001/protected_resource.py", "examples/cpc-001/defective_protected_resource.py", "tests/test_cpc001_executable_fixture.py"],
    "C4": ["revocation-semantics.md", "examples/cpc-001/protected_resource.py", "tests/test_cpc001_executable_fixture.py"],
    "C5": ["protection-contracts.yaml", "examples/cpc-001/protected_resource.py", "tests/test_cpc001_executable_fixture.py"],
    "C6": ["evidence/evidence-manifest.yaml", "evidence/reproduction-instructions.md", "tools/execute_cpc001.py"],
    "C7": ["protection-contracts.yaml", "requirements-traceability.yaml"],
}
NO_RUNTIME_CLAIMS = {"C2", "C7"}
DTFC_PIN = "e7246692bc8f8350888aac2fabe2ce82886d146a"
RAHP_PIN = "7cd34ed53c537a43c0c5ed1a526a3748055e3f1c"

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--rahp", type=Path, required=True, help="Checkout of pinned RAHP v2.8.0")
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    rahp = args.rahp.resolve()
    actual = subprocess.check_output(["git", "-C", str(rahp), "rev-parse", "HEAD"], text=True).strip()
    if actual != RAHP_PIN:
        raise SystemExit(f"RAHP revision mismatch: expected {RAHP_PIN}, got {actual}")
    # Optional R1/R2/R3 are standalone stdlib modules.
    sys.path.insert(0, str(rahp))
    from tools.evidence_adequacy import evaluate
    from tools.temporal_provenance import evaluate_temporal
    from tools.reproducibility_challenge import compare
    scope = "CPC-001 committed synthetic scaffold; metadata availability only"
    files = {}
    claims = {}
    for claim, refs in sorted(CLAIM_FILES.items()):
        observations = []
        for index, ref in enumerate(refs):
            source = (BASE / ref if ref.startswith(("examples/", "tests/", "tools/")) else CPC / ref)
            found = source.is_file()
            if found:
                tracked_path = str(source.relative_to(BASE))
                pinned = subprocess.check_output(["git", "-C", str(BASE), "show", f"{DTFC_PIN}:{tracked_path}"])
                if pinned != source.read_bytes():
                    raise SystemExit(f"Evidence content differs from pinned DTFC revision: {tracked_path}")
            files[ref] = {
                "present": found, "sha256": sha256(source.read_bytes()) if found else None
            }
            # SATISFIED here denotes only file presence, not evidence truth or claim correctness.
            observations.append({
                "id": f"{claim}-OBS-{index+1}", "evidence_id": ref,
                "scope": scope, "state": "SATISFIED" if found else "UNAVAILABLE"
            })
        if claim in NO_RUNTIME_CLAIMS:
            # Consumer inspection and challenge cannot be tested from document presence.
            observations = []
        profile = {"schema": "rahp-evidence-adequacy/v1",
                   "proposition_id": f"CPC-001-{claim}-FILE-AVAILABILITY",
                   "scope": scope, "required_evidence": refs, "observations": observations}
        claims[claim] = {"r1": evaluate(profile), "input": profile,
                         "claim_status": "NOT_ASSESSED" if claim in NO_RUNTIME_CLAIMS else "INDETERMINATE"}
    # R2: absence of independent temporal observations is not transformed into invented timestamps.
    r2_profile = {"schema": "rahp-temporal-provenance/v1",
        "proposition_id": "CPC-001-REVOCATION-TEMPORAL-APPLICABILITY",
        "target_time": "2026-10-21T00:00:00Z",
        "knowledge_cutoff": "2026-10-21T00:00:00Z",
        "evaluated_at": "2026-10-21T00:00:00Z",
        "required_evidence": ["independent-revocation-runtime-observation"],
        "records": []}
    r2 = evaluate_temporal(r2_profile)
    # R3 compares two actual in-process invocations of the R1 evaluator over identical
    # declared input. This is NOT independent execution or source authentication.
    pair = claims["C4"]["input"]
    a, b = evaluate(pair), evaluate(pair)
    pin = {"algorithm": "sha256", "digest": sha256(canonical(pair))}
    r3_profile = {"schema": "rahp-reproducibility-challenge/v1",
        "proposition_id": "CPC-001-C4-R1-STRUCTURAL-REPLAY",
        "runs": [{"id": rid, "evaluator_id": "rahp-evidence-adequacy",
                 "evaluator_version": "v1@"+RAHP_PIN[:12],
                 "input_pin": pin, "outcome": result["outcome"]}
                 for rid, result in (("local-run-A", a), ("local-run-B", b))],
        "challenges": [{"id": "CPC-001-EXTERNAL-REPRO-OPEN", "run_id": "local-run-A",
                        "reason": "EVIDENCE", "evidence_refs": ["independent-reproduction"]}]}
    r3 = compare(r3_profile)
    # Negative controls use actual RAHP evaluators, not hand-written expected dispositions.
    negative = {}
    missing = dict(pair, observations=[])
    negative["missing_r1"] = evaluate(missing)
    conflict = dict(pair, observations=pair["observations"] + [dict(pair["observations"][0], id="C4-DUPLICATE")])
    negative["conflicting_r1"] = evaluate(conflict)
    stale = dict(r2_profile, records=[{
        "id": "synthetic-stale-revocation", "evidence_id": "independent-revocation-runtime-observation",
        "source_pin": {"repository": "qbf-consulting/digital-trust-failure-corpus", "revision": DTFC_PIN},
        "observed_at": "2026-01-01T00:00:00Z", "recorded_at": "2026-01-02T00:00:00Z",
        "effective_from": "2026-01-01T00:00:00Z"
    }], max_observation_age_seconds=86400)
    negative["synthetic_stale_r2"] = evaluate_temporal(stale)
    if negative["missing_r1"]["outcome"] != "INDETERMINATE":
        raise AssertionError("missing evidence became PASS")
    if negative["conflicting_r1"]["outcome"] != "INDETERMINATE":
        raise AssertionError("conflicting evidence became PASS")
    if negative["synthetic_stale_r2"]["disposition"] != "INDETERMINATE":
        raise AssertionError("stale observation became applicable")
    if r2["disposition"] != "INDETERMINATE" or r3["disposition"] != "DECLARED_MATCH":
        raise AssertionError("unexpected R2/R3 result")
    result = {
        "assessment_type": "RAHP optional reasoning-profile execution; not terminal assessment",
        "subject": "CPC-001 synthetic scaffold",
        "dtfc_revision": DTFC_PIN, "rahp_revision": RAHP_PIN,
        "rahp_release": "v2.8.0", "profile_versions": [
            "rahp-evidence-adequacy/v1", "rahp-temporal-provenance/v1", "rahp-reproducibility-challenge/v1"],
        "python": platform.python_version(), "source_files": files,
        "claim_results": claims, "r2": {"input": r2_profile, "result": r2},
        "r3": {"input": r3_profile, "result": r3},
        "negative_controls": negative,
        "limits": ["No independent implementation evidence", "No independent reproduction",
                   "No consumer usability validation", "No terminal RAHP controller disposition",
                   "No runtime revocation or replay execution in these optional profiles",
                   "C2 and C7 NOT_ASSESSED; C1/C3/C4/C5/C6 INDETERMINATE"],
    }
    out = args.output
    out.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(result, indent=2, sort_keys=True) + "\n"
    (out / "cpc001-rahp-reasoning-result.json").write_text(raw, encoding="utf-8")
    lines = ["# CPC-001 pinned RAHP R1–R3 execution", "",
        "**Scope:** synthetic scaffold and declared structural metadata only. This is not a terminal RAHP assurance result.", "",
        f"- DTFC pin: `{DTFC_PIN}`", f"- RAHP pin: `{RAHP_PIN}` (v2.8.0)",
        f"- Python: `{platform.python_version()}`", "",
        "## Claim-level bounded outcomes", "",
        "| Claim | R1 file-availability only | CPC-001 assessment state |",
        "|---|---|---|"]
    for claim, record in claims.items():
        lines.append(f"| {claim} | {record['r1']['outcome']} | {record['claim_status']} |")
    lines += ["", "R1 PASS means **only referenced files exist**. It does not establish a claim, authenticity or revocation safety.", "",
       f"R2 temporal applicability: **{r2['disposition']}** (independent runtime records absent).",
       f"R3 local declared comparison: **{r3['disposition']}** (two local R1 invocations; challenge remains OPEN).", "",
       "## Negative controls", "",
       f"- Missing R1 evidence: **{negative['missing_r1']['outcome']}**.",
       f"- Duplicate/conflicting R1 evidence: **{negative['conflicting_r1']['outcome']}**.",
       f"- Synthetic stale R2 evidence: **{negative['synthetic_stale_r2']['disposition']}**.", "",
       "## Remaining assurance gates", "",
       "No independent target, independent consumer, production revocation, consumer inspection/challenge or terminal RAHP assurance is established. See DTFC #48 and #45.",
       "Post-revocation enforcement and replay behavior belong to existing synthetic executable tests, not to optional R1–R3 outcomes.", "",
       f"Raw JSON SHA-256: `{sha256(raw.encode())}`", ""]
    (out / "cpc001-rahp-reasoning-report.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"ra_hp_r2":r2["disposition"],"ra_hp_r3":r3["disposition"],
                      "result_sha256":sha256(raw.encode()),"claims":{k:v["claim_status"] for k,v in claims.items()}},sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
