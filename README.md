# Digital Trust Failure Corpus

A machine-readable corpus of failure conditions, adversarial configurations, invalid trust propositions, and expected safe outcomes for digital trust systems.

The project provides reusable failure cases, evidence requirements, and falsification criteria for conformance, assurance, interoperability, governance, and resilient trust infrastructure.

## Status

This repository is under active development. The current v0.1 work establishes the technology-neutral failure-case contract before adding the first substantive corpus tranche.

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
docs/taxonomy.md             Initial classification vocabulary
tests/fixtures/valid/        Canonical valid fixtures
tests/test_schema.py         Executable schema invariants
requirements-dev.txt         Test dependency
```

Additional corpus, validation, contribution, licensing, and CI surfaces will be introduced through bounded issues and pull requests.

## Validate the current contract

```bash
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
```

The tests establish that the schema itself is valid, the canonical fixture validates, and important unsafe or contradictory forms are rejected.

## Current schema

The v0.1 schema is at [`schemas/failure-case.schema.json`](schemas/failure-case.schema.json). Its classification vocabulary and extension boundary are documented in [`docs/taxonomy.md`](docs/taxonomy.md).

## Project ownership

Digital Trust Failure Corpus is an open QBF Consulting project intended to be consumable by independent standards, assurance, governance, interoperability, and implementation communities without requiring adoption of QBF-specific semantics.
