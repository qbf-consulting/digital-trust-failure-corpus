# Experimental PyTorch Geometric assurance graph

This directory contains a bounded research sidecar for exploring whether DTFC failure cases can be projected into a graph suitable for PyTorch Geometric experiments.

The experiment is **not authoritative**. It does not change the canonical corpus, case schema, validation CLI, release baseline, or conformance expectations. Learned outputs are hypotheses for review, not evidence of conformance, assurance, severity, applicability, or correctness.

## Proposition

DTFC cases already contain repeated graph-shaped structure:

- cases;
- domains;
- failure classes;
- evidence categories;
- reference types;
- expected dispositions.

This experiment tests whether a deterministic projection of that structure can support later graph-learning work, such as clustering, related-case discovery, missing-evidence hypotheses, and authoring assistance.

## Authority boundary

Authoritative DTFC artifacts remain:

- `corpus/**/*.json`;
- `schemas/failure-case.schema.json`;
- `tools/validate.py`;
- repository tests;
- issue and pull request judgment records;
- tagged releases.

Derived artifacts in this directory are advisory research outputs. They must not be used to mark a failure case as PASS, FAIL, compliant, safe, severe, complete, independently evidenced, or normatively valid.

## What is included

```text
graph_builder.py                  Deterministic graph extraction and optional PyG conversion
build_graph.py                    CLI wrapper for JSON graph export and optional PyG smoke check
requirements-experimental.txt     Optional PyTorch / PyTorch Geometric dependencies
tests/test_graph_builder.py       Unit tests for graph extraction and dependency isolation
```

## Run the tests

The tests intentionally do not require PyTorch or PyTorch Geometric.

```bash
python -m unittest discover -s experiments/pytorch-geometric/tests -v
```

## Export a graph JSON sidecar

```bash
python experiments/pytorch-geometric/build_graph.py \
  --corpus corpus \
  --output experiments/pytorch-geometric/out/dtfc-graph.json
```

The output is deterministic JSON with typed nodes and edges.

## Optional PyTorch Geometric smoke check

Install optional experiment dependencies in an isolated environment.

```bash
python -m pip install -r experiments/pytorch-geometric/requirements-experimental.txt
python experiments/pytorch-geometric/build_graph.py \
  --corpus corpus \
  --output experiments/pytorch-geometric/out/dtfc-graph.json \
  --check-pyg
```

The PyG conversion currently uses minimal node-type one-hot features. This is deliberate: the first tranche tests graph extraction and dependency boundaries, not model quality.

## Evaluation questions

The branch should be judged against these questions before any mainline adoption decision:

1. Can the canonical corpus be converted into a stable graph without schema changes?
2. Does the graph expose useful relationships that are not obvious from individual case files?
3. Do graph-derived clusters or neighbours help authors find related cases faster than taxonomy traversal alone?
4. Can missing-edge hypotheses be reviewed without being mistaken for evidence?
5. Does the optional dependency model keep DTFC's core validation path lightweight and deterministic?

## Non-goals

This experiment does not provide:

- ML-derived conformance decisions;
- risk scoring;
- automatic case maturity classification;
- normative assurance levels;
- release artifacts;
- public API changes;
- schema changes;
- independent third-party evidence.

## Next experimental increments

If this tranche is useful, the next increments should remain separately reviewable:

1. add a graph summary report;
2. add nearest-neighbour baselines using deterministic graph metrics;
3. compare deterministic neighbours with embedding neighbours;
4. add human-review fixtures for whether discovered relationships are useful;
5. only then consider a small PyG training script.
