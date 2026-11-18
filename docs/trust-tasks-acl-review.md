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
