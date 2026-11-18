# ACL source-specific research screening for DTFC #135

This is a **bounded screening of seven current ACL operation versions**, not an independently reviewed or exhaustive assessment of all 20 source versions. The [versioned register](https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/main/research/external-sources/trust-tasks/acl-review.json) holds source blob SHAs, canonical case versions, conditional applicability, negative-test hypotheses, and authority boundaries. The 13 other versions remain `needs-version-delta-review`; none inherits the current version's mapping.

| Source task | Existing DTF | Research classification | Material boundary |
|---|---|---|---|
| `change-role/0.3` | DTF-021 | `mechanism-overlap` | An earlier role observation is insufficient to establish current privilege after a demotion or another relevant state change. |
| `grant/0.3` | DTF-002 | `mechanism-overlap` | The ACL maintainer must bound the grant by the granter's authority, including the relevant capability and purpose scope; a valid signature does not enlarge delegation. |
| `list/0.4` | DTF-010 | `adjacent` | A filtered, paged ACL enumeration need not establish completeness of a revocation sweep; using a partial view as proof of no remaining grant requires conditions not supplied by the read alone. |
| `revoke/0.3` | DTF-021 | `mechanism-overlap` | Removing or narrowing an ACL entry does not prove that a later consumer refreshed a previously accepted grant or scope observation. |
| `show/0.3` | DTF-010 | `adjacent` | The maintainer may return entry:null to conceal existence under disclosure policy; this answer alone cannot positively establish absence of the underlying grant. |
| `swap-key/0.1` | DTF-004 | `mechanism-overlap` | Atomic rebinding of an ACL subject requires persistent authentication artifacts tied to the retired subject to be revoked; their acceptance after effect is a current-validity failure. |
| `update/0.3` | DTF-002 | `mechanism-overlap` | A purpose-widening or capability-changing ACL update remains bounded by the editor's authority; accepting an update beyond that bound produces scope escalation. |

## Version-delta caution

The upstream ACL source itself describes meaningful changes: `acl/list` changed pagination semantics between 0.2 and 0.3 and gained mandatory entry purposes in 0.4; `acl/grant`, `acl/update`, `acl/revoke`, `acl/show`, and `acl/change-role` gained or propagated purpose semantics in their newer versions. The initial `acl/swap-key/0.1` has no earlier source version in this pinned snapshot. No historical equivalence is asserted by these observations.

**Negative control:** `acl/swap-key/0.1` is *not established* as a DTF-032 unlinkability failure merely because it replaces a subject identifier. The relevant cross-context and linkability preconditions are not established.

## Reproduction

Run `python -m tools.validate_acl_review` and `python -m unittest tests.test_acl_review -v`. The checker fails closed on missing source versions, unsupported reviewed-status promotion, stale canonical case references, and fabricated independent evidence. This is **structural validation of source-qualified research judgments**, not independent semantic peer review or execution of the upstream tasks.

Further work: front-matter/catalogue reconciliation, material historical-version delta assessment, independently reviewed no-match decisions, broader families and generated coverage. An external reviewer must inspect the upstream source and challenge the DTFC mapping before treating any judgment as accepted assurance.

## Historical-version source-delta screening

All 13 historical ACL versions now carry a source-pinned baseline or material-change rationale in the research JSON. The six original 0.1 versions are baselines; the seven later historical versions are materially changed successors. The evidence includes version-specific source sections and Git blob identities.

**Crucial distinction:** the delta screening covers *why mapping inheritance cannot be assumed*. It does **not** constitute a DTFC applicability review of any historical version. The 13 historical applicability decisions remain `needs-review`, and no independent peer review or target execution is claimed. A later current-version mapping is not a historical mapping.

| Version transition | Material interpretive change |
|---|---|
| `acl/change-role/0.1 → 0.2` | Explicit authority ceilings, grantor bounds and capability rechecking |
| `acl/grant/0.1 → 0.2` | Explicit authorization axes, proof/issuedAt and grantor authority limits |
| `acl/list/0.1 → 0.2` | Hierarchical direction, capability/resource filters and AclEntry 0.2 |
| `acl/list/0.2 → 0.3` | Pagination wire fields and completeness signaling |
| `acl/revoke/0.1 → 0.2` | Explicit entry/act-scope revocation and next-decision effect |
| `acl/show/0.1 → 0.2` | Explicit authority fields and policy-constrained redaction |
| `acl/update/0.1 → 0.2` | Explicit authority fields, privilege-bound replacement, narrowing restrictions |

Later current revisions introduce the purpose-scoped 0.3 entry model (and `acl/list/0.4`). The current research is pinned to the upstream Git revision, including draft text, and should be challenged on its actual source semantics. Reproduce structural gates with `python -m tools.validate_acl_deltas`; passing validation alone does not attest that the mapping is semantically correct.

## Historical applicability research screening

The 13 historical ACL versions now have source-specific conditional mapping hypotheses, with local proposition, unsupported downstream inference, required evidence and a falsification test. These are DTFC-authored **research screenings**. They are not definitive no-match or all-case-complete determinations, independent reviews or execution results. The mapping contract forbids automatic version inheritance and the validator rejects assertions of independent approval. Together with seven current-version screenings, the ACL family's 20 source versions have initial conditional hypotheses, not exhaustive assurance.

Run `python -m unittest tests.test_historical_acl_screening -v` alongside the other ACL checks. Source-specific mappings may be challenged or superseded following independent review.
