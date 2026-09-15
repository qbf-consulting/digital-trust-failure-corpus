# Digital Trust Failure Corpus

A machine-readable corpus of failure conditions, adversarial configurations, invalid trust propositions, and expected safe outcomes for digital trust systems.

The project provides reusable failure cases, evidence requirements, and falsification criteria for conformance, assurance, interoperability, governance, and resilient trust infrastructure.

## Status

This repository is under active v0.1 development. The technology-neutral failure-case contract, repository validator, CI validation, and the first substantive authority failure tranche are now represented in the repository.

The corpus is **evidence, not authority**. A case can cite normative specifications, governance frameworks, implementations, papers, or incidents, but inclusion here does not make the case itself normative.

## Core design principles

- Failure propositions should be falsifiable.
- Missing, stale, conflicting, or unverifiable evidence must not silently become success.
- The core model remains independent of any single DID method, credential format, registry protocol, assurance methodology, or agent architecture.
- Consumers may have legitimate policy differences; a case can therefore permit more than one safe disposition.
- Taxonomy and schema evolution should be driven by concrete cases rather than speculative completeness.

## Repository structure

```text
schemas/                     Versioned machine-readable case contract
corpus/                      Consumable machine-readable failure cases
docs/taxonomy.md             Initial classification vocabulary
docs/*-observations.md       Non-normative downstream research signals
tests/fixtures/              Positive and negative validation fixtures
tests/                       Executable schema, validator, and corpus invariants
tools/validate.py            Repository and adopter validation CLI
licensing/                   Machine-readable artifact licensing policy
requirements-dev.txt         Test dependency
```

## Current corpus

The initial authority tranche is under [`corpus/authority/`](corpus/authority/) and establishes three technology-neutral failure propositions:

- `DTF-001` — stale authority evidence after revocation;
- `DTF-002` — delegated authority exceeds permitted scope;
- `DTF-003` — delegation survives loss of its authority source.

Derived research signals for lifecycle modelling, executable governance, and trust-infrastructure observability are recorded separately in [`docs/authority-tranche-observations.md`](docs/authority-tranche-observations.md) so they do not expand the core schema by accident.

## Validate the current contract and corpus

```bash
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python tools/validate.py
```

The tests and validator establish structural conformance, collection-level identity uniqueness, and rejection of important unsafe forms. A green result does not establish normative correctness, case completeness, severity, applicability, or implementation assurance.

## Current schema

The v0.1 schema is at [`schemas/failure-case.schema.json`](schemas/failure-case.schema.json). Its classification vocabulary and extension boundary are documented in [`docs/taxonomy.md`](docs/taxonomy.md).

## Licensing

This repository uses a dual-license model based on artifact type:

- Human-readable documentation, taxonomy prose, governance and contribution prose, diagrams, narrative examples, and release notes are licensed under **Creative Commons Attribution 4.0 International (CC-BY-4.0)**. See [`LICENSE-CONTENT`](LICENSE-CONTENT).
- Source code, validators, tests, machine-readable schemas, fixtures, corpus entries, executable configuration, and generated machine-readable evidence are licensed under **Apache License 2.0 (Apache-2.0)**. See [`LICENSE-CODE`](LICENSE-CODE).

The repository-level mapping is summarized in [`LICENSE`](LICENSE) and published in machine-readable form at [`licensing/artifact-license-policy.json`](licensing/artifact-license-policy.json). An explicit file-level license notice takes precedence if one is present.

## Project ownership

Digital Trust Failure Corpus is an open QBF Consulting project intended to be consumable by independent standards, assurance, governance, interoperability, and implementation communities without requiring adoption of QBF-specific semantics.
