# CPC-001 revocation semantics

**Status:** draft protection semantics for CPC-001. This document is not a production certification, not an ARPA amendment and not a DTFC canonical failure case.

## Purpose

CPC-001 examines whether a consumer can withdraw delegated authority from an agent and whether a relying service can enforce that withdrawal while preserving enough evidence for independent review.

The revocation model must therefore distinguish four separate events:

1. **Consumer withdrawal request** — the consumer initiates withdrawal.
2. **Revocation recording** — the authority source records the withdrawal.
3. **Revocation effectiveness** — the revoked delegation should no longer authorize new protected actions under the stated semantics.
4. **Enforcement convergence** — relying services stop accepting the revoked authority within the stated freshness and synchronization boundary.

Recording revocation is not the same as enforcing it.

## Decision boundary

CPC-001 adopts the following decision boundary:

> Discovery, authentication, registration and capability signals establish who the actor may be. They do not independently authorize the protected action. A relying service must evaluate the exact action, current authority state, material constraints, policy version and relevant lifecycle or revocation evidence at evaluation time.

This is aligned with the ARPA authority-at-commitment projection: ARPA can contribute authority and lifecycle evidence, but the relying system still decides whether the exact action is authorized now.

## Required revocation fields

A CPC-001 revocation event or equivalent authority-state record must identify:

| Field | Purpose |
| --- | --- |
| `delegation_id` | Identifies the delegation being withdrawn. |
| `consumer_or_principal_id` | Identifies the party that granted or controls the authority. |
| `agent_id` | Identifies the agent whose authority is affected. |
| `revocation_requested_at` | Records when withdrawal was requested. |
| `revocation_recorded_at` | Records when the authority source recorded withdrawal. |
| `revocation_effective_at` | Defines the boundary after which new protected actions must not be authorized under the revoked delegation. |
| `enforcement_convergence_bound` | Defines the maximum tolerated delay or event boundary for enforcement convergence. |
| `reason_category` | Provides a non-sensitive reason class where appropriate. |
| `source_checkpoint` | Identifies the authority-state source version or checkpoint. |
| `evidence_digest` | Binds the record to integrity-checkable evidence. |

If the implementation cannot provide one of these fields, the assurance case must record the missing field as a limitation. The absence must not be inferred away.

## Default semantic posture

CPC-001 uses a conservative semantic posture for consequential actions:

- **Pre-revocation authorization:** An action evaluated before the revocation effective boundary may be allowed if all other authority and policy conditions are satisfied.
- **Post-revocation authorization:** An action evaluated after the revocation effective boundary and enforcement convergence boundary must not be authorized using the revoked delegation.
- **In-flight action:** The service must explicitly state whether in-flight actions are completed, cancelled, held for review, compensated or denied.
- **Unavailable authority state:** If current authority state is unavailable and the action is consequential, the result must be `deny` or `indeterminate` according to documented fail-safe policy.
- **Stale authority state:** Cached state may be used only within a documented freshness policy. Stale cache use after the convergence boundary is an assurance failure unless the protected action is non-consequential or otherwise explicitly excluded.
- **Conflicting authority state:** Conflicting competent sources require `deny` or `indeterminate` unless a documented precedence rule resolves the conflict.

## Half-open validity interval

Where validity intervals are used, CPC-001 treats authority as valid during:

```text
valid_from <= evaluation_time < valid_until
```

Revoked authority cannot authorize a new protected action at or after the applicable revocation effective boundary, subject to the stated enforcement convergence boundary and in-flight-action semantics.

## Ordering scenarios

| Scenario | Required disposition |
| --- | --- |
| Action evaluated before revocation request | Evaluate under then-current authority state; record historical evidence. |
| Action evaluated after withdrawal request but before revocation recorded | Must follow the documented policy for pending revocation visibility; any allow requires explicit evidence and limitation. |
| Action evaluated after revocation recorded but before effective time | Must follow the documented effective-time semantics. |
| Action evaluated after effective time but before convergence bound | Must follow documented convergence semantics; authorization remains a limitation unless explicitly justified. |
| Action evaluated after convergence bound | Must not be authorized using the revoked delegation. |
| Action starts before revocation and completes after revocation | Must follow documented in-flight-action disposition. |
| Authority source unavailable during evaluation | Must not silently allow consequential action. |
| Cached pre-revocation state used after convergence bound | Contradicts CP-004 unless freshness policy explicitly excludes the action and the exclusion is justified. |

## Evidence required for a revocation finding

A supported revocation-enforcement claim requires at least:

1. a pre-revocation authorized action under the delegation;
2. a revocation event with effective-time and convergence semantics;
3. a post-revocation action attempt using the revoked authority;
4. a denial or indeterminate result consistent with the protection contract;
5. source, policy and evaluator version identifiers;
6. request, evaluation, revocation and decision timestamps;
7. decision evidence sufficient for later reconstruction; and
8. at least one negative or known-defect test demonstrating that the verification harness detects an unsafe post-revocation allow.

If any required evidence is unavailable, the revocation claim remains `INDETERMINATE` or `NOT_ASSESSED`, depending on whether execution occurred.

## Consumer-facing semantics

The consumer-facing view should not merely show that revocation exists. It should allow the consumer or reviewer to determine:

- which delegated authority was active;
- when it was revoked;
- when revocation became effective;
- what actions were attempted before and after revocation;
- which actions were allowed, denied or held;
- what evidence supports those decisions; and
- how to challenge a disputed post-revocation action.

If the first implementation only demonstrates engineering feasibility and not consumer comprehension or usability, the assurance report must say so.

## Non-goals

CPC-001 does not attempt to prove:

- universal revocation semantics for all distributed systems;
- zero-latency enforcement across all relying services;
- legal sufficiency of withdrawal notice;
- that the consumer interface is usable by all populations;
- that an agent cannot act through an unrelated channel outside the protected service boundary.

Those may become later assessment dimensions, but they are not established by the first protection case.
