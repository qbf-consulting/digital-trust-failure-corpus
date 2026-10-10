# Versioned subprocess conformance vectors

The experimental vector runner reads `conformance/vectors/DTF-*.json` and invokes **allowlisted** local Python subprocess targets, using the same JSON request for safe and defective paths.

```bash
python -m tools.run_conformance
python -m unittest tests.test_conformance_vectors
```

Each result records canonical case version and digest, target source SHA-256, raw response, request/response SHA-256, disposition, test verdict and replay command. The summary computes the canonical case denominator from `corpus/` rather than a hard-coded 37. Missing request, mismatched case version, unknown adapter, non-allowlisted target, unexpected target outcome, duplicate case ID or missing target execution fail closed. An empty vector directory reports zero paired executions.

**Current expected coverage:** DTF-001, DTF-023 and DTF-027: **3/37 executed synthetic paired cases**. **0/37 independently maintained targets; 0/37 independent consumers.** DTF-023 and DTF-027 now use local subprocesses implementing bounded synthetic safe and intentionally defective decision semantics. These remain DTFC-authored test targets, not independently maintained policy applications. This does not establish independent conformance or third-party adoption.

Vectors are experimental sidecars; the canonical failure-case schema remains v0.1.0. The allowlist must be reviewed when adding an adapter. This runner does not permit arbitrary executable paths or shell invocation.

## Machine-readable vector contract

`schemas/conformance-vector.schema.json` defines the experimental v0.2.0 vector envelope using JSON Schema Draft 2020-12. The runner validates this contract **before** resolving cases or launching any subprocess. The schema constrains the adapter and target paths to the current synthetic reference implementation; the runner also rejects a pair using the same target twice and validates canonical case version and semantic verdicts. The schema is not a generic arbitrary-executable plugin interface, nor does it establish independent target provenance. The core failure-case schema is unchanged.

The subprocess runner rejects missing/symlink targets, target launch failures, timeouts and any change in target file SHA-256 observed before versus after execution. This is **local file-integrity checking**, not authenticated upstream provenance or a guarantee against all time-of-check/time-of-use races. Independent target revision pinning remains outstanding.

## Worked paired evidence: DTF-023 and DTF-027

These examples are reproducible using `python -m tools.run_conformance` from a checked-out repository with development dependencies installed. Inspect `results[]` by `case_id` and `outcomes.safe` / `outcomes.defective` in the generated JSON. Every example invokes two **local Python processes**, not a supplied fixture verdict.

| Case | Identical adverse input | Safe observed disposition | Defective observed disposition | Harness verdicts |
|---|---|---|---|---|
| DTF-023 | Both components PASS, seam obligation unevaluated | INDETERMINATE | PASS | SATISFIED / VIOLATED |
| DTF-027 | Workflow success, substantive evidence missing | INDETERMINATE | PASS | SATISFIED / VIOLATED |

For DTF-023, the safe target declines to infer composition assurance from two component-level successes. For DTF-027, the safe target declines to infer substantive assurance from successful workflow completion. The defective targets deliberately conflate the corresponding propositions. These are **test verdicts about the case invariant**, not certification or a claim that the broader system is assured.

The JSON result includes `request_sha256`, `response_sha256`, `target_sha256`, `raw_response`, `replay_command`, and the canonical `case_sha256`. To replay a target manually, pipe the vector's `request` JSON into its corresponding Python script and compare the raw JSON disposition. The hashes are calculated locally; they do not authenticate an external developer, immutable upstream revision, or independent operator. Source-control revision and run timestamp must be captured separately by any evidence collector asserting historical provenance. An unavailable, malformed, timed-out, or semantically inconsistent target raises an error and is **not counted as SATISFIED**. A valid INDETERMINATE disposition is allowed only where the canonical case permits it.

## Pinned local target revisions (vector v0.2.0)

Each v0.2.0 vector now requires a `target_git_blob_sha1` object with predeclared `safe` and `defective` Git blob object IDs. Before invoking a subprocess, the runner computes the Git blob hash of the target's source bytes and rejects any mismatch. This supplements the independently reported SHA-256 of the source and the before/after execution integrity check. Tests reject missing pins, malformed pins and a tampered digest before any subprocess launches.

The pinned IDs correspond to Git objects in the repository and can be verified using `git hash-object examples/independent-consumer/<target>.py` on a trusted checkout. Git's SHA-1 object identifiers are used for repository compatibility; they are not a modern cryptographic signature and do not authenticate who authored the target. The pin itself is repository-maintained and can be altered in a coordinated change to vector and target. Use trusted commit/release signatures or externally attested source manifests for stronger historical provenance. The runner remains synthetic-only and cannot claim independent target or consumer evidence.
