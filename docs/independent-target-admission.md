# Independent target admission and execution record

This is a **submission contract**, not evidence that an independent target exists. It supports [#48](https://github.com/qbf-consulting/digital-trust-failure-corpus/issues/48) and the paired-vector work in #63.

## Admission requirements

An independently maintained target must have an identifiable maintainer or organization **outside this repository's synthetic target implementation**. A fork, vendored copy, or renamed DTFC example is not sufficient. Record the public upstream repository URL, immutable commit SHA (or immutable artifact digest), version/tag if present, license, target maintainer, test operator and the relationship between them. Record how the exact revision was acquired and independently reproduced. Do not include secrets, personal information or confidential test transcripts.

Specify the API/CLI invocation, runtime, dependencies, configuration, clock and policy snapshot. Preserve the same canonical DTF case ID/version/digest and the **identical adverse request bytes** for safe and defective paths. If two genuinely different builds/configurations of the same independent target are used, pin both and explain their provenance. A repository-maintained stub or simulated return value cannot substitute for actual target execution.

## Required result record

| Field | Requirement |
|---|---|
| Case | Canonical case ID, version, SHA-256 and exact proposition/falsification boundary |
| Target | Upstream repository, maintainer, immutable revision or digest, license |
| Environment | Runtime, dependency versions, configuration/policy snapshot, clock |
| Request | Raw or privacy-safe reproducible request, SHA-256, identical input for both paths |
| Safe execution | Exact command/API call, raw response, exit status, response digest, trace reference |
| Defective execution | Exact command/API call, raw response, exit status, response digest, trace reference |
| Evaluation | Per-path disposition, independent oracle rationale, observed falsification result |
| Reproduction | Operator, timestamp, clean-room instructions, rerun results, known limitations |
| Independence | Maintainer/operator relationship, DTFC-derived code exclusions, reviewer disposition |

A passing execution is not automatically a complete assurance finding. If the target cannot be pinned, if its decision trace cannot be obtained, or if the two paths do not exercise the same proposition and adverse request, classify the result **INDETERMINATE / evidence incomplete**, not as independent conformance.

## Promotion gate

1. Open an issue identifying the candidate target and its licensing/availability before modifying canonical cases.
2. Capture a pinned, reproducible pair of *actual* target invocations with raw responses and digests.
3. Add an adapter and a versioned vector with negative tests that fail on incorrect target behavior, stale revisions, mismatched requests and missing traces.
4. Obtain independent review of target identity, case interpretation and reproducibility. Keep source-identity and review evidence separately auditable.
5. Only then update independent-target coverage counts. Independently maintained **consumer** adoption is a distinct requirement tracked in #45 and must not be inferred from target execution.

**Current evidence boundary (2026-10-10):** one DTF-001 executed synthetic paired target; zero independently maintained targets and zero independent consumers. The DTF-023/027 fixtures do not increase executed target coverage.
