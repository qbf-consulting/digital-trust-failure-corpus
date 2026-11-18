# Trust Tasks × DTFC: discovery versions, complete author case examination

**18 November 2026 · DTFC issue [#135](https://github.com/qbf-consulting/digital-trust-failure-corpus/issues/135)**  
**Pinned Trust Tasks source:** [f21a98ec](https://github.com/trustoverip/dtgwg-trust-tasks-tf/tree/f21a98ec8383352d18629a08dd5dd23935456142)  
**Machine-readable decisions:** [discovery-case-examination.json](https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/main/research/external-sources/trust-tasks/discovery-case-examination.json)

## Scope and admissible claim

Every one of the **four** published `trust-task-discovery` source versions has been considered against all **37** canonical DTFC propositions, including cases whose preconditions are **not established from the task specification**. The resulting 148 case-level author decisions are pinned to the exact source spec and payload schema.

| Source version | Canonical cases considered | Conditional candidate cells | Not established from source |
|---|---:|---:|---:|
| [0.1](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/trust-task-discovery/0.1/spec.md) | 37 | 9 | 28 |
| [0.2](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/trust-task-discovery/0.2/spec.md) | 37 | 9 | 28 |
| [0.3](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/trust-task-discovery/0.3/spec.md) | 37 | 10 | 27 |
| [0.4](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/trust-task-discovery/0.4/spec.md) | 37 | 10 | 27 |
| **Total** | **148** | **38** | **110** |

These are not independently accepted case mappings, vulnerabilities or executed consumer results. A case that cannot be established **from discovery alone** may be relevant to a later composed operation. Positive candidates are conditional on the full canonical preconditions, an actual relying proposition and observed consumer behavior.

## Four distinct semantic versions, not one latest-only shortcut

| Version | Material distinguishing behavior | Interoperability and assurance consequence |
|---|---|---|
| `0.1` | `frameworkVersion` represents MAJOR.MINOR and includes `supportedTypes` with advisory `requiredExt`. | Cannot assert specific PATCH baseline or authority to execute from the advertised list. |
| `0.2` | `frameworkVersion` becomes MAJOR.MINOR.PATCH. The 0.1 schema cannot accept a 0.2 three-part value as-is. | Exact framework compatibility cannot be inferred by silently retyping 0.2 as 0.1. |
| `0.3` | Adds optional `acceptanceWindow` with `maxAgeSeconds` and `clockSkewSeconds`, governing `issuedAt`. | An older discovery client with closed schema rejects the new field; `issuedAt` bounds may differ from a consumer honoring `expiresAt`. |
| `0.4` | Adds `expiryHorizonSeconds` to distinguish stated `expiresAt` from age limits on documents without expiry. | An already signed document can be outside current acceptance rules; 0.3's narrower window must not be assumed to describe 0.4's expiry behavior. |

Each changed source version has an explicit delta record in the machine matrix. The source's version fallback guidance is not a license to inherit a later version's temporal or evidence semantics.

## Actionable negative/control cases for DTG / Trust Tasks

### 1. A recognized task type is not execution authority

Discovery is explicitly advisory and the following task must still pass its own consumer acceptance pipeline. A successful response may be authenticated without granting any principal a mandate. If a system treats `supportedTypes` as authorization, it crosses the **capability-to-authority** boundary. Candidate DTF-013, DTF-018 and DTF-028.

**Negative test:** Advertise a supported privileged type to an unauthorized principal, then submit that type. The consequent execution must be rejected unless a separately competent authority authorizes the actor. Positive control: supported type plus genuine current scoped authorization passes when all other acceptance conditions are met.

### 2. Pattern-filtered absence is not global absence

The response includes only Type URIs matched by the supplied patterns. An empty response or incomplete subset is scoped to the request, not proof that the responder implements nothing anywhere. A downstream global absence PASS can instantiate DTF-010/026 when the claimed proposition needs evidence absent from the query.

**Negative test:** Query a single pattern while the responder supports an unrelated family, then try to conclude the responder has no other capabilities. The conclusion must stay scoped or indeterminate. A full enumeration with positive completeness evidence is the relevant control.

### 3. `requiredExt` is a claim about responder policy, not permission to disclose

Every examined version already says that required extension namespaces are **untrusted advisory input** and must not cause the producer to collect or attach data it was not otherwise authorized to provide. A deliberately misleading responder may advertise a sensitive extension, but correct producer behavior is to decline the exchange rather than expand disclosure.

**Negative test:** Return a supported type with `requiredExt` naming data the producer's own policy forbids disclosing. The producer must reject or decline. This is an important independent **disclosure-policy test**, but first-time over-disclosure is **not automatically DTF-034**: that canonical case requires an initially legitimate disclosure and later materially different secondary processing. The corpus must not manufacture a positive mapping by ignoring that precondition.

### 4. Temporal compatibility is a consumer decision, not a discovery promise

For 0.3 and 0.4, acceptance-window metadata is time- and context-specific. 0.4 distinguishes a consumer honoring stated `expiresAt` within `expiryHorizonSeconds` from max-age treatment of documents without expiry. A cached window is insufficient evidence of a later consumer's effective current policy. Conditional DTF-011 and DTF-021.

**Negative test:** Cache a broad discovery window and later configure the responder with a narrower temporal bound. Submit a document valid under the cached window but invalid under current policy. The consuming executor must reject it. Control: a document meeting the actual latest bound and all authority requirements.

### 5. Negotiation success is not a composed assurance verdict

A discovery response can be perfectly conformant, including origin authentication and valid schema, while a later task is malformed, unauthorized, beyond the accepted window or simply never executed. DTF-022, DTF-023 and DTF-027 become relevant when a consumer promotes a successful negotiation to overall execution or assurance PASS.

**Negative test:** Complete discovery, then fail the subsequent material authorization. Ensure audit/reporting does not claim successful execution or substantive governance assurance.

## Reproduction and review boundary

```sh
python -m tools.validate_discovery_case_examination
python -m unittest discover -s tests -v
python tools/validate.py
```

The generic family validation contract checks exact version membership, full 37-case comparison, pinned spec/schema hashes, explicit source-delta claims and false-success controls. Independent acceptance, execution of the proposed tests and registry-wide substantive completion are **not** asserted. The repository's existing pinned registry remains the source of inventory truth.
