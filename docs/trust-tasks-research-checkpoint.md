# Trust Tasks × DTFC: pinned registry coverage and applicability findings

**Research checkpoint · 18 November 2026 · DTFC issue #135**

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
| Source-screened versions | 29 |
| Versions requiring source-specific screening | 1,362 |
| Independently approved comprehensive semantic reviews | 0 evidenced |
| Independently maintained consumer executions | 0 evidenced |

The 29 preliminary screenings comprise 12 original pilot versions and 20
ACL-family versions, with three overlaps. An ACL source-version delta study
is separately available for all 13 historical ACL versions. The resulting
mapping hypotheses retain source anchors, canonical DTFC cases, authority
boundaries and falsification tests. They are conditional research findings;
they have **not** been established as complete 37-case judgments or approved
by an independent semantic reviewer.

## Results available for external use

1. [Browse every pinned Trust Task version](trust-tasks/index.md) across all
   43 families. Each task links to its exact upstream specification and shows
   whether it has been source-screened or still needs review.
2. [Examine the source-derived family coverage](trust-tasks-coverage.md).
   The denominator and screened numerator are distinct; unreviewed entries
   cannot silently become reviewed no-matches.
3. [Read the existing conditional crosswalk](trust-tasks-crosswalk.md)
   and [ACL source-specific study](trust-tasks-acl-review.md).
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

## What remains unestablished

The research has **not** produced a defensible mapping/no-match assessment
across the remaining 1,362 versions, a complete case-by-case search for any
version, independently reviewed semantic determinations, or external target
execution. No numerical score here is a coverage-of-risk or safety score.
The source registry's many draft versions may change after the pinned commit.

To claim the full [#135 objective](https://github.com/qbf-consulting/digital-trust-failure-corpus/issues/135),
each in-scope version must receive its own source-qualified review or a
material-equivalence argument with reproducible evidence; non-matches must
describe the corpus examined; contradictory or missing evidence remains
unresolved; and independent scrutiny must establish which judgments survive
challenge. The machine-generated navigator alone cannot satisfy that gate.

## Publication and reuse decision

**Publish as a reproducible, non-normative research checkpoint. Do not label
the crosswalk exhaustive and do not close #135 or issue a completeness release.**

The result is suitable for requesting targeted external review and for
adopters seeking concrete negative-test hypotheses. It does not certify the
Trust Tasks registry, DTFC cases, or any implementation.

Sources: [QBF DTFC](https://github.com/qbf-consulting/digital-trust-failure-corpus),
[upstream Trust Tasks Registry](https://github.com/trustoverip/dtgwg-trust-tasks-tf),
and the source-linked research records and CI evidence above.
