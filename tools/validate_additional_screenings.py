"""Validate source-pinned supplementary DTFC research, not approval."""
import json
from tools.validate_trust_tasks_inventory import MANIFEST, ROOT
PATH=ROOT/"research/external-sources/trust-tasks/additional-screenings.json"
FAMILIES={"audit","governance","task-consent","trust-task-discovery","trust-ceremony-receipt"}
def check(data,inventory):
    source={"https://trusttasks.org/spec/"+r["slug"]+"/"+r["version"]:r for r in inventory["records"] if r["slug"].split("/")[0] in FAMILIES}
    rows=data["records"]
    if data["source_commit"]!=inventory["source"]["commit"] or set(data["families"])!=FAMILIES or len(source)!=15 or len(rows)!=15 or set(source)!={r["task_type_uri"] for r in rows}:
        raise ValueError("unreconciled family inventory")
    for r in rows:
        ref=source[r["task_type_uri"]]
        if r["source_blob"]!=ref["spec_blob"] or r["source_path"]!=ref["path"] or r["source_commit"]!=inventory["source"]["commit"]:
            raise ValueError("incorrect source provenance")
        if (r["review_state"]!="research-screened" or r["independent_review"]!="not-established" or r["execution_evidence"]!="none" or r["case_search_complete"] is not False or r["version_inheritance"]!="not-authorized"):
            raise ValueError("false assurance or equivalence")
        if r["classification"] not in {"adjacent","mechanism-overlap"} or not r["source_section"]:
            raise ValueError("inadequate source classification")
        cases=list((ROOT/"corpus").rglob(r["case_id"]+".json"))
        if len(cases)!=1 or json.loads(cases[0].read_text())["version"]!=r["case_version"]:
            raise ValueError("canonical case unresolved")
        if any(len(r[f])<65 for f in ("rationale","test_hypothesis","authority_boundary")):
            raise ValueError("inadequate falsification rationale")
    return {"sources":len(source),"screened":len(rows),"reviewed":0}
if __name__=="__main__":
    print(json.dumps(check(json.loads(PATH.read_text()),json.loads(MANIFEST.read_text())),indent=2))
