# CPC-001 baseline architecture

Status: **baseline architecture**. This document fixes the initial evidence and repository architecture for CPC-001. It deliberately does not select a final implementation target or claim assurance.

## 1. Architectural posture

CPC-001 is a consumer protection case, not a component-conformance case. The primary subject is the consumer-facing protection:

> withdrawal of delegated agent authority must have an enforceable, inspectable, and evidentially reconstructable effect.

The case therefore starts from consumer harm and service behaviour, then maps to implementation and assurance mechanisms.

## 2. Artifact placement

The baseline location is:

```text
research/consumer-protection/cpc-001-agent-delegation-revocation/
```

This is outside `corpus/` because CPC-001 is broader than a single `DTF-*` failure proposition. It may later generate canonical corpus cases if repeated failure patterns require them, but the baseline should not expand the core schema prematurely.

## 3. Source artifacts and generated artifacts

| Class | Examples | Storage rule |
| --- | --- | --- |
| Source case artifacts | Case manifest, harm model, protection requirements, adversarial test matrix | Commit to Git |
| Implementation artifacts | Enforcement code, protocol fixtures, test harnesses | Commit in owning implementation repository |
| Evidence artifacts | Test results, decision traces, digests, reproduction reports | Commit only small sanitized examples; publish complete bundles as release assets when durable publication is required |
| Publication artifacts | Reviewer guide, consumer-facing explanation, findings summary | Commit to Git and render through Pages where appropriate |
| Sensitive artifacts | Secrets, tokens, real personal data, confidential incident details | Do not publish; do not require for CPC-001 |

## 4. Repository responsibility boundaries

DTFC owns the case-level evidence contract and failure-informed adversarial posture. It must not become the owner of ARPA semantics, RAHP assessment implementation, or an external product's runtime enforcement code.

Component repositories may be used only where they contribute necessary capability or independently useful evidence.

| Capability | Owning location | CPC-001 relationship |
| --- | --- | --- |
| Consumer harm and protection case | DTFC research path | Canonical source |
| Agent authority semantics | ARPA or selected implementation owner | Candidate input |
| Evidence and assurance evaluation | RAHP or DTFC-local research fixture | Candidate input |
| Runtime enforcement demonstration | Selected reference implementation | Candidate input |
| Publication and review record | DTFC docs/research path | Canonical output |

## 5. Claim and evidence model

CPC-001 uses a claim-first evidence model:

```text
claim -> requirement -> verification method -> evidence artifact -> determination -> limitation
```

No claim may be marked `SUPPORTED` unless the evidence artifact is identified, reproducible or reviewable, and within scope.

Allowed determinations:

- `SUPPORTED`: the scoped claim is supported by identified evidence.
- `CONTRADICTED`: evidence shows the claim does not hold under tested conditions.
- `INDETERMINATE`: the claim may be true, but evidence is missing, stale, incomplete, contradictory, or outside scope.
- `NOT_ASSESSED`: the claim has not yet been evaluated.

## 6. Adversarial-resistance properties

CPC-001 should be resistant to three challenge classes.

### 6.1 Adversarial actor

An agent or caller attempts to exceed authority through scope substitution, replay, stale credentials, post-revocation use, or bypass of the protected enforcement point.

### 6.2 Adversarial environment

The environment introduces unavailable authority sources, stale cache state, concurrent revocation and action ordering, malformed evidence, or conflicting authority records.

### 6.3 Adversarial reviewer

A reviewer challenges assumptions, test selection, evidence provenance, claim overreach, and publication integrity.

The case succeeds only if these challenges are either tested, explicitly scoped out, or marked as unresolved limitations.

## 7. Minimum execution evidence

Each execution evidence record should include:

| Field | Purpose |
| --- | --- |
| `case_id` | Binds evidence to CPC-001 |
| `run_id` | Identifies the specific execution |
| `subject_implementation` | Identifies the tested implementation |
| `immutable_revision` | Prevents branch drift |
| `environment_profile` | Describes the execution context |
| `configuration_digest` | Binds configuration to result |
| `claim_id` | Maps result to the relevant claim |
| `test_id` | Identifies verification method |
| `expected_result` | Records the test oracle |
| `observed_result` | Records actual outcome |
| `result` | PASS, FAIL, ERROR, or NOT_APPLICABLE at test level |
| `evidence_artifact` | Points to raw or summarized evidence |
| `artifact_digest` | Supports tamper detection |
| `limitations` | Prevents overclaiming |

Test-level `PASS` must not automatically become claim-level `SUPPORTED`.

## 8. Publication model

CPC-001 should have three publication surfaces when mature enough:

1. **GitHub source record**: full trace from issue to PR to artifacts.
2. **Readable documentation**: human-facing explanation through repository docs or Pages.
3. **Versioned evidence bundle**: immutable evidence package with digests and reproduction instructions.

A CI artifact is not sufficient as the only durable evidence location because artifacts may expire.

## 9. Evidence freshness and supersession

CPC-001 findings must remain historically accurate. Later results may supersede an earlier determination, but they must not silently rewrite it.

Events requiring reassessment include:

- implementation revision change;
- authority or revocation semantic change;
- new relevant failure case;
- evidence artifact expiry;
- discovered enforcement defect;
- test harness change;
- evidence schema change.

## 10. Baseline decision

The baseline decision is:

- Keep CPC-001 under `research/consumer-protection/` until a narrower canonical corpus case is justified.
- Treat DTFC as the case and evidence-governance owner.
- Keep implementation changes in component repositories.
- Require adversarial negative tests and known-defect detection before any assurance claim.
- Treat independent reproduction as a separate gate, not as a synonym for rerunning local CI.

## 11. Open baseline questions

The next tranche must answer:

1. Which repository provides the smallest credible reference enforcement environment?
2. Which ARPA artifacts already define sufficient delegation and revocation semantics?
3. Which RAHP artifact format can consume or evaluate CPC-001 evidence without schema distortion?
4. Should CPC-001 produce one or more canonical `DTF-*` failure cases after the first execution?
5. What GitHub Pages path should present CPC-001 without making the rendered page a second source of truth?
