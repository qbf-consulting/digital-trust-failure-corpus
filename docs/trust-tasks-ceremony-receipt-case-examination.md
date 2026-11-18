# Trust Ceremony Receipt × DTFC: complete author-side case examination

**Source-pinned research · 18 November 2026 · [Issue #135](https://github.com/qbf-consulting/digital-trust-failure-corpus/issues/135)**  
**Upstream:** [Trust Ceremony Receipt 0.1](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/f21a98ec8383352d18629a08dd5dd23935456142/specs/trust-ceremony-receipt/0.1/spec.md)  
**Case-level evidence:** [ceremony-receipt-case-examination.json](https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/main/research/external-sources/trust-tasks/ceremony-receipt-case-examination.json).

## Scope and evidence claims

The pinned receipt specification has been individually considered against all **37 canonical DTFC propositions**. The author matrix records **17 conditional applicability hypotheses** and **20 propositions whose complete preconditions are not established by the task source**. Every decision pins canonical case version `0.1.0` and the exact upstream specification/schema Git blobs. These are neither 17 observed defects nor 20 independently accepted deployment no-matches. No external test or independent semantic approval is claimed.

The specification's deliberate separation of **recorder attestation**, **step content proofs**, **definition-derived completion**, and **later action authority** is the primary finding. Conforming behavior already contains several appropriate safeguards. The relevant DTFC research concerns consumers who misinterpret a narrower observation as a stronger proposition.

## Findings and testable consumer failures

### 1. A recorder-signed receipt cannot prove everything about an enactment

The recorder attests an ordered enumeration. It does not authenticate the contents of each step, and its `payload.complete` is not an authoritative verifier verdict. The verifier must resolve the pinned definition, count unique admissible steps, independently evaluate its completion rule and validate any terminal marker using the signed **step document**, not merely `steps[].terminal`. Without the terminal document, it cannot verify completion.

**Negative/control pair:** Provide a correctly signed receipt with `payload.complete=true` but withhold the signed terminal document and, where relevant, the definition. A verifier must report that completion cannot be established rather than return a substantive PASS. When the definition, signed terminal marker, required role bindings, and held step evidence are available and consistent, it may issue the narrower result supported by those observations. Conditional **DTF-010, DTF-026, DTF-027, DTF-030**.

### 2. A valid prefix and a complete history are different propositions

Signed step digests and `ceremony.prev` detect omitted links only when a verifier holds a successor that commits to them. A missing intermediate step with no held successor is not necessarily detectable. The terminal marker is required to detect tail truncation; the recorder's echo is not enough. `maxDuration` is not assessable from a receipt lacking individual step timestamps.

**Negative/control pair:** Offer an internally valid enumeration missing an unobserved step and assert the complete historical flow and elapsed-time conformity. Require `INDETERMINATE` for those stronger propositions until the necessary signed records and timestamps are available. Conditional **DTF-011, DTF-026**.

### 3. Numeric threshold is not independent approval

The specification rejects duplicate step IDs and constrains `multiplicity: perRole` and `threshold.ofStep` counting. Where the threshold specifically counts **approval steps**, however, independently controlled approvers are a different governance proposition. A definition that only requires distinct issuers does not silently supply independence across organizational control domains.

**Negative/control pair:** Meet a threshold of approval steps using distinct signing identifiers under common control; challenge a relying policy's stronger independent-approval PASS. A legitimate count-only policy can correctly accept the threshold without asserting independent governance. Conditional **DTF-007, DTF-024, DTF-025** when their respective independence or assurance-strength preconditions apply.

### 4. Receipt completion does not authorize a new commitment

The source explicitly states that ceremony membership and a signed receipt grant no material permission. The recorder's competence to attest enactment cannot be promoted into a principal-derived mandate for a privileged task. A nested ceremony also requires separate child-receipt evaluation; parent confirmation alone cannot certify unseen child content.

**Negative/control pair:** Present a genuine receipt to an authorization gate without a scoped principal mandate, or assert nested end-to-end completion without verifying the child's receipt. Demand DENY or INDETERMINATE as appropriate. Conditional **DTF-013, DTF-019, DTF-022, DTF-023, DTF-028**, dependent on the exact relying proposition.

### 5. Verification evidence can create its own privacy failure

The bearer receipt can enumerate roles, stable issuer VIDs, step types and ordering. No recipient binding is required, but *bearer* does not mean unrestricted distribution. The per-enactment salt supports digest privacy only against parties without it, not holders of the receipt. Where a ceremony requires `enactmentPrivacy: blinded`, full participant enumeration cannot automatically be treated as privacy-preserving.

**Negative/control pair:** Collect and join legitimately obtained receipts across otherwise disjoint audiences; determine whether participants can be linked or a sensitive process reconstructed. Independently establish purpose, distribution and retention policy. Conditional **DTF-034, DTF-035, DTF-036, DTF-037** where the actual privacy claims and retention conditions are satisfied.

## Admissible conclusion

A receipt can establish a recorder's attributable, definition-scoped observation even when it cannot establish independently verified enactment completion. That limited result is meaningful and should not be wrongly called defective. Conversely, passing local signature, schema and digest checks must not be expanded into complete-history, authorization, independent approval or privacy assurances without the required additional evidence.

The [37-case machine matrix](https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/main/research/external-sources/trust-tasks/ceremony-receipt-case-examination.json) contains case-by-case rationale, including non-established alternatives and test boundaries. All tests above are **proposed negative/control pairs**, not executed implementation observations.

## Reproduction

```sh
python -m tools.validate_ceremony_receipt_case_examination
python -m unittest tests.test_ceremony_receipt_case_examination -v
python -m unittest discover -s tests -v
python tools/validate.py
```

This is a newly source-screened task version, bringing source-screening to 52 of 1,391; it also has a complete author-side 37-case examination. Review and execution remain separately unestablished. The full #135 Gate B remains incomplete.
