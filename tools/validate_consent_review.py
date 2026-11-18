"""Source-pinned Consent family screening; does not certify independent review."""
import json
from pathlib import Path
from tools.validate_trust_tasks_inventory import MANIFEST, ROOT
PATH = ROOT / "research/external-sources/trust-tasks/consent-review.json"

def check(data, inventory):
    indexed={f"https://trusttasks.org/spec/{x['slug']}/{x['version']}":x
             for x in inventory["records"] if x["slug"].startswith("consent/")}
    if data["source_commit"] != inventory["source"]["commit"] or len(indexed)!=8 or data["family"]!="consent":
        raise ValueError("wrong source or family population")
    rows=data["records"]
    if len(rows)!=len(indexed) or len({x["task_type_uri"] for x in rows})!=len(rows):
        raise ValueError("missing or duplicated consent version")
    for r in rows:
        key=r["task_type_uri"]
        if key not in indexed:
            raise ValueError("unknown source version")
        src=indexed[key]
        if r["source_commit"]!=inventory["source"]["commit"] or r["source_path"]!=src["path"] or r["source_blob"]!=src["spec_blob"]:
            raise ValueError("source provenance mismatch")
        if r["review_state"]!="research-screened" or r["independent_review"]!="not-established" or r["execution_evidence"]!="none" or r["case_search_complete"] is not False:
            raise ValueError("false assurance completion")
        if r["classification"] not in {"mechanism-overlap","adjacent"}:
            raise ValueError("unfounded relationship class")
        found=list((ROOT/"corpus").rglob(r["case_id"]+".json"))
        if len(found)!=1 or json.loads(found[0].read_text())["version"]!=r["case_version"]:
            raise ValueError("unknown or stale canonical case")
        for field in ("rationale","local_proposition","unsupported_inference","test_hypothesis","authority_boundary"):
            if len(r[field])<75:
                raise ValueError("unsubstantiated "+field)
        if not r["source_section"] or len(r["evidence_required"])<2:
            raise ValueError("insufficient source and negative-test evidence")
    if data["version_delta"]["equivalence_asserted"] is not False:
        raise ValueError("version equivalence is not supported")
    return {"consent_versions":len(indexed),"research_screened":len(rows),"independently_approved":0}

if __name__=="__main__":
    print(json.dumps(check(json.loads(PATH.read_text()),json.loads(MANIFEST.read_text())),indent=2))
