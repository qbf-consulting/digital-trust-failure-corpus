# Consuming the corpus

Digital Trust Failure Corpus is designed to be consumed by conformance suites, assurance tooling, interoperability labs, policy test harnesses, and implementations that need reusable negative trust propositions.

## What a case means

A case states a failure proposition, the evidence needed to evaluate it, safe/prohibited dispositions, and conditions that would falsify safe handling.

A case does **not** by itself establish:

- normative authority over an external specification;
- universal severity;
- applicability to every deployment;
- implementation conformance;
- assurance approval.

Consumers remain responsible for mapping the technology-neutral proposition to their own interfaces, policies, evidence sources, and authoritative specifications.

## Validate before consuming

Install the development dependency and validate the repository or selected case paths:

```bash
python -m pip install -r requirements-dev.txt
python tools/validate.py
python tools/validate.py corpus/authority
```

The validator proves schema conformance and collection-level ID/title uniqueness. It does not judge whether the proposition is substantively correct.

## Status handling

Case status is explicit. Consumers should decide which statuses they accept and should not silently treat `draft` as normative or production-ready. The initial v0.1 corpus intentionally uses draft cases while the model and community feedback mature.

## Dispositions

`PASS`, `DENY`, and `INDETERMINATE` describe bounded decision outcomes. The corpus may allow both DENY and INDETERMINATE when the correct choice depends on consumer policy or available evidence.

Do not convert missing, stale, conflicting, or unverifiable evidence into PASS merely because a local implementation lacks a recognised blocker.

## Bindings

A consumer may build a binding that maps a DTF case to:

- protocol exchanges;
- API requests and responses;
- credential or registry fixtures;
- agent relationships;
- policy controls;
- observability signals;
- assurance or risk-assessment inputs.

Keep binding semantics separate from the technology-neutral corpus unless repeated cross-implementation evidence justifies a core schema change.

## Versioning and reproducibility

Pin consumption to a repository tag or commit when deterministic evidence matters. A case ID is stable, but case content may evolve while its status is draft. Consumers should retain the case version and repository revision used for a test or assessment.

## Licensing

Human-readable documentation is CC-BY-4.0. Machine-readable corpus entries, schemas, validators, tests, and executable artifacts are Apache-2.0. See the repository licensing map and machine-readable policy for details.

## Reporting disagreement

Disagreement with a case is useful evidence. Open an issue explaining which proposition, assumption, evidence requirement, or disposition is incorrect or too broad. Prefer a concrete counterexample or authoritative source over a general objection.
