# CPC-001: Delegated-agent revocation consumer protection case

Status: **baseline, protection-contract and executable-fixture work packet**. This directory defines the first Consumer Protection Case (CPC) as a research and assurance artifact. It is not a canonical `DTF-*` corpus case, not a production safety certification, and not a claim that any implementation is currently assured.

Tracks: [#111](https://github.com/qbf-consulting/digital-trust-failure-corpus/issues/111)

## Purpose

CPC-001 examines whether a consumer can grant, inspect, and revoke bounded authority for an agent, and whether a product or service can enforce that revocation while producing evidence that an independent reviewer can inspect, reproduce, and challenge.

The consumer protection proposition is:

> A consumer should be able to withdraw delegated authority from an agent and have that withdrawal reliably enforced within explicitly stated scope, timing, and evidence limits.

The case is designed to demonstrate portfolio capability, not to validate a preferred protocol by assumption. ARPA, RAHP, DTFC, and any interop-lab component may contribute only where they provide necessary capability or independently useful evidence.

## Baseline scope

CPC-001 is scoped to a synthetic, non-production reference workflow:

1. A consumer grants bounded authority to an agent.
2. The consumer can inspect the granted authority.
3. The agent performs an in-scope action.
4. An out-of-scope action is denied.
5. The consumer revokes authority.
6. A post-revocation action attempt is denied after the defined effective point.
7. Missing, stale, contradictory, or unavailable authority evidence does not silently permit consequential action.
8. Material authorization decisions produce attributable evidence.
9. A reviewer can reproduce or challenge the material findings.

## Artifact map

| Artifact | Role | Status |
| --- | --- | --- |
| `case-manifest.yaml` | Machine-readable case identity, claims, repository roles, gates, and evidence expectations | Baseline |
| `baseline-architecture.md` | Repository placement, evidence lifecycle, publication path, and adversarial-resistance model | Baseline |
| `adversarial-test-matrix.yaml` | Initial challenge matrix for negative, stale-state, replay, concurrency, and tamper cases | Baseline |
| `protection-contracts.yaml` | Testable consumer protection behaviours for delegation, revocation, fail-safe handling, evidence and challenge | Draft contracts |
| `revocation-semantics.md` | Explicit revocation timing, convergence, stale-state and in-flight-action semantics | Draft semantics |
| `requirements-traceability.yaml` | Mapping from claims to protection contracts, adversarial conditions, minimum tests and evidence records | Draft traceability |
| `examples/cpc-001/protected_resource.py` | Synthetic protected resource that enforces the draft contracts for local testing | Executable fixture |
| `examples/cpc-001/defective_protected_resource.py` | Intentionally defective target that ignores revocation, stale authority and replay state | Known-defect fixture |
| `tools/execute_cpc001.py` | Runner that emits executed-synthetic-target evidence for the safe and defective targets | Executable fixture |
| `tests/test_cpc001_executable_fixture.py` | Unit tests for safe behaviour and known-defect detection | Test coverage |

## Repository ownership model

This repository owns the consumer protection case, harm model, evidence contract, assurance findings, and publication record. Component implementations should remain in the repositories that own those components.

| Repository | Proposed role |
| --- | --- |
| `qbf-consulting/digital-trust-failure-corpus` | Canonical CPC-001 case record, harm hypotheses, adversarial matrix, evidence requirements, and published findings |
| `qbf-consulting/agent-registry-protocol` | Candidate source for agent authority, delegation, revocation, and relationship semantics |
| `sankarshanmukhopadhyay/rahp-toolkit` | Candidate assessment and evidence evaluation mechanism, where its existing interfaces fit |
| Interoperability/reference implementation repository, if selected | Candidate executable service boundary and enforcement demonstration |

## Protection-contract posture

CPC-001 now defines ten draft protection contracts:

1. bounded delegation representation;
2. exact-action authorization binding;
3. out-of-scope denial;
4. revocation effectiveness;
5. safe handling of missing, stale or conflicting authority evidence;
6. replay and reuse resistance;
7. concurrent revocation/action ordering;
8. attributable authorization decision evidence;
9. consumer inspection; and
10. challenge and correction path.

These contracts intentionally distinguish authority evidence from relying-service enforcement. A registry, identifier, capability claim, signature or discovery record does not independently authorize a protected action.

## Executable fixture posture

The executable fixture is intentionally narrow. It tests a synthetic protected resource against the draft contracts and confirms that an intentionally defective implementation is detected.

Run the focused CPC-001 tests with:

```bash
python -m unittest tests.test_cpc001_executable_fixture -v
```

Run the paired fixture directly with:

```bash
python tools/execute_cpc001.py --role paired
```

The runner records `execution_class: executed-synthetic-target`, source digests, request digests, response digests, expected disposition, observed disposition and verdict. These outputs are local execution evidence only. They are not production assurance, not independent adoption, and not consumer usability validation.

## Non-goals

CPC-001 does not attempt to:

- certify any production agent system;
- prove that all AI agents are safe;
- publish or process personal data, secrets, customer records, or production credentials;
- make DTFC authoritative for ARPA, RAHP, or any external implementation;
- introduce a new generic assurance framework before a concrete need is demonstrated.

## Claim discipline

Every material claim must identify:

- scope;
- enforcement mechanism;
- verification method;
- supporting evidence;
- plausible counterexamples;
- residual limitation;
- current determination: `SUPPORTED`, `CONTRADICTED`, `INDETERMINATE`, or `NOT_ASSESSED`.

A green test result is evidence for a bounded claim. It is not consumer safety assurance by itself.

All CPC-001 claims remain `NOT_ASSESSED` until execution evidence is generated, retained and reviewed through an assurance determination.

## Immediate next tranche

The next tranche should turn executed fixture output into an explicit evidence package:

1. Generate a machine-readable evidence bundle from `tools/execute_cpc001.py --role paired`.
2. Pin source revisions and file digests.
3. Add schema or invariant checks for the CPC-001 result contract.
4. Produce a first assurance determination that distinguishes fixture-supported, contradicted, indeterminate and unassessed claims.
5. Preserve the limits: synthetic local execution is not independent implementation evidence.

## Completion rule

This baseline is complete when it enables a developer or reviewer to understand where CPC-001 artifacts live, what must be tested, what evidence must be generated, and which claims cannot yet be made.
