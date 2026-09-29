# Changelog

## Unreleased

Privacy and correlation failure expansion.

### Added

- Six draft privacy/correlation cases, DTF-032 through DTF-037, covering proof-mechanism correlation, status-query observability, post-presentation purpose overrun, authoritative-participant unlinkability failure, disclosure aggregation, and verification-artefact retention concentration.
- Dedicated regression coverage for the tranche.
- Modeling observations that preserve the W3C VC Data Model Threat Model v2.1 as research provenance while keeping DTF technology-neutral and non-normative.

### Assurance and compatibility

- The failure-case JSON Schema remains **v0.1.0**; all six cases fit the existing contract and taxonomy.
- The corpus is contiguous from DTF-001 through DTF-037 in current development.
- No new failure-class enum was introduced: existing `correlation`, `policy-mismatch`, and `provenance` semantics are sufficient for this tranche.
- Cryptographic or local verification success does not establish privacy safety for the composed transaction.

## 0.3.0 — 2026-09-28

Cross-specification seam and decision-resolution expansion.

### Added

- Eight cross-specification seam cases, DTF-020 through DTF-027, covering semantic ownership ambiguity, cross-stage lifecycle reuse, context-binding/execution substitution, component/composition validity substitution, quorum independence, provenance depth, selective evidence completeness, and workflow/assurance substitution.
- Four decision-resolution cases, DTF-028 through DTF-031, covering authority laundering, decision-basis misattribution, silent unresolved-condition clearance, and false persistence after valid resolution.
- Dedicated regression suites for the cross-specification and decision-resolution tranches.
- Decision-resolution judgment documentation with explicit cross-repository authority boundaries and read-only upstream research provenance.

### Assurance and compatibility

- The failure-case JSON Schema remains **v0.1.0**; all twelve new cases fit the existing contract and taxonomy.
- The corpus is contiguous from DTF-001 through DTF-031.
- PASS remains prohibited for each represented failure condition; DENY and INDETERMINATE remain available where evidence and policy legitimately distinguish them.
- Cross-component success, operational workflow success, repeated non-authority signals, and prior unresolved state do not silently become broader assurance or authority claims.

### Release boundary

v0.3.0 expands the failure corpus and its falsification surface without turning DTFC into a normative authority, protocol, severity scheme, or assurance certification system. External references preserve provenance and context only.

All notable changes to Digital Trust Failure Corpus are recorded here.

## 0.2.0 — 2026-09-22

Authority-at-material-commitment expansion.

### Added

- Seven draft authority failure cases, DTF-013 through DTF-019.
- Explicit failure propositions for valid-signature/authority substitution, expired mandates, iterative scope expansion, revocation during active interactions, stale or wrong-action approvals, reputation/capability substitution, and unreconstructable historical authority.
- Evidence and falsification requirements that distinguish identity, general authorization, and authority for the exact material commitment.

### Assurance and compatibility

- The failure-case JSON Schema remains **v0.1.0** because the new cases fit the existing contract without schema or taxonomy expansion.
- Case versions remain independent semantic versions; repository release version and schema version are no longer assumed to move in lockstep.
- All cases remain `draft`; inclusion remains evidence, not normative authority.
- Existing DTF-001–012 content is unchanged.

### Release boundary

v0.2.0 expands corpus coverage without changing the case contract. It does not define a negotiation protocol, legal enforceability, universal authorization policy, or severity model.

## 0.1.0 — 2026-09-15

Initial development baseline.

### Added

- Technology-neutral Digital Trust Failure Case JSON Schema v0.1.0.
- Bounded taxonomy for domains, failure classes, dispositions, and evidence categories.
- Repository-local corpus validator with duplicate ID/title detection and useful failure diagnostics.
- Positive and negative validation fixtures and executable invariant tests.
- GitHub Actions validation on pull requests and pushes to `main`.
- Dual licensing: CC-BY-4.0 for human-readable content and Apache-2.0 for executable and machine-readable artifacts.
- Twelve draft failure cases:
  - DTF-001–003: authority;
  - DTF-004–006: lifecycle;
  - DTF-007–009: composition;
  - DTF-010–012: evidence.
- Contributor, authoring, consumption, security, and provenance guidance.
- Non-normative downstream research signals for lifecycle modelling, executable governance, and trust-infrastructure observability.

### Release boundary

v0.1.0 is a reproducible development baseline, not a normative standard, severity catalogue, assurance certification, or claim of complete failure coverage. All initial cases remain `draft` and may evolve through evidence-backed review.
