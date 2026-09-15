# Authority tranche observations

The first authority cases expose several recurring questions that belong outside the Digital Trust Failure Corpus core schema. They are recorded here as research signals rather than as normative requirements.

## Trust Lifecycle Event Model

The authority cases depend on distinctions that a lifecycle model should eventually make explicit:

- the time an authority-state event occurs;
- the time that event becomes effective;
- the time evidence of that event is observed;
- the time a relying decision is made;
- whether the question concerns current authority or historical authority;
- whether revocation, withdrawal, replacement, expiry, and supersession have distinct semantics.

DTF-001 demonstrates why historical validity and current validity must not be collapsed. DTF-003 demonstrates that a dependent delegation needs an explicit relationship to the lifecycle of its authority source.

## Executable Governance Profile

The cases suggest machine-testable governance propositions around:

- which authority source is competent for a scope;
- how delegated scope is bounded and attenuated;
- whether downstream delegation is permitted;
- what evidence freshness is required for a decision;
- what safe outcome applies when authority evidence cannot be established;
- whether a rule explicitly preserves authority after a lifecycle event for a bounded context.

The corpus should not own those policies. It should remain capable of testing the failures that arise when such policies are absent, contradicted, or incorrectly executed.

## Trust Infrastructure Observability Model

The cases suggest that operators may eventually need observable evidence for:

- age of authority evidence used in decisions;
- effective time and observation time of authority-state changes;
- propagation delay between authority-state change and relying-system awareness;
- count and rate of decisions resulting in unresolved authority state;
- scope-escalation rejection events;
- dependent delegations evaluated after upstream authority-state changes.

These are candidate observability requirements, not yet metric or telemetry specifications.

## Judgment boundary

These observations are deliberately downstream signals. They must not be converted into new fields in the failure-case schema merely for convenience. A new schema field should be justified by repeated corpus needs that cannot be represented with the existing technology-neutral contract.
