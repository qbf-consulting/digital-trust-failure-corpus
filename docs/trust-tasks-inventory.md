# Trust Tasks source inventory and review gate (issue #135)

This record is an **inventory baseline**, not a complete semantic crosswalk. The prior [12-task pilot](trust-tasks-crosswalk.md) remains a separately bounded assessment and the [canonical DTF cases](corpus/index.md) remain unchanged.

## Pinned source and discovery

Upstream: [trustoverip/dtgwg-trust-tasks-tf at f21a98ec8383352d18629a08dd5dd23935456142](https://github.com/trustoverip/dtgwg-trust-tasks-tf/tree/f21a98ec8383352d18629a08dd5dd23935456142). The upstream `scripts/lib/specs.mjs` discovers version directories containing **both** `spec.md` and `payload.schema.json`; missing one is a build error. Nested slug segments are legal. The committed [inventory](https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/main/research/external-sources/trust-tasks/inventory.json) preserves the git blob SHAs for both files in every pair.

From the pinned Git tree, **1,391 complete versioned pairs** were found, with no unmatched spec or payload file. The directory structure represents **894 distinct slugs** across **43 top-level families**. These are source-tree counts, **not independently verified published registry membership or maturity status**. Front-matter publication/status semantics and generated-registry equivalence remain unverified, so the denominator must not be called a complete authoritative published registry population.

## Evidence states and remaining work

The inventory retains the original **12 sample-screened** versions (15 prior judgments) as a bounded study. The other **1,379 versions remain `needs-review`**; there is no implied defect, non-match, assurance result or semantic coverage. No `reviewed-mapped` or `reviewed-no-match` status is admitted without a separate source-qualified assessment contract.

Run `python -m tools.validate_trust_tasks_inventory` and `python -m unittest tests.test_trust_tasks_inventory -v`. The validator checks pinned provenance shape, path identity, duplicates, inventory cardinality and exact reconciliation with the original pilot; it **does not independently fetch the upstream tree or substantively inspect all task prose**.

## Follow-on gates

1. Reproduce upstream-generated registry membership and front matter, including non-published/internal categories; reconcile counts and statuses before calling the inventory *authoritative*.
2. Define reviewed/no-match/blocked rationale and version-delta records from actual source inspection. Review a full representative family before scaling to the remaining inventory.
3. Complete genuine evidence-backed review states for all in-scope versions. Record gaps without manufactured mapping relationships.
4. Validate generated documentation against the source records and perform independent semantic review. Execution evidence and deployments remain distinct from crosswalk applicability (see #45, #48 and #134).

**Disposition:** Inventory structurally enumerated at a source pin; **registry publication reconciliation and comprehensive semantic review still open**. No DTF schema or case changes, no independent target execution and no release assertion.


## First source-specific ACL review slice

The [ACL screening](trust-tasks-acl-review.md) evaluates seven source-pinned current operation versions against existing DTFC cases; thirteen historical versions remain explicitly pending version-delta review. The screening has no independently executed test evidence and does not close the registry-wide semantic-review gate.
