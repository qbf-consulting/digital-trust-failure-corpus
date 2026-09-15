# Validation

The repository validator checks structural conformance to the current failure-case schema plus a small set of collection-level invariants.

## Run the validator

Validate the repository corpus:

```bash
python tools/validate.py
```

Validate one or more explicit files or directories:

```bash
python tools/validate.py tests/fixtures/valid/DTF-000.json
python tools/validate.py path/to/cases/
```

Use a non-default schema when testing schema evolution:

```bash
python tools/validate.py --schema path/to/schema.json path/to/cases/
```

## What validation proves

Validation establishes that:

- the JSON Schema itself is valid Draft 2020-12;
- each case conforms to the schema;
- stable case IDs are unique in the validated collection;
- canonical case titles are unique in the validated collection;
- diagnostics identify the file and failing schema location;
- invalid input produces a non-zero CLI exit code.

An empty corpus validates successfully and reports zero cases. During bootstrap, absence of cases is not equivalent to evidence that the repository has coverage.

## What validation does not prove

A successful validation does **not** establish that a case is normatively correct, complete, severe, universally applicable, or supported by a particular standard. Those claims require review, provenance, and domain judgment outside the structural validator.

Negative fixtures live under `tests/fixtures/invalid/` and must never be treated as consumable corpus entries.
