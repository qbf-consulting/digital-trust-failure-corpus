# Contributing to Digital Trust Failure Corpus

Digital Trust Failure Corpus accepts focused contributions that make digital-trust failure propositions more concrete, falsifiable, reusable, and testable.

## Before opening a pull request

For a substantive new case or semantic change, open an issue first. The issue should state:

- the failure proposition;
- why the case is materially distinct from existing cases;
- the evidence needed to evaluate it;
- what outcome would demonstrate unsafe handling;
- relevant references or provenance;
- any unresolved judgment that reviewers should make explicitly.

Repository work follows a bounded **Issue → implementation → tests → PR → CI → merge** sequence. Trivial editorial corrections may use a lighter path.

## Adding a case

1. Read `docs/authoring-cases.md` and `docs/taxonomy.md`.
2. Search `corpus/` for an equivalent proposition before creating a new ID.
3. Use the next unallocated `DTF-NNN` identifier.
4. Keep the case technology-neutral unless the contribution is explicitly proposed as a future binding outside the core corpus.
5. State at least one evidence requirement and one falsification condition.
6. Do not treat missing, stale, conflicting, or unverifiable evidence as PASS.
7. Add or update tests for any new invariant or material semantic claim.
8. Run:

```bash
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python tools/validate.py
```

## Provenance and references

A reference explains where a proposition, constraint, or observed failure came from. It does not automatically make that source normative for every consumer.

Prefer public specifications, issues, pull requests, papers, implementation evidence, or published incident material. A repository issue may preserve the project's own judgment trail, but a self-reference is not independent normative support.

Do not submit confidential, personal, security-sensitive, or non-public incident information to the public corpus. Generalise such material into a non-identifying proposition only when doing so preserves the technical meaning and is lawful and appropriate.

## Schema changes

Do not add a schema field merely because one case would be easier to write with it. Schema evolution should be justified by repeated corpus needs that cannot be expressed faithfully with the current technology-neutral contract.

Breaking schema changes must be explicit, include migration impact, and be treated as potential compatibility and assurance invalidation events.

## Review standard

A case should be reviewable as a proposition another competent implementer could challenge or test. Review should distinguish:

- structural validity;
- clarity of the failure proposition;
- evidence sufficiency;
- falsifiability;
- provenance;
- technology neutrality;
- residual uncertainty.

A green CI run establishes repository conformance. It does not by itself establish normative correctness, severity, completeness, or applicability.

## Licensing

By contributing, you agree that material is made available under the repository's artifact-type licensing model: CC-BY-4.0 for human-readable content and Apache-2.0 for machine-readable and executable artifacts, unless an explicit accepted file-level notice states otherwise.
