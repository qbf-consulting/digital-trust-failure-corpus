# CPC-001 non-synthetic implementation admission guide

Status: **admission gate only**.

This guide explains how CPC-001 may later be bound to an externally maintained, product-like, or otherwise non-synthetic implementation target.

It does not select a target. It does not claim that any implementation has passed CPC-001.

## Why this gate exists

CPC-001 currently has repository-owned synthetic evidence and CI-executed synthetic evidence. That is useful for proving that the CPC-001 fixture can detect the included defective target, but it is not enough to make a claim about a real implementation.

A non-synthetic target must therefore be admitted before it is tested.

## Admission rule

A candidate implementation may be admitted for CPC-001 testing only when the case record identifies:

1. the implementation owner or accountable maintainer;
2. an immutable target revision or artifact digest;
3. the protected resource and authorization boundary;
4. the source of current authority and revocation state;
5. the mapping from CPC-001 contracts to target behaviour;
6. the execution adapter and output contract;
7. a negative-control or known-defect strategy;
8. the data, privacy and publication boundary; and
9. a reproducible execution path.

Absence of any mandatory element should produce `NOT_ADMITTED` or `ADMISSION_INDETERMINATE`, not an implicit pass.

## What counts as non-synthetic implementation evidence

A target may be non-synthetic when it is maintained outside the CPC-001 fixture and has a durable implementation identity. Examples include:

- an external reference implementation;
- a product-like local service with realistic enforcement boundaries;
- an independently maintained adapter;
- a protocol implementation repository that can be pinned and executed.

The target does not need to be production software. It does need to be distinct from the CPC-001 synthetic fixture.

## What does not count

The following are not non-synthetic implementation evidence:

- the repository-owned safe fixture;
- the repository-owned deliberately defective fixture;
- local self-runs of `tools/execute_cpc001.py` alone;
- GitHub Actions success on the synthetic fixture alone;
- a design document without an executable target;
- registry, discovery or identity records that do not exercise relying-service authorization.

## Required output of a future binding tranche

A future binding tranche should produce a completed implementation binding record with:

- selected target identity;
- target revision;
- execution command or adapter;
- scenario mapping;
- observed results;
- evidence digests;
- negative-control results;
- unsupported contracts;
- limitations;
- final admission value.

Only after that record exists should CPC-001 move from admission readiness to non-synthetic testing.

## Current determination

Current value:

```text
NOT_ADMITTED
```

Reason:

No non-synthetic implementation target has been selected or evidenced.

## Prohibited interpretation

This guide must not be cited as evidence that CPC-001 has assessed a real implementation. It is only the gate that defines what evidence a real implementation must provide before admission.
