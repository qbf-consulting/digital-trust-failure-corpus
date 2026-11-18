# Trust Tasks applicability review and reuse

## Objective

For each pinned, versioned Trust Task, identify an evidence-qualified existing
DTFC failure proposition at a concrete consumer trust boundary, or substantiate
a no-match after inspecting the full canonical case corpus. Separate registry
enumeration, preliminary screening, independent semantic review and execution.

The [versioned navigator](trust-tasks/index.md) covers every pinned registry
version, including retired versions, **without** claiming complete semantic review.

## Independent evidence dimensions

| Dimension | Positive evidence | Does not establish |
|---|---|---|
| Inventory | Exact upstream Type URI and pinned spec/schema files | Applicability or safety |
| Screening | Source-specific conditional DTFC hypothesis | Exhaustive case review |
| Classification | Mechanism overlap or adjacency | Implementation defect |
| Source provenance | Version, commit and Git blob | Correct interpretation |
| Independent review | Named reviewer, exact scope, decision and challenged cases | Execution conformance |
| Execution | Reproducible test on identified consumer/target | Universal interoperability |

Unreviewed is not a no-match. Missing, stale, conflicting or unavailable evidence
is not PASS. An AI-assisted self-review cannot be counted as independent approval.

## Author-side full case examination

An author may substantively examine all 37 canonical cases for a pinned task
without claiming independent acceptance. The complete-case machine records for
[audit](trust-tasks-audit-case-examination.md) ,
[capability governance](trust-tasks-governance-case-examination.md), and
[delegated task consent](trust-tasks-task-consent-case-examination.md) demonstrate
this intermediate evidence level. Each record includes one decision for every
canonical case, distinguishes a falsifiable conditional candidate from a
`not-established-from-task` observation, and pins source/schema hashes.

This intermediate class is **not** `reviewed-no-match`: not establishing the
case's preconditions from a task specification is weaker than disproving a
candidate in a known consuming system. Case-level rationale and negative tests
are necessary but do not establish a deployed consumer response, global
non-applicability or an independent reviewer decision.

## Reviewer acceptance path

1. Open the exact upstream Type URI and source commit, including its metadata,
   conformance language, payload schema, lifecycle, errors and privacy conditions.
2. Inspect the full relevant DTF case propositions and competing mechanisms.
   Document exactly which preconditions are present and which remain conditional.
3. Separate what successful local task execution establishes from an unsafe
   downstream inference, including authority, policy, timing, retention and scope.
4. Preserve falsifiable negative tests and evidence required to distinguish
   safe handling from failures. Do not infer defect from applicability.
5. For a reviewed **no-match**, record the corpus coverage examined, competing
   explanations and evidence of absence of a matching *existing* proposition.
   Rejecting one candidate case is not a reviewed task-level no-match.
6. Pin the reviewer identity, source commit, all case versions, decision, limits
   and any adversarial counterexamples. Record unresolved contradictions as
   blocked; no unreviewed result may be promoted through schema validation.
7. Record implementation execution separately, with target provenance, commands,
   observed result, evidence hashes and reviewer. Synthetic self-execution is
   not independently maintained external evidence.

The published [coverage summary](trust-tasks-coverage.md) remains a preliminary,
non-normative research finding. It is shareable as a source-complete versioned
registry index, not as completed task-to-failure assurance.

## Unresolved independent challenge

A contested interpretation is recorded as `blocked-evidence` with a source-pinned challenge record. It is **not** a completed independent review and does **not** count toward the semantic-completeness numerator. An unresolved contradiction must not be converted to an accepted mapping, a reviewed no-match, or a positive assurance result. The report contract tests this false-success case.
