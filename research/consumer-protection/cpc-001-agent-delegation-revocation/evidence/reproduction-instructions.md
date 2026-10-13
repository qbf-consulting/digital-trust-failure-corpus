# CPC-001 reproduction instructions

Status: **synthetic fixture reproduction path**.

These instructions reproduce the repository-owned CPC-001 synthetic fixture. They do not constitute independent reproduction unless executed and reported by a separate reviewer or environment.

## Preconditions

- Python 3.12 or compatible Python 3 runtime.
- Repository checkout containing merged commit `6723329668d1feb8815c9c1f74fcf3e9d928d891` or a later commit that explicitly preserves the CPC-001 evidence manifest.
- Development dependency installation:

```bash
python -m pip install -r requirements-dev.txt
```

## Run the focused synthetic fixture

```bash
python tools/execute_cpc001.py --role paired
```

Expected high-level result:

- the safe target is classified as satisfying the included synthetic scenarios;
- the defective target is classified as violating the CPC-001 fixture expectations;
- the same scenario identifiers are exercised across both targets;
- post-revocation, stale-authority and replay defects remain visible.

## Run repository validation

```bash
python -m unittest discover -s tests -v
python tools/validate.py
```

The repository validation path should include:

- `tests/test_cpc001_executable_fixture.py`;
- `tests/test_cpc001_current_determination.py`; and
- `tests/test_cpc001_evidence_manifest.py`.

## Interpret the result

A successful reproduction supports only this bounded statement:

> The repository-owned CPC-001 synthetic fixture detects the deliberately defective protected-resource target under the included scenarios.

It does not support any of the following statements:

- CPC-001 has been independently reproduced.
- CPC-001 demonstrates production product or service safety.
- ARPA is conformant.
- RAHP has assessed CPC-001.
- Consumer usability has been validated.

## Independent reproduction record

A future independent reproduction record should include:

- reviewer identity or role;
- execution environment;
- repository commit;
- commands executed;
- command outputs or result digests;
- whether the same findings were obtained;
- any discrepancy, limitation or unresolved observation.

Until that record exists, the independent-reproduction gate remains open.
