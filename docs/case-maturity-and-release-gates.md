# Case maturity and release-readiness gates (experimental)

This is a non-normative assessment method for [roadmap #21](https://github.com/qbf-consulting/digital-trust-failure-corpus/issues/21), not a revision to the v0.1 case schema. Case status is not certification, legal authority, or a claim of external adoption.

## Case maturity

- **Draft**: the proposition, trigger, safe dispositions, evidence requirements and falsification are present and schema-valid. This is the default for all cases.
- **Review candidate**: an independent reviewer has examined semantic novelty, provenance, scope and the distinction between an actual observation and a hypothetical scenario; reviewer identity and dated findings are recorded.
- **Evidence-supported**: a replayable failure/negative test and safe comparison are captured with versioned inputs, expected oracle, observed outputs, hashes and provenance; inconclusive runs cannot count as successful evidence.
- **Externally exercised**: an independently maintained consumer executes a documented binding against its own independently governed target or policy; its maintainer or a third-party verifier can reproduce the run. Running an external engine with DTFC-maintained policy is **not** this level.
- **Stable**: two independent reviews, stable falsification/disposition semantics, resolved major ambiguity and versioned change history support a promotion decision. Stable does not mean normative or certified.

These are **ordered evidence gates**, not an additive score. A case cannot skip a missing prerequisite. Maturity is an external review record until repeated adopter demand justifies a schema change.

## Experimental application: DTF-001

| Gate | Evidence | Finding |
|---|---|---|
| Draft | Canonical DTF-001 validates and prohibits PASS under revoked authority | Met |
| Review candidate | Informative CWE-863 mapping and external-source research; no independent semantic review attested | Not established |
| Evidence-supported | PR #49 executes paired safe and defective Rego policies with the same synthetic revoked-authority input on hash-verified OPA v1.9.0 | **Partial:** reproducible synthetic engine evidence; not independently authenticated authority state |
| Externally exercised | OPA engine maintained externally, but Rego policies and fixture authored within DTFC | Not established |
| Stable | Independent reviews and longitudinal version evidence not recorded | Not established |

**Current maturity decision: Draft.** Passing CI and use of an external executable do not automatically advance a case. Record missing evidence rather than upgrading its status.

## Schema/taxonomy pressure disposition

Existing cases DTF-001–037, source crosswalk #50 and tool-output review #52 have not demonstrated a repeated need to change the canonical schema. Portable binding and execution-result schemas accommodate adapter-specific data without changing the core case. **Decision: no core schema or taxonomy revision.** Revisit only on concrete repeated evidence that cannot be represented by existing fields.

## Release-readiness decision

Corpus validation, documentation and experimental OPA execution are valuable, but do not establish independent third-party DTFC consumption. #45/#48 remain open; #54 record-level external-source comparison is not yet complete. **Decision: do not cut a release on the strength of this review.** A release may be considered after the roadmap owner explicitly assesses provenance, independently exercised use, documentation, test stability and unresolved issues.

## Research acceptance boundary

The source-level crosswalk is not an exhaustive record-by-record review of AVID, ATLAS or W3C assertions. A claim of all-37-case overlap review requires recording each source/case judgment and reviewing the actual proposition, trigger, evidence and falsification, not just category matches. Issue #54 owns that work.
