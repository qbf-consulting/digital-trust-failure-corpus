# Digital Trust Failure Corpus v0.1.0

## Purpose of this baseline

v0.1.0 establishes the first reproducible development baseline for Digital Trust Failure Corpus (DTF): a technology-neutral, machine-readable set of falsifiable failure propositions for digital trust systems.

The release provides a stable point from which implementers, assurance tools, interoperability labs, governance work, and standards communities can evaluate whether the corpus model is useful and challenge individual cases with evidence.

## Included capability

- JSON Schema Draft 2020-12 case contract, version 0.1.0.
- Repository validator and deterministic collection-level identity checks.
- Negative fixtures for important invalid forms.
- CI validation on pull requests and `main`.
- Twelve initial draft cases across four families:
  - **Authority:** DTF-001 through DTF-003.
  - **Lifecycle:** DTF-004 through DTF-006.
  - **Composition:** DTF-007 through DTF-009.
  - **Evidence:** DTF-010 through DTF-012.
- Contributor and adopter guidance.
- Explicit dual licensing by artifact type.

## Core judgment

The corpus is **evidence, not authority**. Inclusion of a case does not make its proposition normative for another specification or ecosystem. Consumers should map cases to their authoritative rules, interfaces, evidence sources, and decision policies.

The initial cases intentionally permit both `DENY` and `INDETERMINATE` where the corpus cannot legitimately choose consumer policy. Missing, stale, conflicting, or unverifiable evidence must not silently become `PASS`.

## Reproduce validation

```bash
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python tools/validate.py
```

For evidence-producing use, consumers should pin to the v0.1.0 tag or its exact commit rather than a moving branch.

## Licensing

Human-readable content is licensed under CC-BY-4.0. Machine-readable corpus entries, schemas, validators, tests, fixtures, and executable configuration are licensed under Apache-2.0. See `LICENSE` and `licensing/artifact-license-policy.json`.

## Known limits

- All twelve cases remain `draft`.
- The corpus is deliberately not exhaustive.
- There are no implementation-specific protocol bindings in v0.1.0.
- The corpus does not define severity.
- The corpus does not define a universal lifecycle protocol, governance execution model, or observability standard.
- A green validation result establishes repository conformance, not substantive correctness, applicability, or assurance approval.

## Forward research signals

The initial cases provide evidence for three adjacent research tracks without coupling those models into DTF:

1. **Trust Lifecycle Event Model** — event/effective/observation/decision time, current versus historical validity, and lifecycle semantics.
2. **Executable Governance Profile** — competent authority, scope, evidence freshness, conflict handling, and policy-to-control mapping.
3. **Trust Infrastructure Observability Model** — evidence age, lifecycle propagation, unresolved decisions, authority-state changes, and composition failures.

Future DTF changes should continue to be driven by concrete cases and executable evidence rather than speculative schema expansion.
