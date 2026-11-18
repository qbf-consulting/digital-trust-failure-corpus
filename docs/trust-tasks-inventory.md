# Trust Tasks source inventory and review gate (issue #135)

This record is an **inventory baseline**, not a complete semantic crosswalk. The prior [12-task pilot](trust-tasks-crosswalk.md) remains a separately bounded assessment and the [canonical DTF cases](corpus/index.md) remain unchanged.

## Pinned source and discovery

Upstream: [trustoverip/dtgwg-trust-tasks-tf at f21a98ec8383352d18629a08dd5dd23935456142](https://github.com/trustoverip/dtgwg-trust-tasks-tf/tree/f21a98ec8383352d18629a08dd5dd23935456142). The upstream `scripts/lib/specs.mjs` discovers version directories containing **both** `spec.md` and `payload.schema.json`; missing one is a build error. Nested slug segments are legal. The committed [inventory](https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/main/research/external-sources/trust-tasks/inventory.json) preserves the git blob SHAs for both files in every pair.

From the pinned Git tree, **1,391 complete versioned pairs** were found, with no unmatched spec or payload file. The directory structure represents **894 distinct slugs** across **43 top-level families**. The [pinned upstream registry build](https://github.com/qbf-consulting/digital-trust-failure-corpus/actions/runs/44263516864) successfully reconciled all **1,391 generated entries** against **1,391 complete source pairs**. The status census is **1,318 draft, 73 retired**. The [reconciliation record](https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/main/research/external-sources/trust-tasks/registry-reconciliation.json) preserves provenance. The count includes retired published historical versions, and does not establish semantic applicability.

## Evidence states and remaining work

The inventory retains the original **12 sample-screened** versions (15 prior judgments) as a bounded study. The other **1,379 versions remain `needs-review`**; there is no implied defect, non-match, assurance result or semantic coverage. No `reviewed-mapped` or `reviewed-no-match` status is admitted without a separate source-qualified assessment contract.

Run `python -m tools.validate_trust_tasks_inventory` and `python -m unittest tests.test_trust_tasks_inventory -v`. The validator checks pinned provenance shape, path identity, duplicates, inventory cardinality and exact reconciliation with the original pilot; it **does not independently fetch the upstream tree or substantively inspect all task prose**.

## Follow-on gates

1. **Completed:** pinned upstream registry generation and exact membership/status reconciliation (run 44263516864).
2. Define reviewed/no-match/blocked rationale and version-delta records from actual source inspection. Review a full representative family before scaling to the remaining inventory.
3. Complete genuine evidence-backed review states for all in-scope versions. Record gaps without manufactured mapping relationships.
4. Validate generated documentation against the source records and perform independent semantic review. Execution evidence and deployments remain distinct from crosswalk applicability (see #45, #48 and #134).

**Disposition:** Pinned source and published registry membership reconciled; **comprehensive semantic review remains open**. No DTF schema or case changes, no independent target execution and no release assertion.


## First source-specific ACL review slice

The [ACL screening](trust-tasks-acl-review.md) evaluates seven source-pinned current operation versions against existing DTFC cases; thirteen historical versions remain explicitly pending version-delta review. The screening has no independently executed test evidence and does not close the registry-wide semantic-review gate.


## Source-derived crosswalk coverage

The [coverage matrix](trust-tasks-coverage.md) combines the original pilot and the ACL research slice without double counting the overlap. It makes the remaining screening queue visible by family. Publication reconciliation and independent semantic review remain open.


## Reconcile with the actual upstream registry build

An offline [registry reconciliation command](https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/main/tools/reconcile_trust_tasks_registry.py) can verify source bytes and the generated catalogue against the pinned inventory. It compares both files in every discovered pair, enforces exact registry membership and reports upstream lifecycle statuses. Run from a local clone of DTFC:

```bash
git clone https://github.com/trustoverip/dtgwg-trust-tasks-tf.git /tmp/dtgwg-trust-tasks-tf
git -C /tmp/dtgwg-trust-tasks-tf checkout f21a98ec8383352d18629a08dd5dd23935456142
cd /tmp/dtgwg-trust-tasks-tf
npm ci
npm run build
cd /path/to/digital-trust-failure-corpus
python -m tools.reconcile_trust_tasks_registry --checkout /tmp/dtgwg-trust-tasks-tf
```

The pinned upstream `scripts/build-registry.mjs` derives `website/registry.json` from validated spec front matter and paired schemas. This reproduction requires an external upstream checkout and npm toolchain; **the full upstream build was subsequently executed successfully in CI**. The successful full build and reconciliation are evidenced by workflow run 44263516864; semantic-review completeness remains open. Even a successful reconciliation would not establish DTFC semantic-review completeness.
