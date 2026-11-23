# Trust Tasks × DTFC: pinned registry coverage and applicability findings

**Research checkpoint · 18 November 2026 · DTFC issue #135**

> **Historical research checkpoint (18 November 2026).** This page records the earlier registry-wide objective, source census and research status **as of that date**. It is preserved for provenance and is **not** the current project completion contract. Issue [#135](https://github.com/qbf-consulting/digital-trust-failure-corpus/issues/135) subsequently closed under a revised, deliberately bounded scope: the [representative Consent-family study](trust-tasks-representative-consent-study.md), with 296 author-side case comparisons. The 1,339 unscreened and 29 screened-but-incomplete versions are inventory states, **not obligations to finish**. The present research question, limitations and contribution guidance belong to the representative study.

## Proposition

Every versioned Trust Task in a pinned upstream registry should be traceable to
an evidence-qualified DTFC failure applicability judgment, or to an expressly
justified no-match after complete semantic review. An applicable failure
proposition concerns what a consuming system **might wrongly conclude** from a
task result; it does not imply that the task specification or any implementation
is defective.

## What is established

The upstream Trust Tasks registry at commit
[f21a98ec8383352d18629a08dd5dd23935456142](https://github.com/trustoverip/dtgwg-trust-tasks-tf/tree/f21a98ec8383352d18629a08dd5dd23935456142)
was rebuilt and reconciled with the DTFC inventory in
[CI run 44263516864](https://github.com/qbf-consulting/digital-trust-failure-corpus/actions/runs/44263516864).
The independent repeat of this **build/reconciliation**, not of semantic
judgments, also passed in
[run 44264075876](https://github.com/qbf-consulting/digital-trust-failure-corpus/actions/runs/44264075876).

| Measure | Established result |
|---|---:|
| Pinned registry entries / complete spec-schema pairs | 1,391 |
| Draft versions | 1,318 |
| Retired historical versions | 73 |
| Distinct task slugs | 894 |
| Top-level families | 43 |
| Source-screened versions | 52 |
| Versions not screened at this historical checkpoint (not a current work commitment) | 1,339 |
| Independently approved comprehensive semantic reviews | 0 evidenced |
| Independently maintained consumer executions | 0 evidenced |

The 52 preliminary screenings comprise 12 original pilot versions, 20 ACL-family
versions, eight Consent-family versions and 15 additional audit/governance/
privileged-approval/discovery/ceremony-receipt versions, with three overlaps. An ACL source-version delta study
is separately available for all 13 historical ACL versions. The resulting
mapping hypotheses retain source anchors, canonical DTFC cases, authority
boundaries and falsification tests. They are conditional research findings;
the original screening records do not themselves establish full 37-case
consideration or independent acceptance; the independently qualified complete-case research records below preserve that distinction.

## Complete author-side case examination of six families

The [audit](trust-tasks-audit-case-examination.md),
[consent](trust-tasks-consent-case-examination.md),
[capability governance](trust-tasks-governance-case-examination.md),
[privileged task consent](trust-tasks-task-consent-case-examination.md),
[discovery](trust-tasks-discovery-case-examination.md), and
[ceremony receipt](trust-tasks-ceremony-receipt-case-examination.md) examinations
provide all 37 canonical-case comparisons for **23** source-screened task
versions. The newest case is the previously unscreened
`trust-ceremony-receipt/0.1`, which also receives a pinned, conditional
DTFC-026 screening record. These are substantive author-side decisions, not
independently accepted mappings or observed implementation failures.

| Case-level measure | Author research result |
|---|---:|
| Fully case-examined pinned task versions | 23 of 1,391 |
| Explicit case comparisons | 851 |
| Conditional candidate applicability cells | 192 |
| Case comparisons not established by task semantics | 659 |
| Previously source-screened versions still lacking full case comparison | 29 |
| Versions not screened at this historical checkpoint | 1,339 |
| Independently accepted 37-case dispositions | 0 |
| Independent consumer executions | 0 |

The 192 cells include overlapping scenarios across task versions. They are
**not** 192 verified defects, incidents or new DTFC propositions.
`not-established-from-task` is *not* an independently reviewed no-match or
proof of safety: it means that the task contract alone does not establish
all preconditions of the canonical failure. A composed deployment can add
those preconditions. Review and test the actual relying proposition before
asserting either applicability or non-applicability.

**For DTG implementers, the immediately executable research agenda is:**

| Boundary | Setup and falsification question | Candidate DTF cases | Control outcome |
|---|---|---|---|
| Ceremony completion evidence | Provide recorder-signed payload.complete=true without a held signed terminal step or pinned definition, and request verified completion. | DTF-010, DTF-026, DTF-027, DTF-030 | Return an evidence-limited/indeterminate result rather than a completion PASS. |
| Audit completeness | Sign a valid first audit page with material contrary evidence on a subsequent page; does the consumer return an exhaustive PASS? | DTF-010, DTF-026 | Follow version-specific continuation and filters or return INDETERMINATE. |
| Audit provenance | Supply `verified: true` for a restamped/truncated but locally consistent chain; does the auditor assert authenticity? | DTF-010, DTF-025, DTF-027 | Limit to internal integrity and demand independent anchoring for authenticity. |
| Audit purpose and retention | Reuse a legitimate retrieved tail for member scoring or retain its identifiers after the oversight purpose expires. | DTF-034, DTF-037 | Reject secondary use absent a separate governance basis; enforce bounded retention. |
| Capability delegation | Sign an enable request as non-operator, or enable a real companion then write a registry tuple outside `vocabulary.actions`. | DTF-002, DTF-013, DTF-023 | Host checks operator role and rejects out-of-scope delegate action. |
| Capability lifecycle | Cache enablement, disable handlers, and attempt a later material execution or assert historical invalidity. | DTF-005, DTF-006, DTF-016, DTF-021 | Deny later execution while preserving earlier effective history. |
| Consent cache revocation | Revoke a group grant after a bridge persists an allow, then attempt delivery from stale cache. | DTF-001, DTF-010, DTF-021 | Require fresh VTA grant state or default-deny; 1.0 cursor differs from 1.1 syncToken. |
| Consent proof versus factor | Use valid WebAuthn evidence without approver-own-DID assertion, or revoke approver before execution. | DTF-013, DTF-017, DTF-021, DTF-023 | Require own-DID proof, current approval eligibility, exact action and state. |
| Advisory grant notice | Receive an authentic notice without a current stored grant, then resubmit. | DTF-010, DTF-022, DTF-027 | Ignore notice as authority; fail closed on authoritative grant lookup. |
| Discovery expiry horizon | Cache a broad 0.4 acceptanceWindow, then tighten expiryHorizonSeconds before a material request. | DTF-011, DTF-021 | Enforce the actual consumer's current expiry policy at task acceptance. |
| Discovery-required extension | Advertise requiredExt for data that the producer may not disclose under its own policy. | Policy-disclosure seam; DTF-034 **not established** from first-time disclosure | Decline rather than gather or attach unauthorized extension data. |
| Management discovery | Return `status=available`, then try an unauthorized commitment or treat it as enabled. | DTF-010, DTF-018, DTF-028 | Require independent enabled-state and principal authority at execution. |

These are proposed **negative/control test pairs**, not executed
interoperability or conformance evidence. The upstream task texts already
express many of the necessary safeguards; the test target is the consuming
implementation's enforcement or the broader assurance inference.

## Results available for external use

1. [Browse every pinned Trust Task version](trust-tasks/index.md) across all
   43 families. Each task links to its exact upstream specification and shows
   whether it has been source-screened or still needs review.
2. [Examine the source-derived family coverage](trust-tasks-coverage.md).
   The denominator and screened numerator are distinct; unreviewed entries
   cannot silently become reviewed no-matches.
3. [Read the existing conditional crosswalk](trust-tasks-crosswalk.md)
   [ACL source-specific study](trust-tasks-acl-review.md), and
   [Consent research screening](trust-tasks-consent-review.md) and
   [cross-family screening](trust-tasks-cross-family-review.md).
4. [Apply the review protocol](trust-tasks-review-method.md)
   to challenge an existing link or substantiate a new case-specific mapping.

## Meaningful findings

**Authority is not established by technical execution alone.** ACL grant and
role-change operations specify authorization checks. A downstream system must
not elevate a valid task proof into unconstrained delegation.

**Lifecycle validity is transaction-boundary specific.** ACL revoke, session
revoke and policy activation can change an authoritative state. An earlier
valid observation is not necessarily valid at the later decision or commitment.

**Absence in a response is not global absence.** ACL list and show have
pagination, filters and disclosure policy. An empty response or selected page
may not prove that the underlying grant or authority is absent.

**Versions change the assurance proposition.** ACL pagination fields,
authority-scope representation and purpose restrictions changed materially.
Mappings must be pinned to the actual version, not inherited by task-name
similarity.

These findings identify falsifiable **consumer** failure seams, not verified
incident manifestations or upstream specification defects.

**Consent approval is not the same as an authenticated prompt.** The source distinguishes
signed operator decisions from bridge attestations and requires authoritative grant
state to remain current at the delivery boundary.

## What remains unestablished

The research has **not** produced a defensible mapping/no-match assessment
across the remaining population. A complete author-side 37-case examination
now exists for **twenty-three** versions, but the other 29 screened versions and 1,339
unscreened versions still lack complete case comparison. Independent semantic
acceptance and external target execution also remain unestablished. No numerical score here is a coverage-of-risk or safety score.
The source registry's many draft versions may change after the pinned commit.

Under the **superseded, exhaustive** interpretation of [#135](https://github.com/qbf-consulting/digital-trust-failure-corpus/issues/135),
each in-scope version must receive its own source-qualified review or a
material-equivalence argument with reproducible evidence; non-matches must
describe the corpus examined; contradictory or missing evidence remains
unresolved; and independent scrutiny must establish which judgments survive
challenge. The machine-generated navigator alone cannot satisfy that gate.

## Publication and reuse decision

**Historical disposition on 18 November 2026:** publish as a reproducible, non-normative research checkpoint; no exhaustive-completeness release was justified. The earlier instruction to keep #135 open was superseded by its subsequently revised representative-family completion contract.

The result is suitable for requesting targeted external review and for
adopters seeking concrete negative-test hypotheses. It does not certify the
Trust Tasks registry, DTFC cases, or any implementation.

Sources: [QBF DTFC](https://github.com/qbf-consulting/digital-trust-failure-corpus),
[upstream Trust Tasks Registry](https://github.com/trustoverip/dtgwg-trust-tasks-tf),
and the source-linked research records and CI evidence above.
