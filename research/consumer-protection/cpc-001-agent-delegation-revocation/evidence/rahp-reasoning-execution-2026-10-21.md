# CPC-001 bounded RAHP R1–R3 execution record (2026-10-21)

Status: **EXECUTED — OPTIONAL REASONING PROFILES ONLY; NOT TERMINAL RAHP ASSURANCE**.

## Provenance and invocation

- DTFC source evidence pin: `e7246692bc8f8350888aac2fabe2ce82886d146a`. The runner compares every inspected present evidence file byte-for-byte with the file at this commit.
- RAHP v2.8.0 commit: `7cd34ed53c537a43c0c5ed1a526a3748055e3f1c` (the annotated `v2.8.0` tag dereferences to this commit).
- RAHP profiles: `rahp-evidence-adequacy/v1`, `rahp-temporal-provenance/v1`, `rahp-reproducibility-challenge/v1`.
- Actual run: [GitHub Actions #39549426868](https://github.com/qbf-consulting/digital-trust-failure-corpus/actions/runs/39549426868).
- Independent repository validation: [GitHub Actions #39549426630](https://github.com/qbf-consulting/digital-trust-failure-corpus/actions/runs/39549426630).
- Run artifact: [`cpc001-rahp-reasoning` (ID 12323160776)](https://github.com/qbf-consulting/digital-trust-failure-corpus/actions/runs/39549426868/artifacts/12323160776). GitHub Actions artifact retention is 90 days; the code and this run record remain in Git.
- Raw result SHA-256: `3ffb7a3a66b1d93c3a2e56ad02b2e9ef5ec1e2784db95b2efbff5049b5ef567b`.
- Derived Markdown report SHA-256: `d4ee9bebed5bdcbc39f0323e6453b1502ee360bc898b577505cc13d024d0025e`.

Replay from repository root, with the matching RAHP commit checked out at `../rahp`:

```sh
python research/consumer-protection/cpc-001-agent-delegation-revocation/tools/run_pinned_rahp.py \
  --rahp ../rahp --output /tmp/cpc001-rahp-output
sha256sum /tmp/cpc001-rahp-output/*
```

The maintained automated replay is `.github/workflows/cpc001-rahp.yml`. It fetches the pinned RAHP commit, validates the DTFC evidence against its source pin, invokes the actual RAHP evaluators and publishes output. The execution environment is Python 3.12 on the GitHub Actions Ubuntu runner; the raw output records the interpreter version.

## Scope and observed results

The scoped question is whether the repository provides a *structurally inspectable synthetic scaffold*. No profile output asserts consumer safety, operational revocation, independent target implementation, or RAHP terminalization.

| Claim | Observed bounded determination | Interpretation |
|---|---|---|
| C1 bounded delegation | INDETERMINATE | Referenced contract and synthetic fixture metadata, not implementation assurance |
| C2 consumer inspection | NOT_ASSESSED | No consumer interaction observations |
| C3 denial of out-of-scope actions | INDETERMINATE | Synthetic fixture only |
| C4 post-revocation denial | INDETERMINATE | No independent runtime enforcement evidence |
| C5 missing/stale/conflicting authority | INDETERMINATE | Synthetic demonstration only |
| C6 attributable evidence | INDETERMINATE | No independently verified provenance chain |
| C7 consumer challenge | NOT_ASSESSED | No consumer-facing challenge workflow evidence |

- **R1:** Structural availability of referenced files was actually evaluated. A structural `PASS` for an item means only that a matching file exists, not that the underlying claim is true.
- **R2:** `INDETERMINATE`. No independent time-scoped revocation observation was supplied.
- **R3:** `DECLARED_MATCH` for two actual local invocations of the same R1 profile/input. It does not establish independent replay; the external-evidence challenge remains `OPEN`.
- Negative tests: missing R1 observations remain `INDETERMINATE`; duplicated/conflicting R1 observations remain `INDETERMINATE`; deliberately stale declared R2 evidence remains `INDETERMINATE`.
- Post-revocation target enforcement and replay resistance are **not exercised by these optional profiles**; pre-existing synthetic fixture tests have a different evidence boundary.

## Disposition

**Assessment execution completed at the optional R1–R3 structural profile boundary.** The entire consumer protection proposition is **not assured** and no terminal RAHP controller PASS, independent reproduction or production evaluation exists. The result supplies bounded evidence about the scaffold and about evidence insufficiency. It must not be promoted to an independent-target, product-safety or consumer-usability claim.

- Independent implementation semantics remain under DTFC #48.
- Independently operated consumer binding remains under DTFC #45.
- A future *terminal RAHP controller assessment* would require a separately defined and justified assessment subject, applicable controller contract and eligible independent evidence. It is not silently inferred from these optional profiles.
- The CPC-001 bridge's `BRIDGE_NOT_EXECUTED` applies to an actual terminal RAHP assessment, so it is **not** overwritten by this bounded structural execution.

No release is justified solely by this experimental assessment record.
