# CPC-001 RAHP assessment bridge guide

Status: **assessment bridge, not an assessment result**.

This guide explains how to use the CPC-001 evidence package as an input to RAHP or an equivalent assurance review. It does not claim that RAHP has executed, that CPC-001 is assured, or that the synthetic fixture establishes production safety.

## Purpose

The bridge exists to make CPC-001 assessable without weakening the evidence boundary. It converts the case into a reviewable input package:

```text
claim -> protection contract -> evidence input -> current boundary -> permitted disposition
```

The bridge should be used to ask:

> Does the current CPC-001 package contain a coherent, traceable and reproducible synthetic evidence scaffold for delegated-agent revocation?

It must not be used to ask:

- whether a production product or service is safe;
- whether ARPA is conformant;
- whether independent reproduction has occurred;
- whether consumer usability has been validated; or
- whether RAHP has already assessed CPC-001.

## Required input set

A reviewer should inspect, at minimum:

- `case-manifest.yaml`
- `baseline-architecture.md`
- `protection-contracts.yaml`
- `revocation-semantics.md`
- `requirements-traceability.yaml`
- `adversarial-test-matrix.yaml`
- `evidence/current-determination.yaml`
- `evidence/evidence-manifest.yaml`
- `evidence/reproduction-instructions.md`
- `evidence/independent-reproduction-record-template.yaml`
- `evidence/rahp-assessment-bridge.yaml`

## Assessment method

A RAHP or equivalent assessment should:

1. Confirm that each material claim has an explicit scope and evidence input.
2. Confirm that synthetic fixture evidence is not promoted into production assurance.
3. Confirm that independent reproduction remains absent unless a completed record is supplied.
4. Confirm that consumer-facing inspection and challenge claims remain `NOT_ASSESSED`.
5. Confirm that missing or stale authority evidence remains fail-safe in the synthetic target.
6. Record whether evidence supports only a synthetic-fixture proposition, remains indeterminate, is contradicted, or is not assessed.

## Permitted outputs

The bridge allows these output categories:

- `SUPPORTED_FOR_SYNTHETIC_FIXTURE_ONLY`
- `INDETERMINATE`
- `NOT_ASSESSED`
- `CONTRADICTED`

It does not allow these outputs:

- `PRODUCTION_SAFE`
- `INDEPENDENTLY_REPRODUCED`
- `ARPA_CONFORMANT`
- `RAHP_ASSESSED` unless a real RAHP result is separately generated
- `CONSUMER_USABILITY_VALIDATED`

## Evidence handling

The assessor should treat CI success as evidence that repository-owned tests executed in CI. CI success is not independent reproduction unless the reviewer is operationally separate and records the environment, command, observed output, and relationship statement in a completed reproduction record.

The assessor should treat the defective target as evidence that the test suite can detect selected known defects. It does not prove that the suite detects every relevant defect.

## Stop condition

This tranche is complete when:

- the bridge file exists;
- this guide exists;
- tests prevent the bridge from claiming completed RAHP assessment; and
- CI confirms the guardrails.

The next substantive tranche requires an actual RAHP or equivalent assessment result, or a completed independent reproduction record.
