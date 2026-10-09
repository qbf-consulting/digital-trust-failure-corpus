# External-source semantic screening matrix

Tracked by [#54](https://github.com/qbf-consulting/digital-trust-failure-corpus/issues/54). The [machine-readable matrix](https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/main/research/external-sources/semantic-overlap-matrix.json) contains **111 individually explained judgments**: each of the 37 existing canonical DTF propositions screened against three externally published source records from three different source families.

| Primary source record | Source type | Direct mechanism overlap | Interpretation |
|---|---|---|---|
| [MITRE CWE-863](https://cwe.mitre.org/data/definitions/863.html) | Weakness classification | DTF-001/002/003/013–018/028 | Incorrect authorization is a broad class; DTF cases have narrower scope, lifecycle and authority conditions. |
| [W3C VC Threat Model T5](https://www.w3.org/TR/2026/DNOTE-vc-data-model-threat-model-2.1-20260927/#t5-correlation-via-status-and-revocation-lookup) | Group Note Draft threat | DTF-033 | The status-lookup observation is a direct privacy failure match. Draft is provenance only. |
| [OWASP LLM01 (2025)](https://owasp.org/www-project-top-10-for-large-language-model-applications/assets/PDF/OWASP-Top-10-for-LLMs-v2025.pdf) | Application risk category | DTF-002/018/028 | Only the unauthorized-action outcome overlaps. Other prompt-injection effects cannot automatically be treated as covered. |

Each judgment classifies the case as `mechanism-overlap`, `adjacent`, or `not-established` and includes the existing case proposition summary and the reason for its classification. These are **conservative semantic screening judgments**, not 111 executed tests or independent source-specific implementation reviews. In particular, a generic weakness or attack technique does not establish all preconditions, required evidence or falsification criteria of a DTF case.

## Findings

1. The strongest privacy match is W3C T5 to DTF-033. DTF-037 (retained verification artefacts) is adjacent but requires additional evidence; do not collapse retention into lookup observability.
2. CWE-863 is useful as a broad informative cross-reference. It does not replace the narrower authority and temporal claims in DTF-001.
3. OWASP LLM01 can instantiate DTF-028 when untrusted text is promoted to authority; prompt manipulation that does not result in an authority decision may be outside DTFC's existing proposition set.
4. No source-level label alone establishes a distinct new DTF case or a core schema change.

## Remaining acceptance gaps

This matrix screens **three source records**, not eight directly inspected individual records across three families. Earlier CWE triage lists eight preliminary records but those are not a substitute for verified multi-source record research. The full 37-case cross-product here is a reasoned *screening*, not an independent peer-reviewed examination of complete upstream evidence. Issue #54 still requires two independently demonstrated improvements, executable binding where appropriate, source rights review and an adoption handoff. #45/#48 retain independent-consumer acceptance.

## Reproduction

Run `python -m unittest tests.test_semantic_overlap_matrix` from the repository root. This verifies completeness, canonical case ID resolution, source references and judgment presence. It does not validate semantic correctness of each research conclusion.
