# Trust Tasks × DTFC: audit family, complete author-side case examination

**Research result:** 18 November 2026. Tracks [#135](https://github.com/qbf-consulting/digital-trust-failure-corpus/issues/135).  
**Task authority:** [pinned Trust Tasks source](https://github.com/trustoverip/dtgwg-trust-tasks-tf/tree/f21a98ec8383352d18629a08dd5dd23935456142).  
**Case authority:** the 37 existing canonical DTFC propositions.  
**Machine evidence:** [audit-case-examination.json](https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/main/research/external-sources/trust-tasks/audit-case-examination.json).

## Research claim and limitations

This is **the complete 37-case author-side comparison for all three pinned audit task versions**, not an independent semantic acceptance or assertion that all 37 cases are inapplicable to any real consumer. The matrix records each case as either a **conditional-candidate** with a falsifiable consumer-boundary hypothesis, or **not-established-from-task** with a reason the specified task behavior does not establish the case's material preconditions. The latter means **not proven by task semantics**, not a globally safe operation, a reviewed no-match for the complete deployment, or a claim that the failure can never occur.

The full existing corpus was considered case by case. The report does **not** claim to observe any consumer implementation. Proposed negative tests remain unexecuted. No independent reviewer has accepted these conclusions. The original 51-source-screened / 1,340-pending count is unchanged; this record adds depth, not newly screened versions.

| Pinned task | Canonical case comparisons | Conditional candidates | Not established from task | Independent approvals |
|---|---:|---:|---:|---:|
| [audit/list/0.1](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/audit/list/0.1/spec.md) | 37 | 9 | 28 | 0 |
| [audit/list/0.2](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/audit/list/0.2/spec.md) | 37 | 9 | 28 | 0 |
| [audit/verify/0.1](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/audit/verify/0.1/spec.md) | 37 | 5 | 32 | 0 |
| **Total** | **111** | **23** | **88** | **0** |

The 23 cells are **conditional hypotheses**, not 23 separate incidents, vulnerabilities or new canonical cases. Most are repetitions of a small number of consumer mechanisms across the two published list versions. See the machine file for the **individual rationale and case ID on every one of the 111 comparisons**, including rejected or unestablished alternatives.

## Findings actionable to DTG and Trust Tasks

### 1. An audit reader is a second evidence authority boundary

An authorized `audit/list` response exposes full entries, including actor/target DIDs and an unbounded `detail` object. It requires a signed request and signed response; this makes the read attributable, **not reusable for an unrelated purpose**. An auditor can hold an immutable signed snapshot after the maintainer has redacted its live store. This is a testable downstream governance problem under **DTF-034** (subsequent use beyond purpose) and **DTF-037** (retained evidence as a durable correlation surface), not a claim that the task fails to define privacy obligations.

**Negative/control pair:** authorize a scoped oversight query and retain it for its specified audit period; then attempt reusing the actor history for member scoring or retain an identifiable copy after the permitted purpose has expired. Test separate read authorization, secondary-use policy and independent-copy erasure rules. The former is a legitimate bounded read; the latter requires fresh authorization or rejection.

### 2. Audit evidence completeness is a separate proposition from a signed page

`audit/list/0.1` uses `truncated` plus a returned `cursor`; `audit/list/0.2` uses `nextCursor` presence/absence. A version-0.2 client silently relying on 0.1's `truncated` semantics can misread an incomplete page as exhaustive. Both versions also permit filters and opaque continuation that must retain query scope.

**Negative/control pair:** place a material contradicting event beyond page one, return a valid first page, and determine whether the auditor claims no matching event exists. Then repeat after following every required continuation under the same filters. Candidate **DTF-010/026** conclusions require an actual relying proposition that needs complete evidence.

### 3. Chain integrity and historical accountability are non-equivalent

`audit/verify/0.1` reports internal consistency, `legacySkipped`, `unparseableSkipped` and `head`. It explicitly states that the check does not authenticate an adversary-controlled store and that a valid-prefix truncation can evade local self-verification. A reviewer cannot use `verified: true` alone as authentic, complete, independently anchored or decision-time-authorized history.

**Negative/control pair:** recompute a self-consistent chain over a modified or truncated store and request a historical-authority determination. Compare a false substantive PASS with a result limited to locally observed integrity. Candidates include **DTF-010, DTF-019, DTF-025, DTF-026 and DTF-027**, conditional on the consumer's asserted proposition.

### 4. Review non-matches must preserve their predicates

The matrix does not label a case negative merely because the operation is read-only. For example, DTF-013 requires an authenticated actor making a material commitment *without action-specific authority*, not simply a signed audit query. DTF-024 requires an independence claim about N-of-M approvals, not an audit event mentioning approvals. DTF-033 requires status resolution that exposes credential-use activity, not every metadata-bearing read. These predicates explain why a mechanism is not established by these task specifications; an implementation or composed workflow could introduce them.

## Version-specific finding

Upstream 0.2 expressly documents a breaking wire change: request `pageSize` → `limit`, response `cursor`/`truncated` → `nextCursor`. Despite the intended paging equivalence, each version's evidence of completion must be interpreted using **its own fields**. The machine file records this delta and independently anchors both versions to distinct Git blobs. **No blanket historical equivalence** or carry-forward of unexamined semantics is asserted.

## Reproduction and falsification

Run the repository's existing test entrypoint and the direct bounded validator:

```sh
python -m tools.validate_audit_case_examination
python -m unittest tests.test_audit_case_examination -v
python -m unittest discover -s tests -v
python tools/validate.py
```

The case-matrix validator reconciles exactly three audit versions against the pinned inventory, checks all 37 canonical IDs in each row, verifies source spec/schema blobs, rejects duplicate and omitted comparisons, rejects unsubstantiated no-match or independent approval, and requires a distinct authority boundary and negative test for each conditional candidate.

For further work, replicate this **source-specific complete-case examination** in other task families, prioritizing critical consumer trust boundaries before extending to the long `vta`/`vtc` histories. Use explicit version deltas only where source semantics permit them. Do not promote structural completeness or AI-assisted challenge into independent semantic acceptance.

## Publication decision

**Publish as comprehensive author-side research for the pinned audit family** and as a bounded negative-test agenda for DTG and Trust Tasks. **Do not claim registry-wide Gate B completion**, independent acceptance or executed conformance. No completeness release follows solely from this evidence.
