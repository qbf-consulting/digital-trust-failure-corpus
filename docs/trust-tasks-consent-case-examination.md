# Consent operations × DTFC: source-pinned case matrix and technical supplement

**18 November 2026 · Tracked by [#135](https://github.com/qbf-consulting/digital-trust-failure-corpus/issues/135)**  
**Upstream source:** [Trust Tasks registry commit f21a98e](https://github.com/trustoverip/dtgwg-trust-tasks-tf/tree/f21a98ec8383352d18629a08dd5dd23935456142)  
**Machine evidence:** [consent-case-examination.json](https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/main/research/external-sources/trust-tasks/consent-case-examination.json).

> **Reading guide:** This is the detailed source/case accounting underlying the [representative Consent research study](trust-tasks-representative-consent-study.md). Start with the primary study for family selection, analytical design, conclusions, limitations and contribution steps. This supplement retains the original author-side decisions and their negative/control hypotheses; it does not add independent evaluation.

## Scope

All eight pinned `consent` specification versions were examined against the 37 existing canonical DTFC cases. The **296 case-version comparisons** contain 61 conditional candidate cells and 235 decisions where the complete case preconditions are **not established from the task source alone**. All data is bound to per-version upstream specification and payload-schema Git blobs. Conditional candidates are not validated incidents or vulnerabilities; not-established does not imply deployment-wide non-applicability or safety. Independent semantic acceptance and external target execution remain unestablished.

| Task version | Case comparisons | Conditional candidate cells |
|---|---:|---:|
| [approve-request/0.1](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/consent/approve-request/0.1/spec.md) | 37 | 8 |
| [approver-list/1.0](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/consent/approver-list/1.0/spec.md) | 37 | 6 |
| [approver-set/1.0](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/consent/approver-set/1.0/spec.md) | 37 | 7 |
| [decision/1.0](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/consent/decision/1.0/spec.md) | 37 | 9 |
| [list/1.0](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/consent/list/1.0/spec.md) | 37 | 8 |
| [list/1.1](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/consent/list/1.1/spec.md) | 37 | 8 |
| [request/1.0](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/consent/request/1.0/spec.md) | 37 | 7 |
| [revoke/1.0](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/consent/revoke/1.0/spec.md) | 37 | 8 |
| **Total** | **296** | **61** |

These eight versions were already included in the 51 source-screened versions; this deeper research does not increase the screened-version numerator.

## Findings for DTG and Trust Tasks

### Authority boundaries: identity, approver routing, consent and access

`consent/approver-set` allows a **context admin** to bind the approver for a platform/context, with an opaque `routeHint`. A valid signature by someone who is not a context admin must not install a binding. `approver-list` may disclose only bindings the requester is entitled to see; it does not confer approval authority on the requester. `consent/request` requires an enrolled messaging bridge, default-deny message holding, and an operator decision before release.

**Negative/control pair:** Authenticate an actor with valid proof but no administrator authority for the named VTA context, then attempt to change its approver to an attacker. Reject. Conversely, a correctly scoped signed admin binding succeeds without granting that admin blanket authority to read the conversation. Candidate DTF-002, DTF-013, DTF-028.

### Consent provenance must survive weaker bridge attestation

`consent/decision/1.0` deliberately admits both a directly signed operator decision and a **bridge-attested** choice, recording which evidence mode applies. Bridge enrollment is the source of trust for the latter. An implementation that reports bridge attestation as the human's own non-repudiable signature has upgraded the evidentiary proposition without justification.

**Negative/control pair:** Present an enrolled bridge assertion that the operator allowed a conversation. Verify the legitimate bounded bridge-attested grant without claiming directly signed non-repudiation. Then substitute a signed decision from a bridge not enrolled for the subject/context and require denial. Candidate DTF-013, DTF-023, DTF-027; no protocol defect is asserted by the choice to support a weaker mode.

### A prompt is not an approval and a grant is not an execution result

`approve-request/0.1` sends an authenticated prompt to an approver's separate device using a single-use challenge. `request/1.0` makes an enrolled bridge hold conversation messages in default-deny while the VTA routes a prompt. The initial `accepted` status establishes routing, not operator consent, agent message delivery, or a completed consequential action.

**Negative/control pair:** Deliver a valid prompt and suppress the signed `consent/decision`; try releasing the inbound message anyway. Refuse. For the positive control, record an authorized challenge-matching `allow` in the VTA for the exact `subject` and `scope` and re-check it at delivery. Candidate DTF-010, DTF-017, DTF-023, DTF-027.

### Consent revocation and bridge caches form a distributed temporal boundary

`consent/list` permits the bridge to persist an agent-scoped local grant cache. `consent/revoke` deletes the authoritative subject grant and signals bridges, returning it to default-deny. These are **separate** operations, and a successful revoke response does not itself prove every caching bridge has discarded the prior allow before further messages arrive. The 1.0/1.1 list versions have breaking wire changes: 1.0 `since` / `cursor` become 1.1 `syncToken` / `nextSyncToken`; 1.1 forbids accepting a token not issued by the consumer. These are change-stream positions, not generic paging or timestamps.

**Negative/control pair:** Cache an allowed group in `consent/list/1.0`, revoke it, then deliver a message based on that cache. Reject or defer to current VTA authority. Repeat with 1.1 tokens and deliberately use an unissued token; reject the token rather than interpreting an empty delta as no revocation. Candidate DTF-001, DTF-010, DTF-011, DTF-021 and DTF-026, conditional on the relying claim.

### Privacy: opacity is not sufficient retention governance

Opaque conversation references and routing hints reduce direct address exposure. They do not make logs or persistent consent caches unlinkable across multiple requests. The `receive` vs `converse` scope difference is material: a group conversation can expose participants never asked directly, and an agent with converse scope may speak as the subject. A legitimate approval record is no general authorization to profile members or retain their communication graph indefinitely.

**Negative/control pair:** Join legitimately collected `conversationRef`, agent DID, platform and decision history across groups and attempt downstream participant analytics. Challenge any claim of privacy-minimal processing absent a purpose and retention basis. Candidate DTF-034, DTF-036, DTF-037 when their complete preconditions are satisfied.

## Version- and authority-specific limits

A bridge-attested `decision/1.0` is **not** a `task-consent/decision/0.2` own-DID approval. The two task families govern different consent mechanisms. Likewise `list/1.1` is not wire-equivalent to `list/1.0`; the exact token names and issuer validation obligations matter.

This report provides substantive author-side case research, not accepted no-match verdicts for unseen deployment compositions. It preserves upstream source safeguards and does not claim execution of the proposed negative tests or independent review.

## Reproduction

```sh
python -m tools.validate_consent_case_examination
python -m unittest discover -s tests -v
python tools/validate.py
```

The shared validator detects omitted or duplicated versions/cases, changed pinned blobs, unsupported semantic version reuse, missing candidate boundaries and falsification, and fabricated independent acceptance or execution. The version navigator and machine assessment report link to these source-pinned research decisions without claiming corpus-wide Gate B completion.
