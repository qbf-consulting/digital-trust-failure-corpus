# When a consent task succeeds but the relying decision fails
*A source-pinned, purposively selected analytical case study*

**Research checkpoint · 24 November 2026 · QBF Consulting LLP · Non-normative**

**Scope:** Eight pinned `consent/*` task versions in the [Trust Tasks registry](https://github.com/trustoverip/dtgwg-trust-tasks-tf/tree/f21a98ec8383352d18629a08dd5dd23935456142), at upstream commit `f21a98ec8383352d18629a08dd5dd23935456142`. **DTFC authority:** [37 canonical failure propositions](corpus/index.md). **Reproducible evidence:** [296 case/version judgments](https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/main/research/external-sources/trust-tasks/consent-case-examination.json), [source-specific consent screening](https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/main/research/external-sources/trust-tasks/consent-review.json), [review method](trust-tasks-review-method.md). [Full per-task examination](trust-tasks-consent-case-examination.md).

## What was examined, and why it matters

The question is not whether a signed consent task can be validated in isolation. It is whether a consuming system can legitimately advance from the **narrow proposition evidenced by that task** to a later authorization, delivery, or governance decision. This study uses DTFC's existing failure propositions to identify the exact point where a valid local result may be over-interpreted. It asks what additional evidence or enforcement must be present at that point and what counterexample would expose an unjustified PASS.

**Research design at a glance**

| Element | Deliberate design choice |
|---|---|
| Research type | Retrospective, purposively selected, documentary semantic assessment |
| Source population | Source-pinned upstream Trust Tasks registry; **not** an empirical sample of deployments |
| Selected study unit | Each of eight versioned Consent task contracts, including their payload-schema constraints |
| Comparative unit | One pinned task version × one of 37 versioned canonical DTF propositions |
| Analysis produced | 296 source-bound author judgments, each conditional-candidate or not-established-from-task |
| Adversarial component | Proposed negative/control pairs at concrete consumer boundaries, **not executed tests** |
| Validation performed | Provenance, schema, cardinality, case-version and research-sidecar checks in repository CI |
| Evidence not obtained | Independent semantic acceptance; observed external VTA/bridge behavior; incidence or risk magnitude |

The unit of analysis matters: **296 comparisons are not 296 independent experiments**. A recurring mechanism across two versions or related operations may produce multiple cells without providing additional independent evidence of a failure.

## Executive determination

The most consequential boundary in the selected family is **the difference between a valid local consent task result and a justified later permission to deliver or act**. A prompt may have been routed, a bridge may legitimately attest an operator choice, a grant may have been stored, or a synchronization request may have completed. None of those facts alone establishes that the exact conversation, actor, scope and authority remain permitted at the eventual delivery or execution boundary.

The eight published source versions explicitly provide safeguards for several of these seams. This study is therefore **not** a finding that the Trust Tasks specifications are defective. It identifies conditional failure propositions a *consuming implementation or composition* could get wrong even when an individual exchange is syntactically conformant. The central assurance challenge is whether the consuming system can support the stronger proposition it asserts with current authority, decision provenance, complete evidence, and enforceable purpose and lifecycle controls.

This representative assessment is deliberately bounded. It does **not** claim exhaustive applicability coverage of the 1,391 pinned registry versions. The wider registry inventory is retained for source discovery and future voluntary studies, without being treated as a research-completion denominator or project deliverable.

## Selection rationale and transferability

The family was chosen **after** the inventory and existing author-side family studies were available, not through preregistered sampling or a randomized selection. Two considerations drove the choice. First, the Consent family already contained a complete and source-pinned 37-case assessment for every one of its eight versions, allowing the synthesis to be evidence-led rather than manufactured to fill coverage gaps. Second, it crosses several non-collapsible semantics: administrator competence, operator choice, bridge enrollment, grant creation and withdrawal, distributed enforcement, and information retention. It also includes an explicit version break in incremental synchronization. That combination makes it a compact demonstration of where local validation and downstream reliance differ.

The selection was not based on a claim that Consent is the **highest-risk**, most prevalent, or typical Trust Tasks family. Audit, capability governance, task consent, discovery, and ceremony receipt already have their own author-side examinations and would each illuminate different boundaries. Choosing Consent emphasizes multi-party approval and asynchronous enforcement; it correspondingly under-represents mechanisms such as audit-chain completeness, ceremony terminal evidence, or registry historical-state semantics. Those omissions delimit **transferability**, not findings of non-applicability.

**Selection criteria:** complete pinned family membership; full existing canonical case accounting; meaningful cross-component reliance; a demonstrable version-specific distinction; and sufficient negative/control hypotheses to challenge without inventing implementation evidence. A future family study should document its own purpose and why existing Consent findings cannot answer that question before undertaking another full matrix.

## Evidence population and assessment states

The selected corpus consists of the exact eight Consent task versions, each considered against every existing canonical DTF case. No additional speculative mappings were generated for this synthesis. **It is not a statistically representative sample**: repeated judgments for closely related operations or versions are dependent observations, not independent evidence that failure is more likely.

| Pinned task version | Role in the consent system | Conditional case judgments | Cases not established from task alone |
|---|---|---:|---:|
| `consent/approve-request/0.1` | Route approval prompt and challenge | 8 | 29 |
| `consent/approver-list/1.0` | Read scoped approver bindings | 6 | 31 |
| `consent/approver-set/1.0` | Establish approver routing | 7 | 30 |
| `consent/decision/1.0` | Submit decision with direct or bridge-attested provenance | 9 | 28 |
| `consent/list/1.0` | Sync local grant cache, original token format | 8 | 29 |
| `consent/list/1.1` | Sync local grant cache, changed token format | 8 | 29 |
| `consent/request/1.0` | Hold content pending consent | 7 | 30 |
| `consent/revoke/1.0` | Withdraw authoritative grant | 8 | 29 |
| **Total** | **8 exact source versions × 37 canonical cases** | **61** | **235** |

The 61 conditional cells are **not 61 vulnerabilities, incidents or independent findings**: several express the same mechanism across different versions or steps. The 235 `not-established-from-task` results indicate that complete canonical failure preconditions were not established by the isolated task source. They do not establish deployment-level safety or independently reviewed no-match.

## Design of the analytical experiment

This is an **analytical experiment over published task contracts and DTFC propositions**, not a laboratory or field experiment on running systems. Its central test is whether evidence that establishes proposition *P* can be mistakenly used to justify a stronger proposition *Q*. The analysis proceeds as follows:

1. **Freeze the evidence baseline.** Use the upstream Trust Tasks commit and exact specification/schema Git blobs listed in the [Consent research sidecar](https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/main/research/external-sources/trust-tasks/consent-case-examination.json). Use the existing, versioned canonical DTFC case files as the source of each failure's preconditions, triggering condition and falsification rule.
2. **Extract the task's supported proposition.** Identify the parties, request and response semantics, authorization obligations, temporal requirements, evidence provenance and allowed side effects. A successful response is interpreted within these boundaries, not as an unconditional downstream authorization.
3. **Compare each canonical case individually.** Ask whether the task text by itself supplies all material preconditions. If a plausible unsafe consumer interpretation could supply the remaining premises, record a `conditional-candidate` and its specific boundary and negative test. Otherwise record `not-established-from-task` with its bounded rationale; this is not proof the case cannot arise in a composed deployment.
4. **Challenge competing interpretations.** For a candidate, articulate the stronger relying claim, the missing or stale evidence, a false-success scenario, and a corresponding controlled safe outcome. Where an upstream contract already prohibits the behavior, attribute the risk to nonconforming enforcement or unsafe composition rather than to a missing specification rule.
5. **Respect versioned differences.** Do not silently reuse a 1.0 consent-list inference across 1.1's renamed, issuer-controlled synchronization tokens. A coincidentally identical case disposition is not sufficient evidence of full semantic equivalence.
6. **Keep assurance dimensions separate.** Repository validation can confirm evidence structure, exact source bindings and count reconciliation. It cannot independently judge interpretive correctness or supply observations from a VTA, bridge or relying system.

The comparison outputs existed before this consolidated report. The consolidation did not conduct additional external experiments or add new canonical propositions. The negative/control scenarios below are **proposed falsification designs**, and the word “test” refers to their executable hypotheses, not evidence of having run them.

### Worked example: a revocation after an authorized delivery grant

**Starting conditions:** A VTA maintains an authoritative `allow` grant for a particular agent/conversation/scope; an enrolled bridge previously synchronized it into a local cache. **Intervention:** The grant is revoked at the VTA before a later message is eligible for release, while the bridge retains its old cache entry. **Question at the relying boundary:** Does the bridge release the message solely because its earlier synchronization succeeded?

The relevant task-level outcomes may both be valid: the earlier list response accurately described a past grant and the revoke operation accurately withdrew it at the VTA. A subsequent delivery PASS using only stale cached authority would require additional evidence that the grant remained effective, which the old list result does not provide. This is a conditional DTF-001/DTF-021 failure mechanism **if** the actual consumer makes that later authorization decision and lacks a sufficient freshness or enforcement rule. It is not a finding that a particular bridge has done so.

**Negative case:** Revoke, preserve a stale local `allow`, attempt delivery, and observe whether the consuming boundary wrongly permits it. **Control:** Repeat after refreshed authoritative state or an applicable currentness mechanism, and require denial or safe deferral. Preserve exact timestamps, token issuer, policy context, cache state and request scope. A PASS in a synthetic mock would show behavior of that mock, not actual deployment incidence.

## 1. Actor identity, administrative competence and approval authority are separate

`consent/approver-set` permits a context administrator to set the approver routing for a platform/context. A valid signature establishes attribution, but the authorization question is whether the signer is competent for that context. An unauthorised actor must not redirect approval requests by presenting an otherwise valid proof. `approver-list` is likewise a scoped read, not a transfer of authority over every binding it can disclose.

This distinction becomes more consequential in `consent/decision/1.0`, where the task accepts both directly signed operator decisions and a weaker **bridge-attested** choice. An enrolled bridge's evidence of the operator's choice has its own legitimacy conditions; it must not be described as the operator's independent non-repudiable signature. That is not a criticism of allowing multiple modes. It is a requirement to preserve their different evidentiary claims in downstream decisions.

**Conditional DTFC seams:** DTF-002 (scope of delegated authority), DTF-013 (signature versus action authority), DTF-023 (component versus composition validation), DTF-027 (workflow success versus assurance), DTF-028 (non-authoritative signals laundered into authority).

**Negative/control pair:** An actor signs an approver-set request but lacks context-administrator competence; a VTA rejects the change. A competent administrator sets the same binding and succeeds. For a consent decision, accept a properly scoped enrolled bridge's attestation only as bridge-attested evidence, then reject a decision from an unenrolled bridge or a source whose decision provenance is misrepresented.

## 2. Request acceptance and prompt delivery do not establish consent

`consent/request/1.0` routes requests through an enrolled bridge while messages remain held in **default-deny**. `consent/approve-request/0.1` authenticates an approval prompt with a single-use challenge. A successful request or prompt establishes that the process advanced, not that the correct operator approved the intended subject, scope and action. Neither a transport acknowledgment nor an `accepted` workflow response is an authorization grant to release content.

The relying decision must bind the *actual recorded decision* to the relevant conversation subject, operator, challenge and scope, and still establish that the grant is current when content is delivered.

**Conditional DTFC seams:** DTF-010 (required evidence missing), DTF-017 (approval bound to stale/wrong action), DTF-023 and DTF-027 (local success elevated into composed assurance).

**Negative/control pair:** Deliver a valid prompt and deliberately omit the corresponding signed decision; an inbound message remains held. Repeat with a valid recorded `allow` for the exact subject, scope and challenge, and confirm the current authoritative grant before release. An authenticated but unmatched or expired approval must not be treated as equivalent.

## 3. Revocation is authoritative; a bridge cache is not

The most operationally important seam links `consent/list` and `consent/revoke`. A bridge may persist a locally cached grant to enforce steady-state inbound traffic. A VTA revocation changes authoritative permission and signals bridges, but a successful revoke response **does not prove that all distributed caches have converged**. A consumer that continues delivery based on a formerly valid cached `allow` can cross the authority and temporal boundary even though each local operation returned success.

The two list versions must be interpreted separately. Version 1.0 uses request `since` and response `cursor`. Version 1.1 uses `syncToken` and `nextSyncToken` and expressly requires that a consumer not accept a token it did not issue. The token denotes a **change-stream position**, not a pagination position or timestamp. Silently reusing 1.0 field semantics in a 1.1 consumer can conceal material changes. This is a concrete version-specific assurance condition, not a reason to assume a whole-family defect.

**Conditional DTFC seams:** DTF-001 (stale evidence after revocation), DTF-010 (missing grant evidence), DTF-011 (unverifiable currentness), DTF-021 (earlier lifecycle check reused later), DTF-026 (incomplete evidence interpreted as complete). Whether any canonical failure actually occurs depends on the consumer's asserted reliance and the deployment timing.

**Negative/control pair:** Allow a conversation, populate a bridge cache, revoke at the VTA, then attempt delivery from the stale cache. The safe result is denial or deferral pending current authoritative grant state. For 1.1, supply a fabricated or wrong-issuer sync token; the VTA refuses it instead of returning an empty delta that could be mistaken for “nothing changed”. Separately validate that a genuine issued token produces the expected bounded update.

## 4. Privacy survives only when the relying purpose and retention remain bounded

The family uses opaque conversation references and route hints, which limit direct exposure but do not guarantee unlinkability. A persistently cached combination of agent identifiers, conversation references, platform tags and grant/decision timestamps may create a joinable communication graph. Legitimate oversight, delivery and enforcement can each produce derivative records that are subsequently reused outside their original purpose.

The relevant question is not simply whether a consent task exposes a plaintext personal identifier. It is **whether a downstream processor can justify the purpose and retention of the combined records**. A successful permission check does not authorize independent profiling or indefinitely retain a detailed conversation history.

**Conditional DTFC seams:** DTF-034 (secondary use outside purpose), DTF-036 (composition of individually acceptable disclosures), DTF-037 (retained verification artefacts as durable correlation surface).

**Negative/control pair:** Complete the authorized delivery process using only the scoped grant evidence. Then join legitimately obtained decision histories across otherwise unrelated groups and attempt member scoring or indefinite retention. The second action must have its own governance and legal basis; the earlier permission is not a substitute for that basis. A source-level privacy observation is not an empirical privacy test of a deployment.

## 5. Distinguish what each successful task establishes

| Observed local outcome | Supported proposition | Unsupported stronger conclusion without further evidence |
|---|---|---|
| Signed approver-set succeeds | A routing binding was established by the competent context actor | The binding itself confers arbitrary approval or message access |
| Approval prompt accepted | An authenticated prompt was routed | An authorized operator approved the requested action |
| Bridge-attested consent decision accepted | An enrolled bridge reported a choice according to its contract | The operator personally signed that decision |
| Grant list returned | Grants visible to the caller were returned for the stated scope and sync state | No unobserved revocation or concurrent contrary decision exists |
| Revocation succeeds | The authoritative grant was withdrawn | Every distributed enforcement cache has already converged |
| Valid proof or schema | The local evidence or exchange passed its applicable local checks | The later relying operation has current, purpose-scoped authority |

**This separation is the study's main result:** verification of *one* proposition does not supply the missing evidence for a *different*, stronger proposition. An assurance mechanism becomes misleading when it promotes a valid local observation into unsupported authority, completeness, effective-state or privacy claims.

## Preliminary conclusions and evidentiary limits

The following are **interpretations supported by the pinned task semantics and the recorded author assessments**. They are not observations of deployed failures.

| Provisional conclusion | Evidence basis | What would strengthen or overturn it |
|---|---|---|
| A routed prompt is not a permission decision. | Request/prompt and authoritative decision are separate Consent operations. | Execute a consumer test where no matching decision exists; inspect its release behavior and decision provenance. |
| Authentication, bridge enrollment and operator approval establish different propositions. | Versioned approver/decision requirements support distinct authority and attestation modes. | Inspect a real bridge/VTA implementation's issuer checks, evidence classification and operator-action binding. |
| Revocation and distributed cache enforcement may diverge in time. | The task contracts separate VTA revocation from bridge-side caching and synchronization. | Capture revocation and post-revocation delivery timelines under realistic delay and failure conditions. |
| Success of a local exchange is insufficient to certify end-to-end authorization. | The canonical failure preconditions and source-specific consumer boundaries remain separate from successful task responses. | Test a real composed workflow with effective-state evidence and explicit relying-policy evaluation. |
| Opaque references do not prove purpose limitation or unlinkability. | Stored consent and routing metadata can be joined in a consuming environment. | Examine actual data flow, retention policy, cross-context joinability and applicable purpose governance. |

**Do not infer** that the 61 conditional cells are observed defects, that the 235 not-established cells prove safety, or that the family is a representative probability sample. Do not infer that an upstream specification is defective where it already specifies the relevant safeguard; an unsafe consuming interpretation and a normative defect are different claims. Do not infer inter-version equivalence merely from recurring case labels, or operational confidence from successful CI. Above all, **do not promote an unexecuted negative test into an observed failure**.

The current evidence warrants a **reproducible, non-normative assessment method and bounded candidate test agenda**. It does not warrant scores for risk prevalence, conformance, implementation maturity, completeness of the entire registry, independent semantic approval, or effectiveness of controls in actual deployments. Inference beyond the selected Consent family requires a fresh rationale and appropriate source/implementation evidence.

## Evidence authority and assurance boundaries

The [canonical predicate catalog](https://github.com/qbf-consulting/digital-trust-failure-corpus/tree/main/research/external-sources/trust-tasks/predicate-catalog) is a derived, drift-checked index of the existing 37 DTF cases; its authority remains with the canonical JSON case files. Exact task source/schema Git blobs and canonical case-version pins provide traceability. The research sidecar records author judgments, not an invented consent-specific failure taxonomy.

The study's **claim is author-side, source-specific applicability analysis**, not formal implementation conformance. No independent external reviewer has accepted the findings; no real VTA/bridge deployment was executed against these negative/control tests. A failure seen in one implementation would support a bounded observation about that implementation, not an automatic upstream defect. A passing synthetic or CI check likewise cannot certify external deployment behavior. Other existing family matrices remain useful research resources, but their existence does not establish registry-wide semantic completion.

## How to challenge, enrich or contribute

The immediate opportunity is to **test, correct or independently review** the existing study, not to fill remaining registry rows. Contributions that materially improve the evidence fall into three classes:

1. **Interpretation challenge.** Identify the exact Consent task URI/version and the pinned source section; identify a specific DTF proposition and its canonical case version; explain which necessary precondition the existing judgment overlooks or overstates. Propose corrected rationale and a falsifying counterexample. A counter-reading is valuable even if it disproves an existing candidate.
2. **Consumer negative/control execution.** Specify an actual test target and version, configuration, authority/policy baseline, initial state, intervention, expected safe behavior, observed result, execution timestamp and reproducible evidence. Report whether the target was a synthetic fixture, independent implementation or deployed system. Redact credentials, conversation content and unnecessary personal data. An execution on one target must not be generalized to all consumers.
3. **Independent semantic review.** Have a reviewer independently evaluate a bounded subset of task/case judgments against the pinned source, checking competing interpretations and the adequacy of proposed controls. Record reviewer identity or accountable review role, reviewed scope, source/case revisions, disagreements and signed-off disposition. Author-side re-runs and CI are not independent acceptance.

**Suggested minimal contribution record**

| Field | Required content |
|---|---|
| Claim being challenged | Task Type URI and version; canonical DTF ID and case version |
| Evidence anchor | Upstream commit, specification/schema blob and applicable source section |
| Relying proposition | Exactly what the consumer claims and why local task success does not necessarily establish it |
| Negative/control pair | Preconditions, invalid transition, expected safe outcome and positive control |
| Evidence status | Hypothesis, author-side judgment, independent review, synthetic execution, or observed external execution |
| Reproduction and privacy | Commands/fixtures or redacted observations, target/version, timestamps, permissible disclosure |
| Requested correction | Revised assessment, documented dispute, reproducible test, or explicitly justified non-applicability |

Open a [repository issue](https://github.com/qbf-consulting/digital-trust-failure-corpus/issues) for a substantive source interpretation or experimental finding, then use the [contribution procedure](https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/main/CONTRIBUTING.md) for an issue-to-PR change. Evidence-sensitive implementation findings should follow [security reporting](https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/main/SECURITY.md) rather than exposing sensitive records publicly. Preserve the original record and record contested assessments as unresolved until supported; do not change canonical failure definitions merely to make a particular mapping fit.

**A sufficient next contribution** would be one independently reviewed, reproducible stale-cache revocation negative/control pair, with its exact source and canonical-case anchors, rather than another registry-wide matrix. The study remains useful without such a contribution; it must not imply one has occurred.

## Reproduce and challenge

The machine-record authority and validators remain in their original locations. From a checked-out DTFC repository:

```sh
python -m tools.validate_consent_case_examination
python -m tools.validate_trust_tasks_predicate_catalog
python -m unittest discover -s tests -v
python tools/validate.py
python tools/build_docs.py
mkdocs build --strict
```

These commands exercise source/case bindings, structural invariants, regression expectations and published documentation. They do **not** execute a live consuming consent system or certify independent interpretive review.

A future external challenge should focus on the negative/control pairs above, test an identified VTA/bridge implementation with captured evidence and report whether it incorrectly returns a substantive `PASS` at the relying boundary. The report should distinguish target identity, current policy, execution timestamps, effective revocation state, corpus case revisions and independent reviewer findings.

## Disposition and future work

**Publish this as a bounded representative research study and preserve the machine evidence.** Retain the 1,391-version source inventory and other authored family examinations as optional inputs to future work, not as a pledge of exhaustive semantic assessment. New family studies should be undertaken only where a specific adoption need, interoperability question, deployment harm, or independent audit opportunity warrants the effort.

The appropriate close-out claim is **representative-family author research complete; broader registry coverage intentionally out of scope**. Independent challenge and execution may be pursued as separate future work and must not be silently implied by this document.
