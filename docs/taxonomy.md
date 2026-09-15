# Failure-case taxonomy

The Digital Trust Failure Corpus classifies each case along independent dimensions. These dimensions are deliberately small in v0.1 and should grow only when concrete cases demonstrate a need.

## Domains

A **domain** identifies the part of a digital-trust system in which a failure proposition is materially relevant. A case may span more than one domain.

| Value | Meaning |
|---|---|
| `identity` | Identifier, subject, controller, or identity-state behaviour |
| `credential` | Credential issuance, presentation, verification, or status |
| `trust-registry` | Registry authority, query, recognition, or status evidence |
| `authorization` | Permit/deny decision and authority-to-act behaviour |
| `delegation` | Delegated authority, attenuation, expiry, or downstream delegation |
| `lifecycle` | State transitions, revocation, withdrawal, expiry, supersession, or historical validity |
| `governance` | Governance rules, policy authority, controls, and decision rights |
| `privacy` | Disclosure, correlation, unlinkability, minimisation, or privacy harm |
| `composition` | Failure emerging from combining otherwise valid components or evidence |
| `evidence` | Availability, freshness, provenance, conflict, or interpretation of evidence |
| `agent` | Software-agent identity, authority, relationship, or action behaviour |
| `interoperability` | Cross-system or cross-protocol interpretation and behaviour |

A domain is not a severity rating and does not indicate which specification owns the semantics.

## Failure classes

A **failure class** describes the mechanism or trust-property defect represented by the case.

| Value | Meaning |
|---|---|
| `stale-evidence` | Evidence is older than the state it is used to establish |
| `missing-evidence` | Required evidence is absent or unavailable |
| `conflicting-evidence` | Material evidence sources disagree |
| `authority` | Authority is absent, invalid, withdrawn, or incorrectly attributed |
| `scope-escalation` | Claimed or exercised authority exceeds an authorised scope |
| `lifecycle-state` | Current lifecycle state is incorrectly established or interpreted |
| `historical-validity` | Present and historical validity are incorrectly conflated |
| `false-independence` | Evidence appears independent but resolves to a common controlling source |
| `implicit-transitivity` | Trust or recognition is treated as transitive without an explicit rule |
| `policy-mismatch` | A decision relies on a different policy/version/context than the one asserted |
| `correlation` | Information or evidence creates an unintended cross-context correlator |
| `provenance` | The origin, derivation, or custody of evidence cannot support the claim made from it |

## Dispositions

The core vocabulary has three decision outcomes:

- `PASS`: the proposition is positively established for the consuming decision context.
- `DENY`: the proposition is sufficiently established as unsafe or impermissible for the consuming decision context.
- `INDETERMINATE`: available evidence is insufficient, unresolved, conflicting, or otherwise unable to support PASS or DENY.

For each outcome, a case declares `allowed`, `prohibited`, or `not-applicable`. The schema requires every failure case to permit at least one of `DENY` or `INDETERMINATE`. This prevents a failure case from defining PASS as its only safe outcome.

The corpus does not force a consumer to choose DENY when INDETERMINATE is also safe, or vice versa. That policy belongs to the consuming system unless a cited normative authority requires a particular result.

## Evidence requirement categories

An evidence requirement identifies what must be available to evaluate the failure proposition. It does not prescribe a transport or credential format.

| Value | Meaning |
|---|---|
| `authority-state` | Evidence of who holds or held relevant authority |
| `lifecycle-state` | Evidence of lifecycle state and transition |
| `freshness` | Evidence that a claim or observation is sufficiently current |
| `provenance` | Evidence of source, derivation, or custody |
| `policy` | Evidence of the policy/rule/version governing the decision |
| `relationship` | Evidence of the relevant relationship and its current state |
| `cryptographic` | Evidence established through cryptographic verification |
| `temporal` | Evidence establishing effective, observation, verification, or other relevant time |
| `composition` | Evidence about independence, dependency, or interaction among inputs/components |
| `other` | A necessary requirement not yet justified as a stable taxonomy value |

Use `other` sparingly. Repeated use for the same concept is evidence that the taxonomy should evolve.

## Extension boundary

The core case contract is technology-neutral. Implementation-specific material such as DID methods, credential formats, TRQP operations, ARA relationships, RAHP labels, API endpoints, or vendor-specific telemetry belongs in later bindings/adapters rather than new free-form fields in the core case.

References preserve provenance but do not make a corpus case normative. The authority of a referenced specification, governance framework, implementation, incident report, or paper remains external to this repository.
