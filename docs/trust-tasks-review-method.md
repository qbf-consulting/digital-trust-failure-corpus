# Trust Tasks applicability review and reuse

## Research publication scope (24 November 2026)

The current publication objective is the [representative Consent family study](trust-tasks-representative-consent-study.md), **not** completed applicability across the registry. The eight source-pinned Consent versions each have an author-side 37-case examination (296 case judgments), with conditional candidate boundaries and honest not-established-from-source outcomes. The other family records remain historical source-qualified research; they need not be expanded to meet this bounded publication outcome.

The 1,391-version pinned inventory and generated navigator remain available for discovery and reproducibility. Their unscreened versions are **not a committed backlog** under this study and must not appear as reviewed-no-match. Future expansions require a new question, defined in-scope versions and a proportionate review contract. Independent semantic challenge and live target execution are separate assurance levels; neither can be claimed from author research, structural checks or CI.

## Objective

For each **selected in-scope** pinned, versioned Trust Task, identify evidence-qualified existing DTFC failure propositions at a concrete consumer trust boundary, and document when the source alone does not establish their complete preconditions. A deployment-level no-match requires additional evidence and review. Separate registry
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
[delegated task consent](trust-tasks-task-consent-case-examination.md), and
[discovery](trust-tasks-discovery-case-examination.md), and
[consent](trust-tasks-consent-case-examination.md), and
[ceremony receipt](trust-tasks-ceremony-receipt-case-examination.md) demonstrate
this intermediate evidence level. Each record includes one decision for every
canonical case, distinguishes a falsifiable conditional candidate from a
`not-established-from-task` observation, and pins source/schema hashes.

Each case decision also records the exact `case_version` from the
authoritative DTFC proposition. A later amendment that retains `DTF-xxx`
but changes its semantic version invalidates silent reuse of the old judgment.
The family validators fail closed on such drift; only a source-specific
reassessment can re-establish the disposition. The author research JSON
sidecar contract is now `0.2.0`; this is separate from the generated
assessment-report schema `0.2.0`, whose public fields are unchanged here.

This intermediate class is **not** `reviewed-no-match`: not establishing the
case's preconditions from a task specification is weaker than disproving a
candidate in a known consuming system. Case-level rationale and negative tests
are necessary but do not establish a deployed consumer response, global
non-applicability or an independent reviewer decision.


## Canonical proposition catalog (derived, non-authoritative)

The machine-readable [predicate catalog](https://github.com/qbf-consulting/digital-trust-failure-corpus/tree/main/research/external-sources/trust-tasks/predicate-catalog) preserves, without paraphrase, the canonical proposition, preconditions, trigger, evidence requirements, falsification and expected dispositions of every one of the 37 DTF cases. Each entry includes its case version, repository path and exact Git blob identity. It is an **index**, not a replacement for the original `corpus/<family>/DTF-NNN.json` authority. Run `python -m tools.validate_trust_tasks_predicate_catalog` to reconcile all five category indexes against the current canonical corpus. Any change to a case's semantics or source bytes fails closed, even if the author forgets to bump the case version; regenerate and reassess dependent judgments explicitly rather than treating the stale catalog as accepted.

## Semantic-delta method validation (Gate B, issue #135)

The source-pinned [delta control ledger](https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/main/research/external-sources/trust-tasks/semantic-delta-controls.json) records six **known material version changes** already described in the six complete-family author examinations: audit pagination, consent incremental sync, task-consent action binding and supplemental proof, and discovery framework-version and acceptance-window/expiry revisions. Each comparison binds both exact spec/schema Git blobs to the pinned inventory, known delta sections, canonical case versions and candidate predicates requiring challenge.

Run `python -m tools.validate_trust_tasks_semantic_deltas` to check these controls. The regression tests deliberately introduce source drift, semantic-version drift, missing anchors, incorrect marker claims, cross-contract comparisons, false reviewer acceptance and unjustified inheritance. The validator permits only an individually source-justified, unchanged case decision with exact source sections, matching case-version and author-case reasoning, explicit negative control and no overlap with the recorded material-delta challenge. The first such record is **DTF-002 for audit/list/0.1 → 0.2**, where both pinned versions preserve the community-wide audit-read authority requirement despite changing pagination fields. This is **one author-side predicate-scoped reuse argument**, not independent acceptance, an additional fully examined task version, or whole-version equivalence. The validator establishes integrity and admissible evidence shape; a reviewer must still substantively challenge the normative interpretation of both upstream documents.

Further research must validate more unchanged-boundary claims and test whether this approach reduces *fresh* examination requirements across the 29-version screened backlog. Ambiguous comparisons remain unresolved for inheritance. No corpus definition, public machine report contract, Gate B case-completion numerator, or independent-review status changes through this control ledger.

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
