# Ceremony assessment: causal trace and determination contrasts

Issue #168; author-side, AI-assisted analytical scenarios, not executed experiments or observed harms. Profile blob feff06fe825f44af02ae468d17630060e61a0621; registry f21a98ec8383352d18629a08dd5dd23935456142; VTI draft 83e88fcf8760f6bd159bbac09a27b002f5b656c2. Canonical bindings and complete predicates remain in the five family sidecars and frozen baseline. No new cases or independent observations are introduced.

## Determination contrasts

Evaluate the scoped proposition, not a generic ceremony PASS. The following scenarios stipulate observations for comparison; no actual target was exercised.

| Scenario | Local result | Ceremony execution | Outcome legitimacy | Effective state | Reason and control |
|---|---|---|---|---|---|
| J1 reviewed admission, eligible applicant, live competent approver, recorded admission and current scoped access | submit refer; decide approved | satisfied | supported | established for the stipulated access | Require original criterion, actual decision, membership record and current access evidence. No inference from receipt alone. |
| J2 review-required criterion; valid application and authentic acknowledgment, no required review | local exchange succeeds | violated if asserted complete; pending if honestly awaiting review | indeterminate for admission | not established | A missing required step is an execution defect only if completion is claimed or applicable requirement violated. DTF-022/023/030 conditional; automatic criterion is a control, not an omitted-review defect. |
| J3 independent competent direct admission valid under its own policy; subsequent required notification fails | admit succeeds; delivery fails | violated for a deployment-specific ceremony requiring delivery | supported for community-side membership only | established for membership; access separately evaluated | Admit/0.1 permits best-effort delivery. A stricter notification requirement is hypothetical deployment policy, not a task conformance requirement. If policy makes notification constitutive, legitimacy is not supported. Do not substitute a different path retrospectively. |
| S1 authorized self-removal; competent removal and status evidence; downstream service still permits withdrawn dependent authority | removal and receipt delivery succeed | satisfied for community-side removal path; violated at downstream enforcement if applicable requirement breached | supported for departure; contradicted for subsequent dependent access | partially effective for combined outcome | DTF-001/003/021/023 conditional; local success cannot justify later access. Independent grant control below. |
| S2 valid receipt acknowledgment but actual downstream observation unavailable | acknowledgment succeeds | satisfied only for delivery; indeterminate for wider effect contract | indeterminate for wider effect claim | indeterminate | DTF-010/026/027 conditional. Missing evidence does not establish divergence. |
| C1 authorized current receive grant, exact subject; bridge forwards permitted content | request and decision succeed | satisfied | supported for receive action | established for stipulated delivery | Check exact scope and authoritative state; no inference of general processing rights. |
| C2 valid recorded receive grant; bridge replies on behalf of agent despite receive-only scope | request, decision and sync locally succeed | violated at delivery enforcement; satisfied for recorded grant exchange | contradicted for reply | intended legitimate effect not established; actual unauthorized reply stipulated as a distinct observed-state variable in this hypothetical | DTF-002 conditional only if actual bounded delegation and reliance established; otherwise scope violation without that mapping. Valid local execution and invalid relying outcome coexist. |
| C3 approved decision is deny | recorded success response | satisfied | not-requested-or-refused for allow claim | established safe non-delivery if observed | Correct refusal is not failed execution. |
| C4 bridge attestation verifies but operator choice or issuer authorization is unestablished | proof verifies; substantive decision unverified | indeterminate | indeterminate | indeterminate absent observation | DTF-010/027 conditional; legal representative authority never inferred from bridge provenance. |

J3 is deliberately conditional on a policy that separates a notification obligation from membership validity. It is not an upstream normative finding. These contrasts show why execution, legitimacy and actual effect must remain separately scoped. Where an upstream requirement explicitly prohibits the behavior, classify nonconforming enforcement rather than a specification defect. A policy-permitted alternative is not a defect.

## Cross-ceremony path: admission, delegated access, separation, reliance

Actors: community C, member M, delegate D, relying service R. Hypothetical policy P grants M scoped authority A only while membership is active and permits bounded delegation B to D within A. No survival rule applies to B. Independently granted authority I, if any, is outside this dependency. This policy and the actual delegation are necessary premises, not asserted universal VTC semantics.

