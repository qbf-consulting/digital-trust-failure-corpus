# Trust Tasks × DTFC: delegated task consent, complete author case examination

**18 November 2026 · #135 research tranche**  
**Upstream pin:** [Trust Tasks commit f21a98e](https://github.com/trustoverip/dtgwg-trust-tasks-tf/tree/f21a98ec8383352d18629a08dd5dd23935456142)  
**Machine record:** [task-consent-case-examination.json](https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/main/research/external-sources/trust-tasks/task-consent-case-examination.json)

## Coverage and claim

All four pinned task-consent versions are examined against **all 37 existing DTFC propositions**. This supplies 148 explicit author-side case comparisons with source-pinned task/spec/schema digests and case-specific reasoning, including evidence for why a canonical proposition is not established from a particular task contract.

| Version | Case comparisons | Conditional candidates | Not established from task |
|---|---:|---:|---:|
| [request/0.1](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/task-consent/request/0.1/spec.md) | 37 | 9 | 28 |
| [decision/0.1](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/task-consent/decision/0.1/spec.md) | 37 | 10 | 27 |
| [decision/0.2](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/task-consent/decision/0.2/spec.md) | 37 | 12 | 25 |
| [granted/0.1](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/task-consent/granted/0.1/spec.md) | 37 | 6 | 31 |
| **Total** | **148** | **37** | **111** |

The 37 conditional cells are not 37 vulnerabilities or independent failures, and the 111 not-established decisions are **not** independently approved no-matches. They are explicit statements that the task specification does not itself establish the canonical case's complete preconditions. The same failure could arise after adding a consuming implementation. All proposed negative tests remain unexecuted.

## Findings and priority negative/control pairs

### 1. Human consent must cover actual effects, not requester prose

The `request` task requires the executor to dry-run its **actual handler**, not use a separate schema-based approximation, against authoritative state. The approver must see every effect summary, including unrecognized kinds, and must be told when effects are indeterminate. The requester's `note` is untrusted prose: the executor may attest its provenance, not its truth.

**Priority test:** Request a DID document update that implicitly rotates keys while the requester describes only a service change. An approver UI that hides the key rotation is not a complete effect presentation. Pair this with an honest UI rendering the full handler-derived effect and showing explicit uncertainty when consequences cannot be computed. Candidate DTF-017, DTF-023, DTF-026, DTF-027.

### 2. Authorization is the approver's own DID assertion, not channel authentication or added factors

For `decision/0.1`, `proofPurpose: assertionMethod` and the approver's verified DID establish who assented. The executor cannot infer approval from a transport bearer session. `decision/0.2` allows optional WebAuthn or a signed approver statement, but those factors provide additional presence evidence; they **do not replace** the approver's own DID proof. A delegated console signature is not an approver.

**Priority test:** Deliver an otherwise valid approval with only authenticated transport or a valid passkey factor but no own-DID assertion, and require refusal. Then prove the positive case with correct signer, correct challenge, digest, pending action and appropriate factor. Candidate DTF-002, DTF-013, DTF-023, DTF-025.

### 3. Approval must survive neither changed state nor changed policy

The decision binds a single-use challenge and digest to the precise task. At execution the executor rederives the payload digest, checks the prior state and **re-evaluates policy and approver enrolment**. A device that was eligible when it approved may be revoked before execution, or the approved effects may become stale.

**Priority test:** Approve under valid enrolment, then change `statePin` or revoke enrolment before material execution. The subsequent grant cannot be consumed as authority for the stale action. Positive control: same exact payload and state, current enrolment and policy, challenge consumed only at execution. Candidate DTF-017, DTF-021.

### 4. A threshold count is not necessarily independent approval

`minApprovals` counts distinct enrolled approvers. That is an appropriate authorization requirement, but a relying governance policy demanding **independently controlled approval** must establish more than distinct signer identifiers. Even WebAuthn-backed factors do not necessarily establish independent organizational control.

**Priority test:** Meet N-of-M with separately signed approvers sharing a single controlling authority, and challenge any independent-approval claim. Do not claim a protocol defect merely because the task only specifies distinct approval. Candidate DTF-024.

### 5. The granted notification is explicitly non-authoritative

The `granted` task is advisory and may be unsigned; it causes a resubmission, not execution. The executor's stored single-use grant, current policy and current enrollment remain the actual execution gate. A spoofed or replayed notice cannot create a grant.

**Priority test:** Send an authentic or forged notice where no current grant is stored, then resubmit. It must be refused regardless of notification delivery. Also test that an unreceived notice does not block polling. Candidate DTF-010, DTF-022, DTF-027, DTF-028, DTF-030.

### 6. Approval evidence creates a secondary privacy and retention boundary

The request carries personal before/after values and is exchange-scoped. Decisions remain durably attributable to individual approvers for accountability; in 0.2, factor evidence may include persistent WebAuthn credential identifiers. The legitimate audit basis is not permission to maintain a permanent cross-task archive of displayed personal diffs, rank approvers by compliance, or correlate their devices outside stated governance purposes.

**Priority test:** After approval, retain full request snapshots and decision/factor identifiers in a person-level analytics table. Verify independently bounded retention and purpose controls. Candidate DTF-034 and DTF-037; request field composition can additionally test DTF-036 when privacy-minimality is asserted.

## Version-specific semantic difference

`decision/0.2` adds optional `evidence` and `actionId`; the latter can bind a VTC parked action, and the executor may execute it directly when the approval threshold is reached. The core own-DID approval proof remains mandatory. The newer fields create new source-specific failure seams, particularly factor substitution, action mismatch, device-identifier correlation and conflation of approved with completed action. **Do not carry forward all 0.1 judgments without examining those changed semantics.**

## Validation and governance status

```sh
python -m tools.validate_task_consent_case_examination
python -m unittest discover -s tests -v
python tools/validate.py
```

The shared family validator checks all version and case membership, pinned spec/schema blobs, case-count invariants, affirmative candidate boundaries, and source-specific 0.1→0.2 delta. Negative tests reject fabricated independent review, no-match promotion, executed target claims, incomplete case sets and source drift.

This is complete **author-side case consideration for this pinned family**. It is not independent semantic approval, target execution, or a claim that a Trust Task specification has a defect. The broader #135 Gate B population remains incomplete.
