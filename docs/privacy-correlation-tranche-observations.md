# Privacy and correlation tranche observations

## Purpose

This note records the modeling observations behind DTF-032 through DTF-037. The tranche was pressure-tested against the W3C **Verifiable Credentials Data Model Threat Model v2.1**:

https://www.w3.org/TR/vc-data-model-threat-model/

At the time of authoring, that W3C document is a draft/work in progress. It is treated as research provenance, not as authority for Digital Trust Failure Corpus semantics.

## Result

Six materially distinct privacy/correlation failures fit the existing DTF v0.1.0 contract without schema expansion:

- securing-mechanism metadata creates cross-context correlation;
- status resolution exposes presentation activity;
- initially legitimate disclosure is reused beyond its relying purpose;
- an authoritative participant defeats an intended unlinkability property;
- individually minimal disclosures compose into identification or profiling;
- retained verification artefacts become a durable correlation surface.

The existing `privacy`, `credential`, `composition`, `evidence`, `lifecycle`, and `governance` domains are sufficient.

The existing `correlation`, `policy-mismatch`, and `provenance` failure classes are also sufficient for this tranche. No new `purpose-violation`, `surveillance`, or `retention` failure-class enum is justified yet.

## Important judgment

The cases deliberately distinguish **functional or cryptographic success** from **privacy assurance**.

A credential can be authentic. Its signature can verify. Its status can be current. Its issuer can be legitimate. Every local component can satisfy its own contract.

None of those facts, by themselves, establish that:

- proof machinery is unlinkable;
- status checking is unobservable;
- disclosed data is used only for its relying purpose;
- an issuer-controlled surface preserves the claimed privacy property;
- a combined disclosure remains non-identifying;
- retained evidence cannot later reconstruct activity.

This is the central assurance value of the tranche.

## Taxonomy pressure

DTF-034 and DTF-037 create mild pressure toward a future concept such as purpose/lifecycle misuse, but the existing `policy-mismatch` class expresses the current propositions without distortion.

That pressure should remain observational until additional independent cases demonstrate that a stable new failure class is necessary.

## Boundary

The tranche does not make DTF a generic privacy threat encyclopedia. It captures failure propositions that are reusable across digital-trust systems and that can be expressed through evidence requirements and falsification criteria under the existing contract.
