# Consumer Protection Case 001: delegated-agent revocation

Status: **publication entry point for a baseline and protection-contract work packet**. This page introduces CPC-001 for readers who consume the repository through documentation rather than the `research/` tree.

Canonical source artifacts live at:

```text
research/consumer-protection/cpc-001-agent-delegation-revocation/
```

Tracking issue: [#111](https://github.com/qbf-consulting/digital-trust-failure-corpus/issues/111)

## What CPC-001 examines

CPC-001 examines whether a consumer can grant, inspect, and revoke bounded authority for an agent, and whether a product or service can enforce that revocation while producing evidence that an independent reviewer can inspect, reproduce, and challenge.

The consumer protection proposition is:

> A consumer should be able to withdraw delegated authority from an agent and have that withdrawal reliably enforced within explicitly stated scope, timing, and evidence limits.

## What this page does not claim

This page does not claim that:

- any production service has been assessed;
- any agent system is generally safe;
- ARPA, RAHP, DTFC, or any selected implementation has passed CPC-001;
- consumer usability has been validated with real users;
- synthetic local execution is independent adoption evidence.

## Current artifacts

| Artifact | Purpose |
| --- | --- |
| `README.md` | Case overview, repository roles, non-goals, and next tranche |
| `case-manifest.yaml` | Machine-readable claims, gates, evidence expectations, and repository roles |
| `baseline-architecture.md` | Artifact placement, evidence lifecycle, publication model, and adversarial-resistance posture |
| `adversarial-test-matrix.yaml` | Initial actor, environment, and reviewer challenge matrix |
| `protection-contracts.yaml` | Draft testable consumer protection behaviours |
| `revocation-semantics.md` | Revocation effectiveness, convergence, stale-state and in-flight-action semantics |
| `requirements-traceability.yaml` | Claim-to-contract-to-test-to-evidence mapping |

## Protection contracts now defined

The current draft contracts cover:

- bounded delegation representation;
- exact-action authorization binding;
- out-of-scope denial;
- revocation effectiveness;
- safe handling of missing, stale or conflicting authority evidence;
- replay and reuse resistance;
- concurrent revocation and action ordering;
- attributable authorization decision evidence;
- consumer inspection; and
- challenge and correction path.

These contracts treat registry or identity evidence as inputs to an action-specific authorization decision. They do not treat discovery, authentication, registration, capability claims or signatures as sufficient commitment authority.

## How to read the case

Read CPC-001 as a claim-and-evidence scaffold:

```text
consumer harm -> protection claim -> testable requirement -> evidence artifact -> determination -> limitation
```

No claim should be treated as supported unless the case identifies the implementation boundary, verification method, evidence artifact, and residual limitation.

## Next expected evidence

The next tranche should produce:

- selected reference enforcement environment;
- service-boundary document;
- executable fixture binding for each mandatory protection contract;
- positive and negative authorization tests;
- post-revocation denial tests;
- stale, missing, contradictory, unavailable, replay, and tamper tests;
- intentionally defective implementation evidence;
- evidence manifest with pinned source revisions and digests;
- assurance determination distinguishing `SUPPORTED`, `CONTRADICTED`, `INDETERMINATE`, and `NOT_ASSESSED` claims.

## Consumer-facing interpretation

For a consumer, the question is not whether an agent has an identifier or whether a registry entry exists. The question is whether the service can demonstrate that delegated authority is bounded, revocable, inspectable, and accountable in a way that prevents unsupported action and preserves a path for review.

CPC-001 is intended to make that question testable.
