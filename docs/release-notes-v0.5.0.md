# Digital Trust Failure Corpus v0.5.0 — Experimental assurance engineering release

## Release designation and purpose

**Status: experimental development release.** v0.5.0 consolidates the post-v0.4.0 audit remediation, executable evidence scaffolding, provenance controls, documentation improvements and protected single-maintainer release governance. This is an engineering and reproducibility increment, **not** a new corpus case tranche, stable conformance standard, independent certification, or production-readiness declaration.

The corpus retains **37 draft cases** and the existing canonical **case schema v0.1.0**. Version 0.5.0 denotes the repository release, not a promotion of the case schema or the individual cases.

## Changes since v0.4.0

### 1. Corpus safety invariants and validation

- Enforced the corpus-wide invariant that a prohibited failure proposition cannot be classified as `PASS`, including cases from newly introduced families.
- Added regression and negative-probe coverage for this invariant without changing the existing canonical case schema.
- Strengthened structural crosswalk, research metadata, source URL parsing and schema identifier validation; these checks establish local format and consistency, **not** truth or continued availability of external sources.
- Added a case-quality review checklist to guide human assessment of falsifiability, evidence, provenance and potentially misleading inference.

### 2. Executable conformance evidence, explicitly bounded

- Added versioned positive/negative conformance vectors, schema validation and fail-closed integrity checks for execution evidence.
- Added a subprocess-based runner and worked `SATISFIED`/`VIOLATED` evidence examples.
- Added Git-blob revision pinning for relevant source material and tamper-detection negative probes.
- **Actual executed paired scenarios: 3 of 37 cases**, using DTFC-authored synthetic fixtures/policies. The other 34 cases do not have paired executed evidence.
- **Independent target semantics: zero. Independently operated consumer replays: zero.** An external executable such as OPA does not make a DTFC-authored policy an independently maintained target. The separate evidence gates remain [#48](https://github.com/qbf-consulting/digital-trust-failure-corpus/issues/48) and [#45](https://github.com/qbf-consulting/digital-trust-failure-corpus/issues/45).

This evidence demonstrates a bounded runner and integrity contract; it does **not** validate universal corpus semantics, cross-implementation interoperability, or external adoption.

### 3. Provenance and research handling

- Added conservative provenance classification and URL-format inspection, with explicit limits on what metadata checks can establish.
- Added research sidecar schemas and offline schema identifier stability checks.
- Improved auditability of source references without claiming that mutable URLs, source content, source revisions or third-party semantic interpretations were independently verified.
- Retained technology-neutral, falsifiable failure propositions; case provenance is research context, not automatic normative authority.

### 4. Supply-chain and workflow hardening

- Pinned GitHub Actions dependencies to immutable commit identifiers; added regression checks to prevent reintroduction of mutable references.
- Added Dependabot monitoring for GitHub Actions and Python dependencies.
- Preserved the integrity-checked OPA binary path for bounded executable checks.
- **Residual:** transitive Python package dependencies are not locked with authentic distribution hashes. Direct pins and monitoring do not constitute a fully reproducible or independently attested supply chain.

### 5. Release governance and security posture

- Changed publication to a manual, single-maintainer workflow rather than a push-triggered release request.
- Added an explicit authorized-actor check, `main` branch requirement, `release-publication` environment mode, exact-checkout input validation, duplicate-tag rejection and read-only negative preflight.
- The maintainer supplied administrator-visible configuration evidence of `main`-only environment restriction and `RELEASE_AUTHORIZATION_MODE=single-maintainer`.
- **Residual:** no intentionally unauthorized live dispatch against the protected publishing workflow was conducted. The maintainer explicitly accepted this bounded risk in [#62](https://github.com/qbf-consulting/digital-trust-failure-corpus/issues/62). No independent approval is claimed.
- Clarified the security reporting contact and restrictions on publishing confidential incident material.

### 6. Documentation and audit trail

- Repaired source-view and generated documentation navigation, standardized the README's maturity and execution counts, and added strict documentation/navigation checks.
- Added prepublication assurance checkpoints, case-quality review guidance, and an audit residual disposition register.
- The [third-party audit remediation issue #60](https://github.com/qbf-consulting/digital-trust-failure-corpus/issues/60) was closed after bounded engineering remediation and **explicit maintainer acceptance** of the remaining risks. Closure does not mean every risk was eliminated.

## Residual risks explicitly accepted for this experimental scope

The maintainer's 2026-10-10 decisions in [#60](https://github.com/qbf-consulting/digital-trust-failure-corpus/issues/60) and [#62](https://github.com/qbf-consulting/digital-trust-failure-corpus/issues/62) permit an experimental development-release scope while retaining these limitations:

| Finding | Residual limitation |
|---|---|
| H2/M7/M8 | 3/37 synthetic paired executions; no independent target or consumer |
| H3 | Protected publication has no live unauthorized-dispatch negative test |
| M9 | Transitive Python dependencies are not hash-locked |
| M4/M5 | External source contents, revisions and semantic quality not independently authenticated |
| L3/L4 | Public resolution of schema `$id` identifiers not independently demonstrated |
| L5 | No independent legal clearance for all provenance/licensing claims |
| L6 | GitHub private vulnerability reporting enablement not independently confirmed; contact mailbox is a routing channel |
| L7 | Independent verification of all release instructions and codename rationale not established |

These are **accepted limitations**, not test passes, waivers for future stable releases, or endorsements by external parties.

## Compatibility and migration

- **Repository:** v0.5.0 follows v0.4.0.
- **Case count:** 37 draft cases; no new cases asserted by this release.
- **Canonical failure-case schema:** v0.1.0 unchanged.
- **Consumer expectations:** existing case-schema consumers should not require a schema migration merely because the repository version changes. New executable vector and research sidecar artifacts are additional experimental surfaces; consumers must validate against their respective checked-in schemas and must not treat these as independently verified conformance claims.
- **Security/privacy:** do not add private incident details or sensitive verification transcripts to the public corpus.

## Reproduce repository checks

From the tagged checkout with Python available:

```bash
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python tools/validate.py
```

Use the repository's documented executable-evidence examples for the bounded paired-runner demonstration. These commands validate repository-level invariants and local fixtures; they do not verify external URLs, external policies, independent consumers or production deployments.

## Operational and governance follow-up

- [#48](https://github.com/qbf-consulting/digital-trust-failure-corpus/issues/48): obtain genuinely independent target decision semantics and paired adverse-condition evidence.
- [#45](https://github.com/qbf-consulting/digital-trust-failure-corpus/issues/45): obtain independently operated consumer replay, including negative and unavailable outcomes.
- Close the remaining provenance, schema retrieval, supply-chain integrity and security administration evidence gaps before making stronger assurance claims.
- Reassess risk acceptance and release protection before any subsequent stable or materially expanded release.

## Release interpretation

**What v0.5.0 establishes:** a better validated, documented and partially executable *experimental* corpus with a traceable audit and release-control decision trail.

**What v0.5.0 does not establish:** 37 executable conformance tests; independent implementations; external source authentication; comprehensive dependency integrity; legal certification; independent approval; or suitability as a production trust decision authority.

See the repository's case quality guidance, release safety preflight, prepublication assurance checkpoint and audit disposition register for the underlying boundaries.