| Event label (not a total-order index) | Origin or propagation event | Evidence required | Competent owner / relying proposition |
|---|---|---|---|
| t0 | C publishes applicable criterion; M applies under manifest/0.4 and submit/0.3; eligible administrator decides under decide/0.1 for reviewed path | criterion digest/grace, VP/proof, decision, membership record | C: admission legitimate under P |
| t1 | C establishes membership-derived A; M delegates bounded B to D | live access-control entry, exact scope, delegation chain and rule permitting delegation; VTI-ACL-037,070–073, VTI-CMP-050–053 | C and competent delegation authority: B valid only while its source and scope hold |
| t2 | R evaluates B and caches valid result | observation time, evaluated action and policy, current source status | R: earlier authorization observation, not indefinite grant |
| t3 | M initiates self-remove/0.1; C executes removal | authenticated initiator, disposition, effective membership transition, credential status and actual source-authority withdrawal | C: departure and withdrawal of A, separately established |
| n | C sends self-remove-receipt/0.1 after effective removal; delivery is acknowledged | competent receipt assertion, delivery record; separate observation of dependent effect | C/recipient: reported removal and delivery; no universal downstream completion claim |
| t5 | D attempts action within former B; R relies solely on t2 cached decision | exact action, reliance time, stale input, missing current source check, decision result | R: current B authority not established after A withdrawn; conditional false PASS |
| t6 | R executes action, if it actually does so | execution log, affected resource, actual consequences | R: potential unauthorized access becomes observed only if independently evidenced |

Required ordering: t0 < t1 <= t2 < effective withdrawal t3 < t5 <= t6. Receipt delivery t4 may precede or follow t5; authority effect time is not notification time. Request acceptance is not necessarily t3. No assumption that a credential status bit alone proves every derived grant withdrawn. No universal propagation interval is invented. The source timing ambiguity for self-remove response remains bounded.

### Failure origin, propagation, decision and harm

Origin: competent withdrawal of A is a legitimate event, not itself a failure. Candidate failure may originate in dependency maintenance (B remains incorrectly live), propagation (missing status update), or R's enforcement (freshness/source check omitted). These alternatives require distinct evidence. Propagation: earlier valid B result continues to circulate or remain cached. Relying decision: R converts historical authorization into current permission without checking source dependency. Potential consequence: D accesses a resource outside current authority; actual access, disclosure or harm must be separately evidenced.

Canonical conditional anchors: separation DTF-001 (earlier authority evidence after effective withdrawal), DTF-003 (dependent delegation after source loss), DTF-021 (earlier check reused later), DTF-004 only if a previously valid artifact was authoritatively revoked and accepted as current, DTF-029 only if a decision transition caused by evidence arrival is mislabeled an authority event. DTF-006 concerns a distinct historical query, not current permission. Do not count these as independent observed failures.

### Causal alternatives and controls

- Independent grant I or explicit competent preservation rule: evaluate I and exact action independently; departure is not blanket revocation.
- Withdrawal not yet effective: evaluate actual applicable authority and policy, not request submission time. Legitimate pending convergence is distinct from a prohibited post-effect PASS.
- R receives authoritative evidence before reliance and denies B: no false PASS; propagation delay alone is not the candidate relying failure.
- Source unavailable at t5: indeterminate current authority; apply governing disposition, not last-known PASS.
- Historical inquiry at t5 about t2: assess historical validity under then-applicable rules; current withdrawal is not retroactive invalidity.
- Valid resolution evidence arrives for a specific pending effect: update that condition; keep independent unresolved conditions. DTF-030 and DTF-031 are complementary.
- Actual action never executes: unsafe decision may still be a candidate failure; no resulting access or harm inferred.

### Incremental explanatory value

Hold local observations fixed: valid admission decision, earlier authorized B observation, valid removal assertion and receipt. A task-only reading of these artifacts establishes their respective local propositions. The cross-ceremony trace makes the dependency A → B, effective withdrawal time and later relying proposition explicit. That is a useful analytical addition, not a newly discovered normative requirement: VTI-CMP-040–042 and 050–053 already require current evidence and delegation continuity. A task-only assessor supplied the same complete dependency, temporal and policy evidence can reach the same result. No claim that only a ceremony-aware engine can detect the failure.

## Evidence boundary

All scenarios are constructed, not observed. Source-qualified author assessment only. The contrasts and trace do not expand the 111-cell denominator. Exact #135 comparison and integrated privacy/conflict/recovery synthesis are separate companion artifacts. No external observations or independent review.
