# Trust Tasks × DTFC: source-specific semantic challenge (18 November 2026)

**Status:** author-side adversarial research, not independent review or exhaustive case-level acceptance.  
**Tracking:** [#135](https://github.com/qbf-consulting/digital-trust-failure-corpus/issues/135).  
**Upstream pin:** `trustoverip/dtgwg-trust-tasks-tf@f21a98ec8383352d18629a08dd5dd23935456142`.  
**DTFC baseline:** existing canonical cases on the repository revision accompanying this report. No canonical case is changed.

## Purpose and decision discipline

This is a bounded attempt to falsify or narrow three published preliminary mappings by checking the task's explicit guarantees against the **whole proposition and preconditions** of the corresponding existing DTFC case. It is not a substitute for the 37-case examination of every task version. It does not increase the 51 source-screened version numerator or the count of independent accepted reviews.

A boundary test is only a hypothetical test until run on an identified consuming implementation. A source-defined safeguard must not be represented as an upstream defect. Conversely, correct task-level conformance does not establish that the downstream consumer uses the result safely.

## Challenge 1: audit/verify/0.1 and DTF-010

**Sources:** [task specification](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/audit/verify/0.1/spec.md) (Abstract, Conformance, Security & Privacy); [DTF-010](../corpus/evidence/DTF-010.json).

**Existing candidate:** `mechanism-overlap` for a consumer interpreting `verified: true` as complete, externally authentic audit evidence.

**Adversarial finding:** The task already requires `legacySkipped` and `unparseableSkipped` counts and explicitly warns that `verified: true` is an internal consistency result, not authenticity or verification of skipped records. A claim that the task omits these safeguards is contradicted by the upstream source. DTF-010 applies conditionally only when a downstream proposition requires evidence absent from the returned verification, and the consumer nevertheless returns PASS. If the auditor declines to assert completeness or authenticity, the canonical case's trigger is absent.

**Candidate boundary test, unexecuted:** Supply `verified: true` with a nonzero skip count, or a consistent restamped/truncated chain lacking an independently anchored head. Compare (a) a consumer that asserts full provenance/authenticity PASS and (b) one that limits its claim to the verified subset's internal consistency and requests independently anchored evidence. The former is a candidate false PASS; the latter is not. Specify the auditor's required evidence policy before calling this a failure.

**Disposition:** Retain **conditional candidate**, with narrower downstream-only scope. Not an independently reviewed mapping; no execution evidence.

## Challenge 2: governance/capability/list/0.1 and DTF-010 versus DTF-018

**Sources:** [task specification](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/governance/capability/list/0.1/spec.md) (Request, Response, Security & Privacy); [DTF-010](../corpus/evidence/DTF-010.json); [DTF-018](../corpus/authority/DTF-018.json).

**Existing candidate:** `DTF-010` (`adjacent`) because `available` is not `enabled`.

**Adversarial finding:** The spec explicitly defaults an absent status filter to `enabled`; `available` is an affirmative capability-management view, not a claim of present enablement. Therefore **mere receipt of an `available` entry does not meet DTF-010**. To establish that case, a consuming decision would have to require effective enablement evidence, lack it, and still return PASS. By contrast DTF-018 may be a more precise competing candidate if a consumer converts the advertised capability into authority for a material commitment without principal-derived authorization. That alternative still requires evidence of an actual material commitment and insufficient authority.

**Candidate boundary test, unexecuted:** Return a valid `available` entry for a disabled capability; try a consequential operation without principal authority. Independently observe whether the consumer (1) wrongly infers enabled state in absence of required evidence (DTF-010 preconditions) or (2) substitutes capability advertisement for authorization (DTF-018 preconditions). Reject a test result that fails to distinguish these mechanisms.

**Disposition:** Retain existing DTF-010 as **conditional adjacency only**; record DTF-018 as an **unadmitted competing hypothesis**, not a new accepted mapping. No exhaustive case search or reviewer approval.

## Challenge 3: trust-task-discovery/0.4 and authority, freshness, privacy

**Sources:** [task specification](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/trust-task-discovery/0.4/spec.md) (Conformance, Acceptance window); [DTF-018](../corpus/authority/DTF-018.json); [DTF-021](../corpus/composition/DTF-021.json); [DTF-034](../corpus/privacy/DTF-034.json).

**Existing candidate:** DTF-021 (`adjacent`), because a previously discovered acceptance policy can become stale.

**Adversarial finding:** The task says discovery is advisory, requires consumers to apply the full subsequent acceptance pipeline, forbids acting on unauthenticated discovery, and treats `requiredExt` as **untrusted input** that must not cause a producer to gather or disclose additional data. These are explicit normative safeguards, not vulnerabilities. A later execution relying on stale discovery rather than a fresh material decision may satisfy DTF-021's preconditions; simply using discovery within its intended advisory scope does not. A discovery-supported type also cannot confer principal-derived authorization, creating a conditional DTF-018 hypothesis.

The `requiredExt` safeguard creates a **distinct policy/disclosure challenge** worth testing: whether an untrusted extension request can cause the producer to attach data outside its own policy. **Do not automatically map this to DTF-034.** That case requires an initially legitimate disclosure followed by materially different *secondary* processing. First-time over-disclosure induced by `requiredExt` does not, without further facts, satisfy that existing proposition.

**Candidate boundary tests, unexecuted:** (a) Replay a previously authenticated discovery response after material policy change, then verify the later consumer evaluates current conditions; (b) return a supported type to an unauthorized actor and verify that authorization remains separate; (c) advertise a required extension namespace the producer's policy does not authorize and verify that the producer declines rather than collects or attaches it.

**Disposition:** Retain DTF-021 conditional adjacency; DTF-018 and the `requiredExt` policy boundary are **competing research hypotheses**, not adopted mappings. DTF-034 is **not established** for the first-time over-disclosure scenario. This is **not** a task-wide 37-case no-match.

## Cross-cutting result for DTG / Trust Tasks

The three challenges point to a more discriminating test architecture: **(1) upstream task contract, (2) consumer's claimed proposition, (3) required independently authoritative evidence, (4) material decision boundary, (5) observed consumer response**. A failure proposition applies only when the complete canonical preconditions and trigger are satisfied. Upstream text may already prohibit the dangerous behavior; the research target is then consumer interpretation or enforcement, not a specification defect.

The distinction is useful for DTG because it permits a test implementer to build both a rejection case and a non-failure control without relabelling a correctly constrained task as defective. It is useful for Trust Tasks because it identifies where extension policy, discovery semantics and audit completeness depend on downstream governance.

## Evidence limits and next admissible step

These are **author-side adversarial counterchecks** over three previously source-screened versions. They do not establish independent judgment, target execution, historical equivalence, all-case disposition or quantitative completion of Gate B. The inventory remains 1,391; 51 versions remain preliminarily source-screened; 1,340 require source-specific screening; exhaustive 37-case semantic acceptance remains unestablished.

The next substantive Gate B records must evaluate the *complete* canonical case set for an exact version, preserving reasoned rejection of competitors and a genuine no-match only after full case consideration. Gate C should repeat the challenge from source and canonical propositions, not from the author's mapping summary; contested outcomes remain unresolved. Gate A remains the existing pinned reconciliation. No completeness release or closure of #135 follows from this report.
