# External corpus crosswalk: bounded research tranche (2026-10-09)

**Canonical machine-readable register:** [crosswalk.json](../../research/external-sources/crosswalk.json). This is a non-normative research sidecar, **not** an expansion of the 37 canonical DTFC cases or of the v0.1 failure-case schema.

## Method and scope

Compared selected external *source-level* material against the current DTFC case index and inspected DTF-001 directly. Entries are **candidate mappings** unless explicitly marked high-confidence. This is not a record-by-record exhaustive audit of AVID or ATLAS and does not imply that every existing DTFC case has been independently examined. A second pass must inspect each proposed target case's full semantics before upgrading tentative relationships to confirmed mappings.

| Source | Examined item | Existing DTFC overlap | Disposition |
|---|---|---|---|
| [MITRE CWE](https://cwe.mitre.org/data/definitions/863.html) | CWE-863 Incorrect Authorization | DTF-001 (verified), DTF-002 (candidate) | Cross-reference: no new case |
| [MITRE CWE](https://cwe.mitre.org/data/definitions/841.html) | CWE-841 Improper Enforcement of Behavioral Workflow | DTF-017 / DTF-026 (candidates) | Further overlap review |
| [MITRE ATLAS](https://atlas.mitre.org/techniques/AML.T0051) | AML.T0051 Prompt Injection | DTF-002 / DTF-028 (candidates) | Coverage-gap hypothesis |
| [W3C VC 2.0 suite](https://github.com/w3c/vc-data-model-2.0-test-suite) | Executable issuer/verifier interoperability harness | DTF-010 / DTF-025 (candidates) | Test-adapter pattern, not case import |
| [AVID](https://avidml.org/database/) | Report and vulnerability record model | No case-level mapping established | Provenance-method reference |

## Findings and decisions

**1. CWE-863 / DTF-001: high-confidence overlap.** DTF-001 specifically prohibits relying on pre-revocation authority evidence for a current authorization decision. CWE-863 provides a general software weakness classification for incorrect authorization. The CWE classification is *broader* and does not supply the temporal and provenance facts required by DTF-001. Add a link to the canonical DTF-001 references, with a note that the mapping is informative and not an external validation.

**2. CWE-841: not yet a new case.** Workflow order, skipped actions and timing are relevant to digital trust. The current case index already includes commitment, scope, approval, and workflow/assurance boundaries. A new case is justified only if the missing ordered-workflow proposition cannot be represented by these cases.

**3. ATLAS AML.T0051: attack technique is not a trust failure verdict.** A prompt injection may be an input to an unauthorized action. To become a DTFC case, the evaluation must demonstrate a specific authority boundary crossed, with actor, action, permitted scope, governing policy, and observed decision. A technique label alone cannot establish a failure.

**4. W3C VC 2.0: executable test design is useful but has different semantics.** The suite runs tests against issuer/verifier endpoints, with implementation registration and supported proof suites. A passing interoperability test does not by itself establish current authority, evidentiary sufficiency, or privacy. Reuse the adapter concept, not the upstream test code or claims of conformance.

**5. AVID: retain evidence provenance distinctions.** AVID separates concrete reports from recurring vulnerabilities. DTFC should preserve that distinction in research evidence: a report is not automatically a generalizable, falsifiable case.

## Adoption boundaries

- Do **not** bulk import external records or copy upstream test fixtures, code, or prose. External rights and attribution must be evaluated per artifact before reuse.
- Research references do not make DTFC normative or confer an assurance result.
- Canonical case schema and taxonomy remain unchanged; this register is deliberately a separate artifact.
- Proposed follow-up: validate tentative case mappings against each complete case, select one genuinely novel failure proposition only if a gap survives overlap analysis, then build paired negative/positive executable scenarios with provenance.

## Evidence limits

This tranche contains a source-level crosswalk and one case-level mapping, not a completed exhaustive 37-case review. Source URLs are provided for independent inspection; links are not evidence that external projects have adopted DTFC.
