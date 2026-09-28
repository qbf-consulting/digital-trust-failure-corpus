# Decision-resolution failure tranche observations

This note records the judgment behind the decision-resolution failure tranche reserved as DTF-028 through DTF-031. It is explanatory material, not additional normative authority.

## Scope

The tranche captures four technology-neutral failures:

- **DTF-028 — authority laundering through non-authoritative signals**
- **DTF-029 — decision transition basis misattributed**
- **DTF-030 — unresolved material condition cleared without resolution evidence**
- **DTF-031 — resolved condition remains blocking after valid resolution**

The cases reuse the existing failure-case schema and taxonomy. No new domain, failure class, disposition, or evidence category was required.

## DTF-028 and DTF-018 are distinct

DTF-018 covers a specific substitution failure: reputation, capability advertisement, technical ability, or assurance posture is treated as authority for a material commitment.

DTF-028 covers the broader non-amplification failure. Authority can be laundered through repetition, consensus, endorsement, aggregation, projection, discovery, reputation, capability, or unrelated authority even when no single signal is itself mistaken directly for permission.

The falsifiable proposition is therefore broader:

> Transforming or combining non-authoritative signals must not create authority that cannot be established from competent provenance and applicable scope.

DTF-018 remains useful as a specific negative vector within that broader failure family.

## DTF-029 preserves causal provenance

A changed decision does not by itself establish that authority changed.

A transition may result from:

- authority change;
- evidence change;
- policy change;
- lifecycle-state change;
- correction; or
- evaluation-context change.

DTF-029 fails when the system attributes the transition to authority even though the available evidence establishes another material cause, or cannot establish the cause at all.

The case does not prescribe how a system serializes causal provenance. It only requires that the authority claim not exceed what the evidence establishes.

## DTF-030 preserves unresolved material state

An unresolved material condition is not resolved merely because execution advances.

Workflow progression, repetition, peer agreement, confidence, reputation, or similar non-resolution events cannot replace evidence of an admissible resolution event.

This case is narrower than a general missing-evidence failure because it concerns the lifecycle of a condition that was already positively established as unresolved.

## DTF-031 is distinct from existing lifecycle failures

DTF-004 through DTF-006 address revoked current validity, supersession, and current-versus-historical validity.

DTF-031 addresses the inverse decision-resolution failure: a system preserves an earlier unresolved state after current admissible evidence has positively established resolution.

This matters because fail-closed handling does not justify permanent blocking. Correctness requires reassessment when evidence materially changes.

The case still permits DENY or INDETERMINATE where the claimed resolution is stale, revoked, conflicting, superseded, or otherwise insufficient.

## Cross-repository relationship

The portfolio roles remain separate:

- **TSMM** owns canonical decision-resolution semantics.
- **TIS** can carry portable decision-resolution evidence.
- **DTFC** records reusable falsifiable failure propositions.
- **ARPA / ARA / Interop Lab** can produce executable pressure evidence.
- **RAHP** can assess whether an implementation provides sufficient evidence to demonstrate resistance to the failures.

DTFC does not acquire normative authority over those systems by referencing them.

## Research provenance

The tranche was informed in part by a read-only review of the independent Protocol of Care for Agents project:

- https://github.com/JessHines360/protocol-of-care-for-agents
- https://github.com/JessHines360/protocol-of-care-for-agents/blob/main/BRIEF.md
- https://github.com/JessHines360/protocol-of-care-for-agents/blob/main/experiments/SIMULATION_01_RUNBOOK.md

Those references preserve research provenance. They are not normative dependencies, and no writes were made to the upstream repository.

## Sequencing boundary

DTF-020 through DTF-027 are already reserved by the open v0.3.0 cross-specification seam tranche.

The repository currently requires a contiguous corpus baseline. DTF-028 through DTF-031 therefore MUST NOT merge before DTF-020 through DTF-027 are present and validated. The tranche should remain dependency-blocked rather than weakening the corpus continuity invariant.
