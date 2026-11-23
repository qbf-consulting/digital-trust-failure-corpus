# Digital Trust Failure Corpus

**Current published repository release: v0.5.0 (experimental) · 37 draft cases · failure-case schema v0.1.0**

Digital Trust Failure Corpus (DTFC) is a machine-readable corpus of failure conditions, adversarial configurations, invalid trust propositions, and expected safe outcomes for digital trust systems.

The corpus provides reusable failure propositions, evidence requirements, and falsification criteria for conformance, assurance, interoperability, governance, and resilient trust infrastructure.

> **The corpus is evidence, not authority.** A case may cite specifications, governance frameworks, implementations, papers, or incidents, but inclusion in DTFC does not make the case itself normative.

## Start here

- [Browse the complete corpus](https://qbf-consulting.github.io/digital-trust-failure-corpus/corpus/)
- [Understand the taxonomy](taxonomy.md)
- [Consume DTFC safely](consuming-the-corpus.md)
- [Author a case](authoring-cases.md)
- [Validate the repository](validation.md)
- [Read the v0.5.0 experimental release notes](release-notes-v0.5.0.md)

## Current corpus

| Range | Focus |
|---|---|
| DTF-001–003 | Authority |
| DTF-004–006 | Lifecycle |
| DTF-007–009 | Composition |
| DTF-010–012 | Evidence |
| DTF-013–019 | Authority at commitment |
| DTF-020–027 | Cross-specification seams |
| DTF-028–031 | Decision resolution |
| DTF-032–037 | Privacy and correlation |

The [catalogue](https://qbf-consulting.github.io/digital-trust-failure-corpus/corpus/) and individual case pages are generated directly from the committed JSON corpus during the documentation build. They are rendered views, not a second source of truth.

## Reproduce locally

```bash
python -m pip install -r requirements-dev.txt -r requirements-docs.txt
python -m unittest discover -s tests -v
python tools/validate.py
python tools/build_docs.py
mkdocs build --strict
```

## Authority boundary

DTFC does not define the normative semantics of external protocols, standards, governance systems, or assurance methods. Consumers remain responsible for mapping each technology-neutral failure proposition to authoritative specifications, policies, evidence sources, and implementation contexts.

Canonical project source: [GitHub repository](https://github.com/qbf-consulting/digital-trust-failure-corpus).

## Representative Trust Tasks research outcome

The [consent-family assurance study](trust-tasks-representative-consent-study.md) is the current, bounded external applicability research deliverable. It consolidates eight pinned Trust Task versions, 296 case-level author judgments and source-qualified negative/control tests. It **does not** assert a defect in the upstream task specification, independent acceptance or observed implementation failures.

The [generated Trust Tasks navigator](https://qbf-consulting.github.io/digital-trust-failure-corpus/trust-tasks/) retains the 1,391-version upstream inventory for discovery; its remaining versions are **not** a commitment to exhaustive assessment. The source-code [navigator landing page](trust-tasks/index.md) explains why the full index is generated at documentation build time.

## Version-pinned external applicability research

The [Trust Tasks crosswalk](trust-tasks-crosswalk.md) documents a bounded twelve-task screening against existing DTF cases. Its judgments are non-authoritative research and are not external target execution evidence. The upstream Trust Tasks specification remains authoritative for task behavior.
