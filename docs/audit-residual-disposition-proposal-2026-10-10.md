# Audit #60: proposed residual-risk disposition register

**Date:** 2026-10-10  
**Purpose:** A bounded decision record for an **experimental development release**. This document is a **proposal**, not evidence that the maintainer accepted the risks, not release approval, and not a maturity certification.

## Findings and proposed decisions

| Finding | Established control | Remaining uncertainty | Proposed disposition | Required follow-up |
|---|---|---|---|---|
| H1/L8, M1–M3, L1/L2, M6 | Global PASS invariant, navigation and generated links, taxonomy reporting, tests | No outstanding finding evidenced | **Resolved within engineering scope** | Recheck CI on release candidate SHA |
| H2/M7/M8 | Versioned vectors, local integrity checks, three DTFC-authored paired subprocess scenarios | 34 cases lack executed paired scenarios; no independent target/consumer | **Bounded engineering resolved; maturity deferred** | #48 and #45 remain open; state 3/37 and 0/0 prominently |
| H3 | Manual single-maintainer publication, environment branch restriction, explicit mode, exact-SHA guards, read-only negative diagnostic | No deliberately unauthorized dispatch of protected publishing workflow | **Accepted residual under #62**, owner-approved 2026-10-10 | Reconfirm environment and run exact-SHA gates before publication |
| M9 | SHA-pinned Actions and regression, Dependabot, digest-checked OPA binary; direct `jsonschema==4.26.0` and `mkdocs==1.6.1` pins | Transitive Python dependencies are not hash-locked or independently verified | **Propose time-bounded acceptance for experimental scope**, not resolved | Track authentic hash-locked closure; prohibit claims of full reproducible supply-chain integrity |
| M4/M5 | URL syntax and inspected-record metadata checks; conservative source locator classification; advisory quality checklist | External source contents, author/revision and independent semantic quality not authenticated | **Propose scoped acceptance**, treating mappings as informative research only | Keep source provenance research open; no verified-source or equivalence claims |
| L3/L4 | Local JSON schema ID syntax and uniqueness tests; research sidecar schemas | Public resolution of canonical schema `$id` URL not demonstrated | **Propose scoped acceptance** while using checked-in schemas for validation | Verify public identifier resolution; do not advertise it as a working schema retrieval endpoint |
| L5 | `licensing/artifact-license-policy.json` distinguishes content CC-BY-4.0 and code/data Apache-2.0; license files present | No independent legal review or complete copied-content provenance clearance | **Propose scoped acceptance** subject to no new unverified third-party copied material | Review provenance and licensing on intake; do not claim legal clearance |
| L6 | `SECURITY.md` provides private-reporting preference and contact `ask@qbfconsulting.digital` with minimal initial disclosure | GitHub private vulnerability reporting enablement not independently verified; mailbox not end-to-end encrypted | **Propose scoped acceptance** for public experimental repo | Admin to verify private reporting; keep confidential material out of first email |
| L7 | Version and release process documented; historical v0.4.0 distinguished from prospective release | Full independent review of release commands/codename rationale not evidenced | **Propose scoped acceptance** conditional on exact-SHA preflight | Verify release instructions and naming in release preparation, without changing historical tags |

## Risk acceptance boundary

The proposals for M9, M4/M5, L3/L4 and L5/L6/L7 **require explicit maintainer approval**. Recording or merging this register does not grant it. The H3 residual is separately accepted in #62; do not extend that approval to other findings.

An accepted risk remains **open as a factual limitation**. The decision would permit release *preparation* for an experimental, draft-status corpus, not represent remediation, certification, external adoption, stable maturity, or permission to publish.

Independent target semantics (#48) and independently operated consumer replay (#45) remain separate evidence gates. The corpus has **37 draft cases**, **3 DTFC-authored paired executions**, **zero independent target semantics** and **zero independent consumer replays**.

## Required gate before release preparation

1. Record the maintainer's explicit acceptance or rejection **by finding group** in #60; retain any rejected finding as a blocker with owner and remediation action.
2. Recheck exact intended `main` SHA, validation, documentation and relevant security checks; verify `release-publication` settings still match the evidenced single-maintainer model.
3. Confirm release documentation preserves the maturity and provenance limitations.
4. Make a **separate explicit decision** before version selection, release notes, tag creation or publication.

**Current decision:** pending maintainer disposition; #60 remains open.
