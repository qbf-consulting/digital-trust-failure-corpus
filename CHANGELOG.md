# Changelog

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
