# Versioned subprocess conformance vectors

The experimental vector runner reads `conformance/vectors/DTF-*.json` and invokes **allowlisted** local Python subprocess targets, using the same JSON request for safe and defective paths.

```bash
python -m tools.run_conformance
python -m unittest tests.test_conformance_vectors
```

Each result records canonical case version and digest, target source SHA-256, raw response, request/response SHA-256, disposition, test verdict and replay command. The summary computes the canonical case denominator from `corpus/` rather than a hard-coded 37. Missing request, mismatched case version, unknown adapter, non-allowlisted target, unexpected target outcome, duplicate case ID or missing target execution fail closed. An empty vector directory reports zero paired executions.

**Current expected coverage:** DTF-001: **1/37 executed synthetic paired cases**. **0/37 independently maintained targets; 0/37 independent consumers.** DTF-023 and DTF-027 remain fixture-only until real semantically relevant targets are implemented and executed. This does not establish independent conformance or third-party adoption.

Vectors are experimental sidecars; the canonical failure-case schema remains v0.1.0. The allowlist must be reviewed when adding an adapter. This runner does not permit arbitrary executable paths or shell invocation.

## Machine-readable vector contract

`schemas/conformance-vector.schema.json` defines the experimental v0.1.0 vector envelope using JSON Schema Draft 2020-12. The runner validates this contract **before** resolving cases or launching any subprocess. The schema constrains the adapter and target paths to the current synthetic reference implementation; the runner also rejects a pair using the same target twice and validates canonical case version and semantic verdicts. The schema is not a generic arbitrary-executable plugin interface, nor does it establish independent target provenance. The core failure-case schema is unchanged.
