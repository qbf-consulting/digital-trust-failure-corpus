# Evidence-gated execution tranche (2026-10-10)

Status: **execution baseline, not a conformance claim**. Tracks #62, #63, #48, #45, #43, #60 and #21. Canonical 37-case corpus and schema 0.1.0 are unchanged. No release is authorized by this document.

## Dependency and closure matrix

| Gate | Issue | Deliverable | Required independent evidence | Stop condition |
| --- | --- | --- | --- | --- |
| G0 | #62 | Protected release environment, branch restrictions, approval enforcement, exact-SHA validation and negative publication tests | GitHub settings inspection and recorded test outcomes | Unverified required reviewers, branch restrictions or attestation; do not publish |
| G1 | #63 | Generic target-execution binding, adapter protocol, paired safe/unsafe oracle, reproducible coverage report | Raw target input/output, version, source digest, replay commands and result digest | Fixture-only results or unknown adapter cannot count as target execution |
| G2 | #48 | Semantically appropriate independently maintained target | Target repository, license, pinned revision, real API/CLI invocation | No equivalent failure condition: report non-applicability |
| G3 | #45 | Independent executable consumer evidence | Same adverse input under safe and defective decisions, independently reproducible run | Local author-provided observation alone is insufficient |
| G4 | #43 | Reconcile three-case portable-binding acceptance | Tests and docs; explicit unsupported cases and evidence boundaries | Do not close until remaining executable-scenario criterion is met |
| G5 | #60 | Audit remediation with finding-by-finding disposition | Exact green CI SHA, negative probes and source-specific evidence | Do not mark findings resolved from documentation alone |
| G6 | #21 | Roadmap reconciliation and release-readiness decision | Cross-links to G0–G5 and independent maturity review | No new release merely because the issue queue is smaller |

## Execution invariants

1. A target's authorization `PASS` is not the harness's success verdict. An unsafe `PASS` for an adverse DTF condition is a violation.
2. Separate `author-supplied-fixture`, `executed-synthetic-target`, `independently-maintained-target`, and `independent-DTFC-consumer` provenance. These are not interchangeable.
3. Missing inputs, unrecognized adapters, invalid digests, unavailable targets, unsupported case semantics, or malformed output must never become SATISFIED.
4. A paired vector must hold the adverse condition and material inputs constant; change only the safe/defective decision behaviour under examination.
5. Canonical case digests and target version/revision must be pinned. Raw inputs, raw outputs, tool versions, UTC execution time, hashes, and replay commands are required for executed evidence.
6. Publish both fixture-paired and **actually executed paired** coverage using the canonical 37-case denominator. No synthetic inflation.
7. No schema change without concrete pressure, compatibility review and negative tests.
8. No new case merely to increase the count; no maturity promotion without independent evidence.
9. No private incident material, customer data, or confidential third-party review content.

## Implementation sequence

### A. Release controls (#62)
Configure and verify GitHub environment required reviewers and deployment restrictions; enforce review of release-critical changes. Verify no push-based publication path; check unauthorized actor, absent approval, wrong branch, stale SHA, missing notes and existing tag. Record repository settings and results in a PR. This step requires actual GitHub administration and cannot be satisfied by adding YAML alone.

### B. Executable runner (#63)
Specify additive vector/result contracts and a versioned adapter interface. Runner invokes target (never accepts an observed value as execution evidence), captures raw request/response and hashes, applies case-specific oracle, and emits deterministic coverage. Preserve legacy v0.1 and portable fixture v0.2 consumers. Start with DTF-001, then DTF-023 and DTF-027 only if real semantic targets exist. Add positive, negative, tamper, unknown-adapter, unavailable-target, stale-version and malformed-output tests.

### C. External target and consumer (#48, #45, #43)
Select target on semantic fit rather than convenience. Pin external implementation revision and license; demonstrate actual invocation with identical adverse input for safe and defective decisions. Document target-maintainer independence separately from DTFC-consumer independence. Obtain external reproduction/review if possible; otherwise leave the independent-adoption gate open.

### D. Audit remediation (#60)
Three bounded PRs: (1) README, navigation and reproduction commands; (2) provenance classification, source pinning, taxonomy coverage and nonblocking evidence-quality diagnostics; (3) Action SHA pins, dependency/security/licensing/research-schema hygiene. Mark each finding confirmed, partially confirmed, superseded, unverified or resolved with evidence; never rewrite historical releases.

### E. Readiness (#21)
Close subordinate issues only when their actual acceptance checks are satisfied. Publish an evidence-qualified worked example, then perform a separate readiness decision. Preserve the v0.4.0 historical publication; do not cut a new release as part of audit cleanup.

## Baseline as verified in issue and PR history

- 37 draft cases; schema 0.1.0; v0.4.0 published.
- PR #65: opt-in portable fixture v0.2, three fixture-only paired cases, zero actual target executions through its generic fixture runner.
- PR #49: separate OPA v1.9.0 synthetic-engine experiment, not independent adoption.
- PR #64: protected manual release workflow logic merged, but environment reviewer settings and exact-SHA independent attestation remain unverified.
- PR #61: corpus-wide unsafe PASS invariant and navigation fixes merged.

**Completion rule:** a checkbox or issue closure is not evidence. Every gate requires a reproducible artifact and verification of its stated stop conditions.
