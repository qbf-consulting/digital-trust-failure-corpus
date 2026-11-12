# Trust Tasks Registry: bounded failure-applicability crosswalk

Tracked by [DTFC issue #132](https://github.com/qbf-consulting/digital-trust-failure-corpus/issues/132). Source: [Trust Tasks Registry](https://trusttasks.org/registry), governed by the [upstream Trust Tasks repository](https://github.com/trustoverip/dtgwg-trust-tasks-tf). The [machine-readable screening register](https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/main/research/external-sources/trust-tasks/mapping.json) is a **derived, non-normative DTFC research artifact**.

## Research question and rationale

Can existing DTFC failure propositions be connected to specific, versioned Trust Tasks so a reviewer can identify **testable assurance scenarios** without confusing task schema conformance, runtime policy authorization, and actual implementation behavior? The bounded exercise tests usefulness of a source-pinned operation vocabulary before committing to an exhaustive mapping. It is not a taxonomy equivalence exercise, registry coverage score, Trust Tasks conformance claim, or external-consumption demonstration.

The registry describes transport-agnostic operations; DTFC identifies independently falsifiable trust-system failures. An operation may be correctly specified and correctly executed while the consuming system incorrectly infers authority, freshness, privacy, or assurance. **A mapped risk is not a defect report against Trust Tasks.**

## Source, sample and authority

- Upstream authority: `trustoverip/dtgwg-trust-tasks-tf` at immutable commit [`f21a98ec8383352d18629a08dd5dd23935456142`](https://github.com/trustoverip/dtgwg-trust-tasks-tf/tree/f21a98ec8383352d18629a08dd5dd23935456142).
- DTFC source authority: existing canonical `corpus/DTF-*.json` propositions; mappings do not amend their semantics.
- Twelve versioned **draft** specifications, selected from five families (`acl`, `auth`, `credential-exchange`, `registry`, `policy`).
- Selection emphasizes distinct authority, revocation, identity/proof, privacy, recognition, and policy-evaluation boundaries. It is purposive, not statistically representative; task families `vta`, `vtc`, `vault`, `audit`, `voting`, etc. were deliberately not screened here.

## Family screening (discovery only)

| Family | Candidate DTFC mechanisms | Limitation |
| --- | --- | --- |
| `acl` | Scope escalation, revocation after commitment, stale role state | Only three selected operations inspected |
| `auth` | Session lifecycle and token invalidation | Only revoke-session inspected |
| `credential-exchange` | Correlation, disclosure purpose, proof/authority separation | Depends on formats and relying-party policy |
| `registry` | Recognition/authorization distinction, policy/time applicability | Query outcomes are not universal permissions |
| `policy` | Dry-run/assurance substitution, quorum interpretation, policy freshness | Implementation enforcement is not proved |

A family row is **not** a mapping for all its members. Do not infer absence of failure from an unlisted family.

## Versioned task judgments

| Task (version) | DTFC case | Screening | Distinguishing basis |
| --- | --- | --- | --- |
| [`acl/change-role/0.3`](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/acl/change-role/0.3/spec.md) | DTF-021 | `mechanism-overlap` | Role changes use current-role compare-and-swap and ordered updates; reusing a pre-change role check at a later privileged action crosses the lifecycle boundary. |
| [`acl/grant/0.3`](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/acl/grant/0.3/spec.md) | DTF-002 | `mechanism-overlap` | A grant can overrun the granting principal's permitted act/approve/capability ceiling if the maintainer substitutes a signed request for a scoped authority check. |
| [`acl/grant/0.3`](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/acl/grant/0.3/spec.md) | DTF-034 | `adjacent` | The grant includes named purposes for later reads, creating a potential downstream purpose-overrun boundary distinct from correctness of grant acceptance. |
| [`acl/revoke/0.3`](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/acl/revoke/0.3/spec.md) | DTF-016 | `mechanism-overlap` | The specification makes revoked authority effective at the next authorization decision, exposing a time-of-check boundary for in-flight or subsequent decisions. |
| [`auth/revoke-session/0.2`](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/auth/revoke-session/0.2/spec.md) | DTF-004 | `mechanism-overlap` | The specified session revocation requires subsequent access and refresh-token uses to fail; retaining a stale session state would defeat the lifecycle transition. |
| [`credential-exchange/issue/0.1`](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/credential-exchange/issue/0.1/spec.md) | DTF-025 | `adjacent` | The specification distinguishes credential issuer signature from the delivery envelope proof; combining valid proofs does not establish stronger governance assurance than either supports. |
| [`credential-exchange/present/0.1`](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/credential-exchange/present/0.1/spec.md) | DTF-032 | `adjacent` | The specification binds a presentation to verifier nonce and audience while disclosing holder claims; other proof or envelope metadata may still be cross-context correlatable. |
| [`credential-exchange/present/0.1`](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/credential-exchange/present/0.1/spec.md) | DTF-034 | `mechanism-overlap` | The stated presentation purpose restricts subsequent reuse, while the verifier retains disclosed material; a valid presentation need not authorize secondary use. |
| [`credential-exchange/request/0.1`](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/credential-exchange/request/0.1/spec.md) | DTF-013 | `adjacent` | A holder's key-binding proof and task document proof establish different facts; treating possession of a signing key as sufficient issuing authority would substitute proof for permission. |
| [`policy/activate/0.1`](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/policy/activate/0.1/spec.md) | DTF-021 | `mechanism-overlap` | Activation changes the authoritative policy for a purpose immediately; continued use of a cached previous policy at a later material decision creates a lifecycle-stage mismatch. |
| [`policy/evaluate/0.4`](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/policy/evaluate/0.4/spec.md) | DTF-024 | `adjacent` | The requireConsent decision now carries explicit quorum and requester-exclusion members; a consumer may still misinterpret the count as independent approval. |
| [`policy/evaluate/0.4`](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/policy/evaluate/0.4/spec.md) | DTF-027 | `mechanism-overlap` | The task is explicitly a non-persisting dry-run; interpreting its successful output as a deployed policy or effective runtime decision confuses process success with assurance. |
| [`policy/upsert/0.3`](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/policy/upsert/0.3/spec.md) | DTF-012 | `mechanism-overlap` | Version-checked policy updates affect subsequent requests; a stale module, out-of-order write or policy/version mismatch can make a decision rely on obsolete policy. |
| [`registry/authorization/0.2`](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/registry/authorization/0.2/spec.md) | DTF-012 | `mechanism-overlap` | An authorization query is evaluated under an authority-defined action/resource vocabulary and a validity window; a response can be misused when its policy or evaluation context no longer applies. |
| [`registry/recognition/0.2`](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/registry/recognition/0.2/spec.md) | DTF-028 | `mechanism-overlap` | Recognition and authorization are separate registry operations; treating a positive recognition response as permission to act launders a non-authorizing signal. |

The full register records a **separate test hypothesis and authority boundary for every judgment**. `mechanism-overlap` indicates a concrete potential failure mechanism at the task/consumer seam. `adjacent` means additional conditions are necessary before the existing DTF proposition is applicable. Neither is a verified vulnerability or an executed case. `not-established` is a supported classification for future screening, not an assertion of safety.

## Interpretation and negative controls

1. A positive registry *recognition* result must not be used as *authorization*; this is a candidate DTF-028 consumer error, not evidence that the recognition task itself is defective.
2. A policy `evaluate` dry-run returning a decision does not establish that the decision is active or enforced. DTF-027 is an interpretation boundary.
3. The credential `present` task has audience/nonce binding and purpose constraints; correlation and secondary-use failures depend on surrounding wallet, verifier and operational policies.
4. Signed ACL mutations do not themselves prove a subsequent runtime authorization is current. Revocation and role-change mappings require execution-time observations.

All selected upstream task specifications are labelled **draft**. Each mapping is pinned to its exact source version, and a newer upstream revision needs re-review. Source paths and reasoning are independently authored; no upstream specification text has been copied.

## Reproduction and limitations

From the repository root run:

```bash
python -m unittest tests.test_trust_tasks_crosswalk -v
python -m unittest discover -s tests -v
python tools/validate.py
python tools/build_docs.py
mkdocs build --strict
```

The offline tests verify mapping structure, uniqueness, pinned provenance, source-path grammar, case references, classifications, and fail-closed negative inputs. They **cannot** authenticate upstream source content or establish normative correctness. The source revision should be reviewed against the linked upstream files when performing substantive research review.

This research does **not** execute any Trust Task target or close [#48](https://github.com/qbf-consulting/digital-trust-failure-corpus/issues/48) or [#45](https://github.com/qbf-consulting/digital-trust-failure-corpus/issues/45). A future externally maintained target could be selected from the resulting hypotheses only after actual implementation semantics and consumer evidence requirements are demonstrated.

## Disposition

Keep this as an informative research sidecar. No new DTF case, canonical schema, taxonomy, main runtime dependency, API, or release is warranted. Additional registry coverage should follow only if an independent adopter finds this bounded mapping useful for selecting a reproducible adverse-condition test.
