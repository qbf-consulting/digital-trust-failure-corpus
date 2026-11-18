# Trust Tasks machine assessment report: schema 0.2.0

The generated `trust-tasks/assessment-report.json` report changes its machine
contract from schema `0.1.0` to `0.2.0` under #135.

Existing `inventory_state`, `screening_state`, `candidate_mappings`,
`independent_review_state`, `execution_evidence_state`, and `version_delta`
retain their established meanings. **No previously screened candidate becomes
independently approved.**

## Additive fields and consumer migration

The 1,391 version records now include a required
`author_case_examination` object. Its `state` is `not-examined` for 1,377
versions or `author-case-examined` for the 14 full-case research versions.
Examined entries include a canonical case count, source-linked research
record, pinned case revision and counts of conditional and
`not-established-from-task` decisions, plus explicit
`independent_acceptance=not-established` and
`target_execution=not-established`.

Top-level `summary` adds:
`author_case_examined_versions`, `author_case_comparisons`,
`author_conditional_candidates`, and `author_not_established_from_task`.
The `families` section adds `author_case_examined` per family;
`review_dimensions` adds the author research dimension.

Clients using strict schema 0.1.0 must **load the published 0.2.0 schema**
before validating the new report. Do not silently discard or interpret the
new fields as independent approval. Do not combine the preliminary screening
candidate count with the author case cell count: the same scenario may be
recorded by both research stages. The author case-level rationale remains
in the pinned source JSON linked from each examined record; the report is
an index and evidence-level summary, not a second canonical source.

## Assurance status

The published machine report remains `research-checkpoint`, with
`semantic_completion_claim=false`, `independent_review_complete=false`,
and `external_execution_evidenced=false`. The full canonical baseline
and upstream pinned revision are unchanged; the report schema evolution
does not establish corpus-wide semantic Gate B completion.
