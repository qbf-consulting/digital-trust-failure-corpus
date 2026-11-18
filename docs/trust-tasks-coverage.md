# Trust Tasks applicability coverage (derived research)

Generated from the pinned DTFC inventory, the original 12-task screening and the bounded ACL review.
This page does not establish upstream publication status, independent semantic review, or execution evidence.

**Upstream revision:** `f21a98ec8383352d18629a08dd5dd23935456142`  
**Versioned source pairs:** 1391  
**Original pilot:** 12  
**ACL source screening:** 7  
**Overlap:** 3  
**Distinct source-screened versions:** 16  
**Not yet source-screened:** 1375  

Screened means DTFC-authored research mapping, **not** independent verification or all-case semantic completeness.
Historical versions do not inherit screened status from a later version.

| Family | Source versions | Original pilot | ACL screening | Distinct screened | Pending |
|---|---:|---:|---:|---:|---:|
| `acl` | 20 | 3 | 7 | 7 | 13 |
| `audit` | 3 | 0 | 0 | 0 | 3 |
| `auth` | 79 | 1 | 0 | 1 | 78 |
| `backup` | 7 | 0 | 0 | 0 | 7 |
| `chat` | 1 | 0 | 0 | 0 | 1 |
| `config` | 4 | 0 | 0 | 0 | 4 |
| `confirm` | 2 | 0 | 0 | 0 | 2 |
| `consent` | 8 | 0 | 0 | 0 | 8 |
| `credential-exchange` | 8 | 3 | 0 | 3 | 5 |
| `device` | 13 | 0 | 0 | 0 | 13 |
| `did-management` | 60 | 0 | 0 | 0 | 60 |
| `external` | 31 | 0 | 0 | 0 | 31 |
| `git-ns` | 86 | 0 | 0 | 0 | 86 |
| `git-trust` | 2 | 0 | 0 | 0 | 2 |
| `governance` | 3 | 0 | 0 | 0 | 3 |
| `keys` | 17 | 0 | 0 | 0 | 17 |
| `messaging` | 50 | 0 | 0 | 0 | 50 |
| `notifications` | 2 | 0 | 0 | 0 | 2 |
| `peer-check` | 1 | 0 | 0 | 0 | 1 |
| `persona` | 57 | 0 | 0 | 0 | 57 |
| `policy` | 14 | 3 | 0 | 3 | 11 |
| `process-attestation` | 1 | 0 | 0 | 0 | 1 |
| `provision` | 5 | 0 | 0 | 0 | 5 |
| `push` | 6 | 0 | 0 | 0 | 6 |
| `registry` | 18 | 2 | 0 | 2 | 16 |
| `rooms` | 123 | 0 | 0 | 0 | 123 |
| `sync` | 2 | 0 | 0 | 0 | 2 |
| `task-consent` | 4 | 0 | 0 | 0 | 4 |
| `trust-ceremony-receipt` | 1 | 0 | 0 | 0 | 1 |
| `trust-task-control` | 1 | 0 | 0 | 0 | 1 |
| `trust-task-discovery` | 4 | 0 | 0 | 0 | 4 |
| `trust-task-error` | 6 | 0 | 0 | 0 | 6 |
| `trust-task-next-step` | 1 | 0 | 0 | 0 | 1 |
| `trust-task-ok` | 1 | 0 | 0 | 0 | 1 |
| `vault` | 34 | 0 | 0 | 0 | 34 |
| `vetting` | 4 | 0 | 0 | 0 | 4 |
| `voting` | 25 | 0 | 0 | 0 | 25 |
| `vrc` | 2 | 0 | 0 | 0 | 2 |
| `vta` | 239 | 0 | 0 | 0 | 239 |
| `vtc` | 397 | 0 | 0 | 0 | 397 |
| `vtn` | 35 | 0 | 0 | 0 | 35 |
| `webvh` | 10 | 0 | 0 | 0 | 10 |
| `witness` | 4 | 0 | 0 | 0 | 4 |

## Interpretation and reproduction

Each row is an inventory item, not an assurance result. Source status, publication eligibility and
version-delta equivalence still require upstream front-matter and registry reconciliation.
A screened task may have more applicable DTFC cases than currently documented; a pending task
is not a reviewed no-match. A mapping hypothesis is not evidence that an implementation failed.

Run `python -m tools.trust_tasks_coverage` to emit this page's content or
`python -m tools.trust_tasks_coverage --check` to reject documentation drift.
The repository unit tests independently exercise false-success and missing-input conditions.
