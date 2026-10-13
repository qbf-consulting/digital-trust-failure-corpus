# CPC-001 candidate target selection guide

Status: **candidate selection not started**.

This guide describes how to evaluate possible non-synthetic implementation targets for CPC-001 without prematurely treating any candidate as admitted evidence.

## Purpose

CPC-001 currently has synthetic and CI-executed synthetic evidence. A future tranche may bind CPC-001 to a non-synthetic target, but only after a concrete implementation target is selected, bounded, replayable and reviewed.

This guide defines the selection procedure for that future step.

## Non-goals

This guide does not:

- select a candidate target;
- admit a candidate target;
- claim non-synthetic implementation evidence;
- claim production product or service safety;
- claim ARPA conformance;
- claim completed RAHP assessment;
- claim independent reproduction.

## Candidate selection sequence

1. Identify a concrete target.
2. Confirm the implementation owner and maintenance boundary.
3. Confirm access, license and replay constraints.
4. Identify the protected resource and exact protected action.
5. Identify the authorization decision point.
6. Identify the revocation enforcement point.
7. Define the execution adapter and replay command.
8. Define a negative-control strategy.
9. Confirm that no production secret, personal data or live consequential action is required.
10. Record the candidate in `candidate-target-selection-register.yaml`.
11. Decide whether the target is `REJECT`, `NEEDS_MORE_EVIDENCE`, or `ADMIT_FOR_EXPERIMENTAL_BINDING`.

## Admission threshold

A candidate may be recommended for experimental binding only when the reviewer can identify:

- the target's owner or maintainer;
- an immutable revision, release or artifact digest;
- the protected resource and action;
- the authorization decision point;
- the revocation enforcement point;
- the execution adapter;
- a replay command;
- a negative-control strategy;
- the safety and data boundary;
- evidence retention expectations.

A candidate that cannot provide those elements should remain `NEEDS_MORE_EVIDENCE` or be rejected.

## Evidence interpretation

Candidate review metadata is not execution evidence. It is an admission-control input.

A filled candidate record may support a claim such as:

> CPC-001 has identified a candidate target that appears suitable for experimental binding.

It cannot support claims such as:

- the target satisfies CPC-001;
- the target enforces revocation correctly;
- the target is safe for consumers;
- the target is ARPA conformant;
- the target has been RAHP assessed;
- the target has been independently reproduced.

## Stop condition

This tranche is complete when the repository contains:

- a candidate-selection register;
- a reviewer guide;
- tests ensuring that an empty register is not treated as admitted evidence.

The next substantive step is to select and review one concrete target, or pause CPC-001 until such a target is available.
