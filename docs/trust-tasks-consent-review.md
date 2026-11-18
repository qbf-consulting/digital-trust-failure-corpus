# Consent family: source-specific DTFC research screening

**Scope:** eight versioned upstream Trust Tasks at pinned revision `f21a98ec8383352d18629a08dd5dd23935456142`. Each row is a conditional research hypothesis about a *consuming-system* boundary, not a Trust Task defect or evidence of executed conformance. None is independently semantically approved.

| Task version | Existing DTF candidate | What a consumer must not infer |
|---|---|---|
| [`consent/approve-request/0.1`](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/consent/approve-request/0.1/spec.md) | `DTF-010` (`adjacent`) | An authenticated request can be misread as sufficient approval without a returned decision and challenge match. |
| [`consent/approver-list/1.0`](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/consent/approver-list/1.0/spec.md) | `DTF-010` (`adjacent`) | A filtered or visibility-restricted empty listing may be mistaken for authoritative proof that no approver exists. |
| [`consent/approver-set/1.0`](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/consent/approver-set/1.0/spec.md) | `DTF-002` (`mechanism-overlap`) | A party that can submit a signed task could otherwise substitute its own route or operator as the decision authority. |
| [`consent/decision/1.0`](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/consent/decision/1.0/spec.md) | `DTF-013` (`adjacent`) | A verified bridge proof may be incorrectly elevated into proof that the human operator directly authorized the exact consent commitment. |
| [`consent/list/1.0`](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/consent/list/1.0/spec.md) | `DTF-021` (`mechanism-overlap`) | A cached consent grant may be reused at the later inbound-delivery boundary after its authoritative lifecycle state changes. |
| [`consent/list/1.1`](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/consent/list/1.1/spec.md) | `DTF-021` (`mechanism-overlap`) | Confusing an incremental sync position with complete current authorization evidence could permit stale consent to authorize later delivery. |
| [`consent/request/1.0`](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/consent/request/1.0/spec.md) | `DTF-010` (`mechanism-overlap`) | The existence of a valid prompt or pending record can be laundered into an affirmative permission despite the absence of decision evidence. |
| [`consent/revoke/1.0`](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/consent/revoke/1.0/spec.md) | `DTF-004` (`mechanism-overlap`) | A previously valid cached grant can be accepted as presently valid after an authoritative consent revocation has become effective. |

## How to use these records

The [machine-readable consent screening](https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/main/research/external-sources/trust-tasks/consent-review.json) records the exact source Git blob, local proposition, downstream inference, authority boundary, necessary evidence, and falsification test for each version. Open the upstream task and canonical DTFC case before constructing a test.

**Important version difference:** `consent/list/1.1` replaces the `since`/`cursor` incremental sync terminology with `syncToken`/`nextSyncToken`. Its cache-continuity test must use the actual version; no semantic equivalence is claimed.

**Boundary:** Eight candidate mappings are not an exhaustive 37-case review, eight independently accepted conclusions, or eight implementation defects. The same status gates apply as the ACL family. Run `python -m unittest tests.test_consent_review -v` for the structured research contract and negative tests.
