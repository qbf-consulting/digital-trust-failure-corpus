# When a consent task succeeds but the relying decision fails
## A representative Trust Tasks × DTFC assurance study

**Research checkpoint · 24 November 2026 · QBF Consulting LLP · Non-normative**

**Scope:** Eight pinned `consent/*` task versions in the [Trust Tasks registry](https://github.com/trustoverip/dtgwg-trust-tasks-tf/tree/f21a98ec8383352d18629a08dd5dd23935456142), at upstream commit `f21a98ec8383352d18629a08dd5dd23935456142`. **DTFC authority:** [37 canonical failure propositions](corpus/index.md). **Reproducible evidence:** [296 case/version judgments](https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/main/research/external-sources/trust-tasks/consent-case-examination.json), [source-specific consent screening](https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/main/research/external-sources/trust-tasks/consent-review.json), [review method](trust-tasks-review-method.md). [Full per-task examination](trust-tasks-consent-case-examination.md).

## Executive determination

The most consequential boundary in the selected family is **the difference between a valid local consent task result and a justified later permission to deliver or act**. A prompt may have been routed, a bridge may legitimately attest an operator choice, a grant may have been stored, or a synchronization request may have completed. None of those facts alone establishes that the exact conversation, actor, scope and authority remain permitted at the eventual delivery or execution boundary.

The eight published source versions explicitly provide safeguards for several of these seams. This study is therefore **not** a finding that the Trust Tasks specifications are defective. It identifies conditional failure propositions a *consuming implementation or composition* could get wrong even when an individual exchange is syntactically conformant. The central assurance challenge is whether the consuming system can support the stronger proposition it asserts with current authority, decision provenance, complete evidence, and enforceable purpose and lifecycle controls.

This representative assessment is deliberately bounded. It does **not** claim exhaustive applicability coverage of the 1,391 pinned registry versions. The wider registry inventory is retained for source discovery and future voluntary studies, without being treated as a research-completion denominator or project deliverable.

## Why this family is a meaningful representative

Consent is a useful stress test for the DTFC method because it involves multiple independently meaningful actors: an operator or approver, a context administrator, a Verifiable-Trust Agent (VTA) maintaining authoritative grants, an enrolled messaging bridge enforcing decisions, and a relying delivery process. It crosses authority, evidence, temporal state, composition and privacy boundaries, and has a source-pinned breaking change between `consent/list/1.0` and `1.1`. Its breadth demonstrates the method's ability to distinguish observed task behavior from unsupported downstream reliance. It is **purposefully selected**, not a statistically representative sample, and cannot support prevalence or safety claims across other task families.

All eight versions already have explicit author-side consideration of every canonical DTF case. No additional speculative mappings were generated for this synthesis.

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

## Assessment method and acceptance boundaries

The study used the existing 37 canonical DTF propositions, not an invented consent-specific failure taxonomy. Each source version has its own immutable upstream specification/schema blob and case-version pins. Each author judgment records a conditional candidate with authority boundary and falsification hypothesis, or a reason the isolated task source does not establish the full canonical preconditions. The [canonical predicate catalog](https://github.com/qbf-consulting/digital-trust-failure-corpus/tree/main/research/external-sources/trust-tasks/predicate-catalog) provides a derived, drift-checked index of those propositions; it does not supersede their canonical JSON.

The study's **claim is author-side, source-specific applicability analysis**, not formal implementation conformance. No independent external reviewer has accepted the findings; no real VTA/bridge deployment was executed against these negative/control tests. Failing a suggested negative test in an actual consumer would be evidence of that consumer's behavior, not automatic proof of a normative upstream defect. A successfully executed synthetic or CI test likewise does not certify real deployments.

The family was selected for mechanism diversity and existing research maturity. It is not a representative *sample in a statistical sense*, and the study does not estimate failure frequency, severity or absence across the Trust Tasks registry. Other existing family matrices remain useful independent research resources, but this publication makes no assertion about registry-wide semantic review completion.

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
