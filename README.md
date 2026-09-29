# Digital Trust Failure Corpus

A machine-readable corpus of failure conditions, adversarial configurations, invalid trust propositions, and expected safe outcomes for digital trust systems.

The project provides reusable failure cases, evidence requirements, and falsification criteria for conformance, assurance, interoperability, governance, and resilient trust infrastructure.

## Status

Current development baseline: **v0.4.0**. See [`VERSION`](VERSION), [`CHANGELOG.md`](CHANGELOG.md), and the [`v0.4.0 release notes`](docs/release-notes-v0.4.0.md).

v0.4.0 retains the v0.1.0 failure-case schema and contains thirty-seven draft cases, adding the privacy/correlation tranche to the previously released cross-specification seam and decision-resolution work. Repository release version, schema version, and case version are distinct lifecycle dimensions.

The corpus is **evidence, not authority**. A case can cite normative specifications, governance frameworks, implementations, papers, or incidents, but inclusion here does not make the case itself normative.

## Documentation site

The rendered documentation and generated corpus catalogue are published through GitHub Pages:

**https://qbf-consulting.github.io/digital-trust-failure-corpus/**

The Pages site is a presentation layer over this repository. Individual case pages are generated directly from the canonical JSON under `corpus/` during the documentation build; the rendered site does not become a second source of truth.

## Core design principles

- Failure propositions should be falsifiable.
- Missing, stale, conflicting, or unverifiable evidence must not silently become success.
- The core model remains independent of any single DID method, credential format, registry protocol, assurance methodology, or agent architecture.
- Consumers may have legitimate policy differences; a case can therefore permit more than one safe disposition.
- Taxonomy and schema evolution should be driven by concrete cases rather than speculative completeness.

## Repository structure

```text
schemas/                     Versioned machine-readable case contract
corpus/authority/            DTF-001–003, DTF-013–019, DTF-028
corpus/lifecycle/            DTF-004–006 and DTF-031
corpus/composition/          DTF-007–009 and DTF-020–024
corpus/evidence/             DTF-010–012, DTF-025–027, DTF-029–030
corpus/privacy/              DTF-032–037
docs/taxonomy.md             Classification vocabulary
docs/authoring-cases.md      Case authoring guidance
docs/consuming-the-corpus.md Adopter guidance
docs/*-observations.md       Non-normative downstream research signals
tests/                       Schema, validator, corpus, and baseline invariants
tools/validate.py            Repository and adopter validation CLI
licensing/                   Machine-readable artifact licensing policy
```

## Initial corpus

| Range | Focus | Representative failures |
|---|---|---|
| DTF-001–003 | Authority | stale authority, scope escalation, dependent delegation after authority loss |
| DTF-013–019 | Authority at commitment | signature/authority substitution, expiry, revocation, iterative scope exceedance, approval binding, historical reconstruction |
| DTF-004–006 | Lifecycle | revocation, supersession, current vs historical validity |
| DTF-007–009 | Composition | false independence, authoritative conflict, undeclared transitivity |
| DTF-010–012 | Evidence | missing evidence, unresolved freshness, policy/version mismatch |
| DTF-020–027 | Cross-specification seams | semantic ownership, lifecycle stage reuse, composition validity, quorum independence, provenance/evidence sufficiency, workflow/assurance substitution |
| DTF-028–031 | Decision resolution | authority laundering, causal-basis misattribution, silent resolution, false persistence |
| DTF-032–037 | Privacy and correlation | proof-metadata correlation, status-query observability, purpose overrun, issuer-side unlinkability failure, aggregation, retention concentration |

Derived research signals and tranche judgments are recorded separately in `docs/*-observations.md`, including [`docs/privacy-correlation-tranche-observations.md`](docs/privacy-correlation-tranche-observations.md), so they do not expand the core schema by accident.

## Validate the contract and corpus

```bash
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python tools/validate.py
```

The tests and validator establish structural conformance, collection-level identity uniqueness, baseline case continuity, and rejection of important unsafe forms. A green result does not establish normative correctness, case completeness, severity, applicability, or implementation assurance.

## Authoring and adoption

Contributors should start with [`CONTRIBUTING.md`](CONTRIBUTING.md), [`docs/authoring-cases.md`](docs/authoring-cases.md), and [`docs/taxonomy.md`](docs/taxonomy.md). Adopters should read [`docs/consuming-the-corpus.md`](docs/consuming-the-corpus.md) before binding cases to an implementation or assurance process.

The unchanged v0.1 case schema is at [`schemas/failure-case.schema.json`](schemas/failure-case.schema.json); the v0.4.0 release continues to use that same contract.

## Licensing

This repository uses a dual-license model based on artifact type:

- Human-readable documentation, taxonomy prose, governance and contribution prose, diagrams, narrative examples, and release notes are licensed under **Creative Commons Attribution 4.0 International (CC-BY-4.0)**. See [`LICENSE-CONTENT`](LICENSE-CONTENT).
- Source code, validators, tests, machine-readable schemas, fixtures, corpus entries, executable configuration, and generated machine-readable evidence are licensed under **Apache License 2.0 (Apache-2.0)**. See [`LICENSE-CODE`](LICENSE-CODE).

The repository-level mapping is summarized in [`LICENSE`](LICENSE) and published in machine-readable form at [`licensing/artifact-license-policy.json`](licensing/artifact-license-policy.json). An explicit file-level license notice takes precedence if one is present.

## Security

Security-sensitive implementation findings should follow [`SECURITY.md`](SECURITY.md), not be disclosed through public corpus cases or issues. The public corpus is not an incident repository.

## Project ownership

Digital Trust Failure Corpus is an open QBF Consulting project intended to be consumable by independent standards, assurance, governance, interoperability, and implementation communities without requiring adoption of QBF-specific semantics.


## Authority-at-commitment failure tranche

Cases `DTF-013`–`DTF-019` cover signature/authority substitution, expired and revoked mandates, iterative scope expansion, stale or mismatched approvals, reputation/capability substitution, and unreconstructable historical commitment authority. They reuse the existing failure-case contract; no schema expansion was required.
