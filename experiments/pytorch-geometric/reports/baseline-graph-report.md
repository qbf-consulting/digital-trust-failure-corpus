# DTFC experimental graph baseline report

This report is a deterministic research sidecar for the experimental PyTorch Geometric graph-learning tranche. It is not corpus authority, normative coverage evidence, external adoption evidence, assurance certification, or a machine-learning result.

## Summary

| Metric | Value |
|---|---:|
| Canonical draft cases represented by the current corpus baseline | 37 |
| Learned embeddings generated | 0 |
| Clusters generated | 0 |
| Link-prediction claims generated | 0 |
| PASS/FAIL/risk/compliance claims generated | 0 |

## Evidence boundary

- The report is derived from the experimental projection of `corpus/**/*.json`.
- The canonical corpus JSON and `schemas/failure-case.schema.json` remain authoritative for case content and structure.
- This report does not change the release baseline and does not create new conformance evidence.
- PyTorch/PyG conversion remains optional and must be validated in an environment where the heavy optional dependencies are intentionally installed.

## Deterministic graph facts to regenerate

Use the following command sequence to regenerate the full typed node and edge count report from the current working tree:

```bash
python experiments/pytorch-geometric/build_graph.py \
  --corpus corpus \
  --output /tmp/dtfc-graph.json

python experiments/pytorch-geometric/graph_report.py \
  --graph /tmp/dtfc-graph.json \
  --output experiments/pytorch-geometric/reports/baseline-graph-report.md
```

The generated report includes:

- total case nodes;
- total nodes;
- total edges;
- isolated nodes;
- node type counts;
- edge relation counts;
- domain counts;
- failure-class counts;
- evidence-category counts;
- reference-type counts;
- expected-disposition counts.

## Interpretation

The useful output of this tranche is the graph inspection surface, not a learned model. The next valid question is whether deterministic graph facts expose useful authoring or review signals. Model training should remain out of scope until the deterministic report is demonstrably useful.
