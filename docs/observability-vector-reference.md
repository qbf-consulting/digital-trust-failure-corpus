# Observability synthetic vectors: canonical reference

**Status:** experimental, author-supplied synthetic evidence. **Source of truth:** `research/observability/synthetic-vectors-v1.json`. **Consumer:** RAHP Toolkit `examples/observability-dtfc/synthetic-vectors-v1.json`.

## Purpose and boundary

These vectors test the behavior of `tools/observability_harm.py` when operational telemetry might create cross-context linkability or be misused as decision authority. They are not canonical DTFC failure-case records, observed incidents, independently verified target outputs, normative RAHP assessments, or privacy certifications. The vectors do not create a new taxonomy or change the corpus schema. See [original examination](observability-induced-harm.md).

## Contract and propositions

The JSON contract identifier is `dtfc-observability-synthetic-vectors/v1`. Every vector contains an identifier, proposition, synthetic events and an exact expected `state`/`reason` pair. The `provenance` section explicitly marks `author-supplied-synthetic` and `deployment_evidence: false`.

| Vector | Trigger and mechanism | Expected result | Related existing case themes |
| --- | --- | --- | --- |
| OBS-NEG-01 | Reuse of a trace identifier across declared relying contexts permits a synthetic join. | `FAIL / cross-context-trace-correlation` | DTF-032, DTF-033, DTF-036, DTF-037 |
| OBS-NEG-02 | Observation marked missing: no evidence for a positive conclusion. | `INDETERMINATE / insufficient-observation-evidence` | DTF-010–012 |
| OBS-NEG-03 | A consequential suspension claims telemetry as its decision source. | `FAIL / telemetry-promoted-to-authority` | DTF-027 and assurance/workflow substitution |
| OBS-NEG-04 | One verified synthetic event has no demonstrated failure, but cannot prove safety. | `INDETERMINATE / no-failure-observed-not-proof-of-safety` | Evidence sufficiency across cases |

**Overlap disposition:** These are specific negative test propositions, not new failure-case IDs. The case associations are thematic, not a claim that all associated cases are executable through this helper.

## Evidence requirements and residual uncertainty

For real deployment assessment, independently establish the telemetry collection path, identifier derivation and reuse, context boundaries, access controls, retention/deletion and backup behavior, decision-authority chain, provenance, freshness and completeness of evidence. The fixture merely supplies asserted strings; its `evidence_state: verified` is **not** third-party verification. No target was contacted, no independent run was performed, and the helper cannot establish that correlation or authority abuse happened outside its synthetic inputs.

Do not add live relationship identifiers, tokens, credential contents, transcripts or confidential assessment records to these public vectors. The helper returns `INDETERMINATE`, never `PASS`, for absence of observed harm. It reports one reason rather than a complete multi-harm inventory.

## Reproduction

From the DTFC repository root:

```sh
python -m unittest discover -s tests -p 'test_observability_harm.py' -v
python -m unittest discover -s tests -p 'test_observability_portable_vectors.py' -v
python -m unittest discover -s tests -v
```

The tests compare exact expected states and reasons; they do not authenticate the asserted event inputs.

## Versioning and downstream consumption

The published vector file is canonical in DTFC. RAHP imports a byte-identical snapshot and checks the Git blob digest in its consumer test. A change to DTFC vectors does **not** automatically update RAHP. To revise the contract, open a bounded source change, document compatibility and rationale, validate DTFC CI, import the reviewed snapshot into RAHP, update the pinned digest and run RAHP CI. Do not silently change existing expected outcomes. An incompatible shape or semantics change requires a new contract version and explicit consumer migration.

## Traceability and release

Original DTFC [#105](https://github.com/qbf-consulting/digital-trust-failure-corpus/issues/105) / [PR #106](https://github.com/qbf-consulting/digital-trust-failure-corpus/pull/106); portable source [#107](https://github.com/qbf-consulting/digital-trust-failure-corpus/issues/107) / [PR #108](https://github.com/qbf-consulting/digital-trust-failure-corpus/pull/108). RAHP counterparts: [#981](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/981), [PR #982](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/pull/982), [#983](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/983), [PR #984](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/pull/984).

No release was required solely for these experimental changes.
