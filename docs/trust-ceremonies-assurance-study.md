# When valid Trust Tasks do not establish a legitimate ceremony outcome

*A source-pinned comparative DTFC assurance study*

**Research checkpoint · 25 November 2026 · QBF Consulting LLP · Non-normative · AI-assisted author research**

**Scope:** Three purposively selected analytical ceremony profiles, 13 exact Trust Task versions and 37 frozen canonical DTF propositions. [Issue #168](https://github.com/qbf-consulting/digital-trust-failure-corpus/issues/168) records the research contract. This is a companion to the [representative Consent study](trust-tasks-representative-consent-study.md), not its replacement.

## Executive determination

A valid task response can establish a narrow proposition without establishing the legitimacy or effectiveness of the composed outcome. The central research question is whether an assessor can locate the additional conditions at the relying boundary and identify a counterexample to an unjustified positive determination.

The selected upstream contracts already distinguish several such conditions. The contribution of this study is the operationalization of those distinctions through canonical failure propositions, explicit alternative paths, temporal authority dependencies and falsifiable controls. It is not a claim of novel upstream requirements or defects in those specifications.

Ceremony analysis adds a systematic way to identify and trace composition obligations. It does not have an exclusive ability to detect them. A task-only assessor supplied with the same complete dependency, policy, temporal and effect evidence can reach the same determination. Missing evidence remains indeterminate; a valid refusal can be correct execution.

## Source authority and research design

| Source | Frozen revision and responsibility |
|---|---|
| [Trust Tasks framework](https://github.com/trustoverip/dtgwg-trust-tasks-spec/blob/bdf2cdd9256f9d7b98fe8b40c776124fc27a6084/spec/body.md) | `bdf2cdd9256f9d7b98fe8b40c776124fc27a6084`; canonical framework semantics, including §4.11 ceremony membership and §7.2 independent authorization |
| [Trust Tasks registry](https://github.com/trustoverip/dtgwg-trust-tasks-tf/tree/f21a98ec8383352d18629a08dd5dd23935456142) | `f21a98ec8383352d18629a08dd5dd23935456142`; selected task specifications and schemas, not the authority for framework semantics |
| [VTI composition](https://github.com/trustoverip/dtgwg-vti-spec/blob/83e88fcf8760f6bd159bbac09a27b002f5b656c2/spec/14-composition.md), [membership lifecycle](https://github.com/trustoverip/dtgwg-vti-spec/blob/83e88fcf8760f6bd159bbac09a27b002f5b656c2/spec/12-vtc-lifecycle.md), [approvals](https://github.com/trustoverip/dtgwg-vti-spec/blob/83e88fcf8760f6bd159bbac09a27b002f5b656c2/spec/03b-approvals.md) | `83e88fcf8760f6bd159bbac09a27b002f5b656c2`; separately pinned later draft, no cross-version compatibility asserted |
| [Canonical case baseline](https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/main/research/external-sources/trust-tasks/ceremony-case-baseline.json) | DTFC revision `1eda75842cf3b268361dc47ce8ade23b6a99c5cb`; exact 37 case paths, versions and Git blobs |

The [source and method checkpoint](https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/main/research/external-sources/trust-tasks/ceremony-method-checkpoint.md) documents source authority, schema pins, timing ambiguities and exclusions. The [profile sidecar](https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/main/research/external-sources/trust-tasks/ceremony-profiles.json) binds exact Type URIs, specification/schema blobs and nine alternative paths. The [upstream onboarding definition](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/ceremonies/vtc/member-onboarding/0.1/ceremony.json) is a draft targeting framework 0.4. Its selected versions and completion predicate are not equivalent to our joining profile. The [ceremony receipt contract](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/trust-ceremony-receipt/0.1/spec.md) requires definition resolution and appropriate signed terminal and held-step evidence; a receipt does not grant authority. Its existing [37-case examination](trust-tasks-ceremony-receipt-case-examination.md) remains separate.

### Selection and transferability

Joining, separation and consent-mediated delivery were selected to contrast admission decisions, authority withdrawal and scoped permission under distributed enforcement. Consent also permits exact comparison with #135. The selection is purposive, not randomized or preregistered. The profiles are analytical compositions, not claims to define upstream ceremonies. Group/network departure, reciprocal credentials, other task families and material commitment scenarios without grounded premises remain outside the selected scope.

The historical 1,391-version registry inventory remains available for discovery. It is not the denominator of this study or an exhaustive assessment obligation.

| Profile | Selected task versions (relative Type URI under `https://trusttasks.org/spec/`) | Composition and intended result |
|---|---|---|
| Joining | `vtc/join-requests/manifest/0.4`, `vtc/join-requests/submit/0.3`, `vtc/join-requests/decide/0.1`, `vtc/members/admit/0.1` | Automatic, reviewed or direct admission under applicable policy; current access assessed separately |
| Separation | `vtc/members/self-remove/0.1`, `vtc/members/self-remove-receipt/0.1`, `vtc/members/admin-remove/0.1` | Authorized termination of the same membership; dependent effects and historical evidence separately evaluated |
| Consent | `consent/approver-set/1.0`, `consent/request/1.0`, `consent/approve-request/0.1`, `consent/decision/1.0`, `consent/list/1.1`, `consent/revoke/1.0` | Direct or bridge-attested decision, policy-permitted preauthorization or withdrawal; enforce exact current scope at delivery |

### Four independent determination dimensions

| Dimension | Question | Example |
|---|---|---|
| Local task result | What does this particular exchange establish? | Authenticated application acknowledged; continuation is not terminal success |
| Ceremony execution | Was the applicable path performed correctly? | Required review pending, or automatic path properly complete |
| Outcome legitimacy | Is the exact claimed outcome justified under competent authority? | Membership supported, without inferring unrestricted resource access |
| Effective state | What effects are actually established at the relevant boundary? | Community membership removed; downstream access state unknown |

These are analytical dimensions, not new upstream state names. A ceremony definition differs from its enactment; a task type/version differs from a particular execution. The same valid local result can appear in both negative and control scenarios. A partial effect requires affirmative evidence of differing effects, not simply absent observations.

An informative functional lens, derived from a user-supplied diagram of unknown normative status, is:

```text
Trigger → Gather → Verify → Facts → Evaluate → Verdict → Effects
```

Verified evidence does not automatically establish the relied-upon fact; established facts do not determine applicable policy; evaluation does not establish decision competence; a verdict does not prove the effect. Authority cuts across all functions. They can recur, overlap and span multiple tasks or ceremonies. This is an analytical aid, not a linear execution model.

## Evidence population and dispositions

One cell represents one pinned profile × one canonical case. The author assessment compares exact canonical preconditions, trigger and falsification rules against local and stronger relying propositions. It records missing premises, applicable authority, evidence and expected safe disposition. A conditional candidate is a source-grounded hypothesis requiring stated deployment conditions. Not established means insufficient grounds within the selected profile, not proof of safety.

| Family | Conditional | Not established | Total |
|---|---:|---:|---:|
| [Authority](https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/main/research/external-sources/trust-tasks/ceremony-authority-assessment.json) | 12 | 21 | 33 |
| [Composition](https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/main/research/external-sources/trust-tasks/ceremony-composition-assessment.json) | 11 | 13 | 24 |
| [Lifecycle](https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/main/research/external-sources/trust-tasks/ceremony-lifecycle-assessment.json) | 11 | 1 | 12 |
| [Evidence](https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/main/research/external-sources/trust-tasks/ceremony-evidence-assessment.json) | 24 | 0 | 24 |
| [Privacy](https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/main/research/external-sources/trust-tasks/ceremony-privacy-assessment.json) | 16 | 2 | 18 |
| **Total** | **74** | **37** | **111** |

These are not 111 independent experiments, 74 observed failures, incidence estimates or risk rankings. Author-side adversarial review narrowed 13 initially conditional cells because additional premises were not established: independent corroboration, transitive recognition, material commitment, ambiguous ownership, independent quorum and credential-presentation privacy. The [mechanism synthesis](https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/main/research/external-sources/trust-tasks/ceremony-mechanism-synthesis.md) and [false-success register](https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/main/research/external-sources/trust-tasks/ceremony-false-success-review.md) record the reasoning.

## Worked examples

### Joining: valid application, missing required decision

Under a review-required criterion, a valid application and authentic acknowledgement cannot establish admission before the applicable review. The negative design asserts completion despite missing competent decision. The control uses the same application evidence plus the required decision and authoritative membership record. A separate automatic-path control is important: missing manual review is not a failure when the applicable criterion does not require it. Direct admission is a distinct authorized alternative, not evidence of applicant assent.

DTF-010/022/030 become conditional where their precise missing-evidence, binding/effect and unresolved-condition premises hold. A local task assessor who knows the review criterion can already identify the defect.

### Separation: removal versus downstream enforcement

Self-removal and its receipt can support the community-side transition without establishing every downstream effect. Acknowledgement proves delivery, not universal convergence. An earlier valid dependent authority observation cannot establish current authority after effective withdrawal. Distinguish actual effective removal from acceptance, notification and verifier observation. An independent current grant is a control, not a failure.

DTF-001/003/021/023 require actual dependency and reliance conditions. Historical validity (DTF-006) is a different question from present authorization. A source timing tension in the removal response remains explicitly unresolved; no universal convergence interval is assumed.

### Consent: an authentic decision is not unrestricted permission

A bridge-attested decision has different provenance from a directly signed operator decision. Enrollment and authorized operator choice are material; neither establishes legal representative authority. A receive-only grant cannot justify converse. The authoritative VTA grant must match the platform, opaque conversation reference, kind, agent, action scope and current state. The bridge cache is advisory; the list/1.1 change token is issuer-bound and is not a timestamp.

A recorded deny can be correct execution. Valid preauthorization may omit a challenge where policy permits it. DTF-002 requires actual bounded delegation and reliance, not simply an action outside message scope. The prior Consent research already identified revocation/cache and provenance seams.

### Cross-ceremony trace: the dependence of later reliance

Assume an explicit hypothetical policy P under which membership gives M bounded authority A, M can delegate B within A, and B does not survive withdrawal of A. An independent grant I is outside this dependency.

| Event | Established proposition | Additional evidence required |
|---|---|---|
| Admission | Community legitimately admits M | Applicable criterion and decision, authoritative membership |
| A and B established | M receives A and validly delegates B | Exact scope, competent delegation rule and dependency |
| Earlier check | R observes B as valid | Observation time and action-specific decision |
| Effective withdrawal | Community withdraws A upon departure | Effective event time, actual source loss |
| Notification (separate event) | Removal evidence is delivered | Delivery does not establish every downstream effect |
| Later reliance | R evaluates B for a new action | Current dependency and authority, distinct from cached decision |
| Execution | Action actually occurs, if executed | Execution and impact evidence |

Notification follows removal but may precede or follow the later relying decision. If R wrongly accepts B solely from its earlier observation after effective withdrawal, the negative hypothesis is supported under P. If R denies B on current evidence or authorizes the same action under valid I, the control holds. No actual access, disclosure or harm is inferred. See the [full causal trace](https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/main/research/external-sources/trust-tasks/ceremony-causal-trace.md).

## Comparative findings

The [historical Consent comparison](https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/main/research/external-sources/trust-tasks/ceremony-consent-comparison.json) accounts for 37 rows and 222 prior judgments across six matching task versions. The two canonical revisions have unchanged case paths and blobs, supported by commit comparison and representative direct blob checks. Historical judgments remain author interpretations, not independently accepted evidence.

| Comparison category | Rows | Interpretation |
|---|---:|---|
| Overlap | 14 | Mechanism already identifiable in prior work |
| Conditional extension | 10 | Additional profile-level hypothesis, not demonstrated incremental detection |
| Not established | 10 | Necessary premises not established in the selected scope |
| Scope narrowing | 3 | Earlier interpretation requires qualification for the current profile |

Composition makes missing semantic obligations and causal dependencies easier to enumerate. It is particularly useful where valid local propositions do not establish a stronger outcome across time or components. But #135 already considered stale grants, decision provenance, combined disclosure and retention. Rediscovery is not novelty. Unknown dependency, actual policy or effective state can leave both analytical methods indeterminate.

Privacy must be evaluated at the composed boundary: actual observer, purpose, linkable metadata, retention and authority for secondary use. Individually justified disclosures do not demonstrate joint privacy. Conversely, authorized within-context identification is not itself a privacy violation. Recovery must resolve the specific outstanding condition, not clear unrelated gates. Compensation is a separately authorized action, not assumed atomic rollback.

## Falsification agenda and evidence limits

The [four machine-readable negative/control designs](https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/main/research/external-sources/trust-tasks/ceremony-negative-controls.json) specify exact task references, initial state, actors, policy, intervention, local observations, relying claim, separate determinations, safe disposition and evidence. The [false-success register](https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/main/research/external-sources/trust-tasks/ceremony-false-success-review.md) includes omitted mandatory steps, unauthorized actors, contradictory evidence, stale authority, invalid ordering, optionality, partial effects, purpose overrun, unsupported mappings and source drift.

All deployment scenarios are unexecuted hypotheses. No external implementation behavior, harm or independent semantic acceptance was observed. The later VTI snapshot is comparative evidence, not a cross-version conformance result. Full transitive schema closure and deployment-specific policies, times, privacy objectives and retention necessity are not established. Where upstream already prohibits a behavior, attribute the hypothesis to nonconforming enforcement, not a specification defect.

## Reproduction and contribution

From the repository root, install the existing development dependencies and run:

```bash
python -m pip install -r requirements-dev.txt
python -m tools.validate_ceremony_profiles
python -m tools.validate_trust_tasks_predicate_catalog
python -m tools.validate_consent_case_examination
python -m tools.validate_ceremony_assessment
python -m unittest discover -s tests -v
python tools/validate.py
python tools/build_docs.py
mkdocs build --strict
```

The [matrix validator](https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/main/tools/validate_ceremony_assessment.py) reuses the canonical predicate and profile checks. Its [regression tests](https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/main/tests/test_ceremony_assessment.py) exercise real repository inputs and reject structural false success. At research checkpoint `3007ad7ede422680e7abab8bf41c55b90410c7f1`, [validation](https://github.com/qbf-consulting/digital-trust-failure-corpus/actions/runs/45559574916) passed 435 unit tests including all 22 assessment regressions, 12 graph tests and corpus validation; [documentation](https://github.com/qbf-consulting/digital-trust-failure-corpus/actions/runs/45559575010) passed generation and strict build; [DCO](https://github.com/qbf-consulting/digital-trust-failure-corpus/actions/runs/45559575553) passed. This checkpoint predates the standalone publication commit; it is not evidence of deployment of this page.

To challenge a judgment, identify the exact profile, task Type URI and source pin, canonical case/version, contested premise, competing interpretation and negative/control design. A well-grounded disproof is a valuable contribution. For actual execution evidence identify implementation/version, configuration, policy, event sequence, observation boundary, expected/actual result and privacy-safe reproduction material. Follow the repository [contribution guidance](https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/main/CONTRIBUTING.md); do not disclose sensitive deployment data.

## Close-out disposition

The bounded research result is three analytical profiles, 13 task versions, 37 canonical propositions, 111 judgments (74 conditional and 37 not established), four negative/control designs and ten challenge classes. The method exposes semantic seams without claiming exclusive detection, and permits negative findings and narrowing. Canonical cases and historical Consent judgments are preserved. No broader catalogue expansion is justified without a separate concrete research proposition. Pages publication is the intended consumption surface; no versioned release is warranted for this increment. Publication and final acceptance evidence remain tracked in #168.
