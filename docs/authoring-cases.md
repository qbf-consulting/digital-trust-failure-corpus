# Authoring failure cases

A Digital Trust Failure Corpus case describes a bounded failure proposition that can be evaluated from explicit evidence and challenged through a falsification condition.

## Start from the failure, not the technology

Write the proposition so that it remains meaningful across implementations. A case may later be bound to a DID method, credential format, trust-registry protocol, agent framework, or assurance tool, but the core case should describe the trust failure itself.

Good framing:

> A relying system must not treat evidence as current when required freshness cannot be established.

Avoid framing the core case as a product- or protocol-specific API failure unless the failure genuinely exists only in that implementation.

## Required structure

Each case must contain the fields required by `schemas/failure-case.schema.json`.

### `id`, `title`, `version`, `status`

Use a stable `DTF-NNN` identifier and a lowercase hyphenated canonical title. Case versions use semantic-version syntax. New cases normally begin as `draft`.

### `domains`

Domains identify where the case is materially relevant. They do not assign ownership or severity.

### `failure_classes`

Failure classes describe the mechanism or trust-property defect. Reuse existing vocabulary before proposing an extension.

### `proposition`

State what a relying system must not incorrectly infer, accept, or represent. The proposition should be understandable without reconstructing a particular codebase.

### `preconditions` and `trigger`

Preconditions establish the facts necessary for the failure proposition. The trigger identifies the relying action or evaluation that exposes the failure.

### `expected.dispositions`

The v0.1 core uses `PASS`, `DENY`, and `INDETERMINATE`, each classified as `allowed`, `prohibited`, or `not-applicable`.

A failure case must permit at least one of DENY or INDETERMINATE. When evidence does not justify choosing between those outcomes, allow both rather than inventing universal policy.

### `evidence_required`

List the evidence needed to evaluate the proposition. Describe the semantic requirement, not a preferred transport or credential format.

### `falsification`

State observable conditions that would demonstrate unsafe handling. A falsification condition should make it possible to build a negative, regression, contract, or interoperability test.

### `references`

References preserve provenance and context. They do not automatically become normative authority. If a normative source requires a specific outcome, make that relationship explicit in the case or associated judgment trail.

## Evidence discipline

Missing evidence is not PASS. Unresolved conflict is not PASS. Unknown freshness is not current evidence. A schema-valid case is not necessarily a correct case.

Where a safe outcome depends on consumer policy, use the disposition map to preserve that uncertainty rather than hiding it.

## Extensions and bindings

Do not place implementation-specific convenience fields into the core schema. A future binding may map a DTF case to protocol messages, API calls, test vectors, fixtures, or implementation-specific expected outputs.

Schema extension is justified only when multiple concrete cases demonstrate that an important technology-neutral proposition cannot be represented faithfully with the existing contract.

## Privacy and incident material

Do not place confidential, personal, regulated, or non-public incident data in a corpus case. Generalise the proposition and use public provenance when possible. Security-sensitive findings should follow `SECURITY.md` rather than being disclosed through a public case or issue.
