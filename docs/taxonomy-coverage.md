# Descriptive taxonomy coverage

Run `python -m tools.taxonomy_coverage` to obtain a deterministic JSON report of the canonical case denominator, case IDs, statuses, domain labels and failure-class labels. The report is computed from the current `corpus/` tree rather than maintained manually.

These are **counts of labels assigned to cases**. A large count is not evidence of complete failure coverage; a small count is not proof that an area is unimportant. Multiple labels per case are counted independently. All current cases remain draft, and these figures do not measure independently executed targets, consumer adoption, assurance maturity or certification.

The tool rejects duplicate canonical case identifiers. CI runs positive and negative tests via the standard unit-test discovery. Interpretation and selection of missing failure classes require research judgment rather than a mechanical score.
