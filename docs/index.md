# Digital Trust Failure Corpus

**Current repository baseline: v0.3.0 · 31 draft cases · failure-case schema v0.1.0**

Digital Trust Failure Corpus (DTFC) is a machine-readable corpus of failure conditions, adversarial configurations, invalid trust propositions, and expected safe outcomes for digital trust systems.

The corpus provides reusable failure propositions, evidence requirements, and falsification criteria for conformance, assurance, interoperability, governance, and resilient trust infrastructure.

> **The corpus is evidence, not authority.** A case may cite specifications, governance frameworks, implementations, papers, or incidents, but inclusion in DTFC does not make the case itself normative.

## Start here

- [Browse the complete corpus](corpus/index.md)
- [Understand the taxonomy](taxonomy.md)
- [Consume DTFC safely](consuming-the-corpus.md)
- [Author a case](authoring-cases.md)
- [Validate the repository](validation.md)
- [Read the v0.3.0 release notes](release-notes-v0.3.0.md)

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

The [catalogue](corpus/index.md) and individual case pages are generated directly from the committed JSON corpus during the documentation build. They are rendered views, not a second source of truth.

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
