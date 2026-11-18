# Trust Tasks × DTFC: governance capabilities, complete author case examination

**18 November 2026 · Research output for [#135](https://github.com/qbf-consulting/digital-trust-failure-corpus/issues/135)**

**Pinned source authority:** [Trust Tasks commit f21a98e](https://github.com/trustoverip/dtgwg-trust-tasks-tf/tree/f21a98ec8383352d18629a08dd5dd23935456142).  
**Machine-readable case decisions:** [governance-case-examination.json](https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/main/research/external-sources/trust-tasks/governance-case-examination.json).

## Scope and evidence level

All **three** versioned `governance/capability` operations are assessed against all **37** existing canonical DTFC propositions. Each of the 111 comparisons contains a case-specific disposition and explanation. The task schemas, actual source texts and case propositions were examined together; this is a complete **author-side case consideration for this family**, not a comprehensive claim about any deployment or independent reviewer acceptance.

| Versioned operation | Case comparisons | Conditional candidates | Not established from task |
|---|---:|---:|---:|
| [disable/0.1](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/governance/capability/disable/0.1/spec.md) | 37 | 6 | 31 |
| [enable/0.1](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/governance/capability/enable/0.1/spec.md) | 37 | 7 | 30 |
| [list/0.1](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/governance/capability/list/0.1/spec.md) | 37 | 5 | 32 |
| **Total** | **111** | **18** | **93** |

`Not-established-from-task` means the task specification alone does not establish that canonical case's entire precondition and trigger. It is **not** a final reviewed no-match for arbitrary consumer compositions, implementation safety or evidence of execution. The 18 candidate cells include overlapping conditional hypotheses and are not 18 verified failures.

## Material findings and implementable DTG negative tests

### 1. Capability enablement is an authority-changing operation

`enable` activates Trust Task handlers, advertises capabilities and begins membership lifecycle hooks. A valid signed request cannot replace the host's explicit **community operator role** check. With a companion capability, `delegate` creates a namespace delegation and the host must constrain registry writes to the declared `manifest.vocabulary.actions`.

**Challenge cases:** DTF-002, DTF-013, DTF-023, DTF-028. A negative test should authenticate a non-operator with a valid proof and attempt enablement, then enable a legitimate companion but attempt out-of-vocabulary registry writes. Distinguish invalid actor authority, valid bounded delegation and broken composition enforcement. A valid manifest or attractive human-readable `title` cannot authorize an action.

### 2. Disabling stops execution but preserves historical records

`disable` removes handlers and discovery advertisements while retaining registry records for historical audit. A cached positive capability advertisement is not a current execution permit. Historical records must not disappear or be represented as never valid merely because the module is disabled today.

**Challenge cases:** DTF-005, DTF-006, DTF-016, DTF-021. Establish an enabled record, disable the module during a long-running interaction, and attempt a later material handler operation. It must use current host state. Separately demonstrate that a decision valid before disabling remains reconstructable for the relevant historical question. These are **different temporal propositions** and require different tests.

### 3. Management availability is neither current enablement nor authority

`list` returns capabilities with `enabled` flags. An absent request filter defaults to `enabled`, while `status=available` intentionally exposes capabilities that *could* be enabled. The management surface may legitimately reveal a manifest without establishing that handlers will run or that the requester may commit an action.

**Challenge cases:** DTF-010, DTF-011, DTF-018, DTF-021, DTF-028. Query an available-but-disabled capability, then test independent enablement and role checks at the material execution boundary. Replay a previously enabled list after an intervening disable. Distinguish a missing-evidence false PASS from capability advertisement laundering into principal authority.

### 4. Execution success, policy acceptance and governance assurance are distinct

The enable response reports an active state and the disable response an inactive state. That local response cannot by itself prove every external adapter and derived consumer has synchronized effective enforcement. This is a conditional **DTF-027** seam when a consumer asserts broader assurance than the host result actually establishes.

**Negative/control pair:** Observe an accurate host state transition, then exercise an adapter with a stale cache. A host success result can be valid while a global enforcement claim is unproven. The corresponding safe control requires a current adapter decision, not merely replay of the management response.

## Source interpretation and boundaries

The enable source already mandates operator-only activation and out-of-vocabulary delegation rejection; the disable source already defines handler shutdown and historical-record retention; the list source distinguishes `available` from `enabled`. These rules are **source safeguards**, not findings that the upstream specifications are defective. The risk arises if a consuming system misapplies or fails to enforce those rules.

The machine matrix separately covers less plausible propositions. For example, there is no N-of-M independent-approval assertion solely from `enable`, no credential-presentation status-resolution privacy channel from `list`, and no claim of a fully valid historical mandate from `disable`. Treating such unestablished cases as definite no-matches without examining a real composed relying decision would be unsound.

## Reproduction and status

```sh
python -m tools.validate_governance_case_examination
python -m unittest discover -s tests -v
python tools/validate.py
```

Validation rejects missing/duplicate cases, omitted versions, mismatched pinned source or schema digests, candidate tests without authority boundaries, unsupported no-match promotion, and invented independent acceptance. **Target execution and institutional acceptance remain unestablished.**

Alongside the [audit family examination](trust-tasks-audit-case-examination.md), this provides two complete, source-pinned author-side family comparisons for DTG and Trust Tasks contributors. It does not change the aggregate 51 preliminary screenings, prove registry-wide Gate B completion, or justify a completeness release.
