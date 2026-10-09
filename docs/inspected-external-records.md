# Inspected external records: dispositions and two new privacy bindings

Tracked by [#54](https://github.com/qbf-consulting/digital-trust-failure-corpus/issues/54). The [eight-record register](https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/main/research/external-sources/inspected-record-dispositions.json) identifies eight individual primary-source records from MITRE CWE, the W3C VC Threat Model v2.1 Group Note Draft and OWASP LLM Top 10 (2025). The register preserves source identifiers, deep links, dates/status, case-specific judgments, rights caveats and reasons.

## Specific integration improvements

1. **DTF-032 ↔ W3C T4**: the new informative, machine-readable T4 binding isolates repeated proof/signature/key material as a correlation mechanism. This improves specificity beyond a generic threat-model reference. It does **not** prove unlinkability in a deployed system.
2. **DTF-035 ↔ W3C T18**: the new T18 binding isolates issuer-controlled issuance and renewal patterns as privacy-defeating behavior. This distinguishes authoritative participation from evidence of privacy assurance. It does **not** assert issuer misconduct in a real deployment.

Both mappings are separate portable research records; the canonical schema and case maturity remain unchanged. The validation test enforces unique source identifiers, exact case references and the two specific bindings. The improvement is **source precision and machine-consumable provenance**, not newly executed external tests.

## Negative findings

- CWE-862 (missing authorization) is not automatically DTF-002 (overscoped delegated authority).
- W3C T10's stable identifier can correlate without composition; DTF-036 requires compositional inference.
- OWASP LLM01 is only a DTF-028 authority case when untrusted text is actually promoted to consequential authority.
- OWASP LLM02 is broader than post-presentation purpose misuse in DTF-034.

## Evidence and licensing limits

The sources were inspected at their publicly accessible primary pages. The W3C document is a **Group Note Draft** and not an endorsed standard. The register uses source IDs, URLs and original DTFC paraphrases, not copied payloads or upstream prose. Reuse licensing for any future redistribution of external content must be checked separately.

The earlier [three-source matrix](external-semantic-screening.md) covers all 37 canonical cases for three selected records; this new eight-record sample adds direct inspection and candidate dispositions, **not** 8 × 37 full semantic judgments. CI verifies structure and references, not independent technical correctness. Independent DTFC adoption remains tracked in #45/#48.

## Complete screening matrix

The [eight-record coverage matrix](https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/main/research/external-sources/eight-record-coverage-matrix.json) records 296 conservative judgments (eight source records × 37 canonical cases), including explicit negative findings. The unit is a source-to-case *screening judgment*, not an executable conformance result or independently peer-reviewed semantic equivalence. `python -m unittest tests.test_eight_record_coverage` checks structural completeness. The record links were carried forward from the earlier inspected register; they were not independently re-fetched in this matrix increment. No independent adoption or release-readiness inference follows.
