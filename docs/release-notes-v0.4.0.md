# Digital Trust Failure Corpus v0.4.0

## Purpose

v0.4.0 expands the corpus from thirty-one to thirty-seven draft failure cases while retaining the existing failure-case schema v0.1.0 and bounded taxonomy.

The release adds the first substantive **privacy and correlation** tranche. These cases focus on failures that can remain invisible if assurance stops at credential authenticity, signature verification, current status, or local component conformance.

The governing release principle is:

> Cryptographic validity and local verification success do not establish privacy safety for the composed trust transaction.

## Added cases

- **DTF-032** — securing mechanism creates a cross-context correlator.
- **DTF-033** — status resolution exposes presentation activity.
- **DTF-034** — legitimate disclosure is reused beyond the relying purpose.
- **DTF-035** — an authoritative participant defeats intended unlinkability.
- **DTF-036** — individually minimal disclosures compose into identification or profiling.
- **DTF-037** — retained verification artefacts create a durable correlation surface.

## What the tranche establishes

The new cases make several distinctions executable:

- a payload can avoid stable identifiers while proof or securing metadata still creates a correlator;
- a status response can disclose nothing sensitive while the act, target, or timing of the lookup reveals credential use;
- an initially legitimate disclosure does not create perpetual permission for later retention, transfer, profiling, or secondary use;
- an issuer or operator can be authoritative for issuance or operation without thereby establishing that its metadata choices preserve unlinkability;
- individually minimal disclosures can become identifying or sensitive when composed;
- evidence retained for verification, assurance, or audit can itself become a surveillance or correlation surface when retention is unnecessary or unbounded.

## Compatibility

The machine-readable failure-case contract remains **schema v0.1.0**.

No new domain, failure-class, disposition, or evidence-category enum was required. The tranche uses the existing `privacy`, `credential`, `composition`, `evidence`, `lifecycle`, and `governance` domains together with the existing `correlation`, `policy-mismatch`, and `provenance` failure classes.

This is useful evidence that the current core contract can represent materially different privacy failures without importing VC-specific threat labels into the taxonomy.

Repository release version, schema version, and individual case versions remain independent lifecycle dimensions.

## Assurance and falsification

All thirty-seven cases remain `draft`.

Every new v0.4 case:

- prohibits PASS for the represented unsafe proposition;
- permits DENY and/or INDETERMINATE according to available evidence and consuming policy;
- states explicit evidence requirements;
- states falsification conditions suitable for negative, regression, contract, interoperability, or privacy-assurance testing.

The dedicated privacy/correlation regression suite additionally establishes that:

- proof-mechanism privacy cannot be inferred from payload minimization;
- status-query observability is distinct from status-response disclosure;
- successful presentation is not a blanket secondary-use authorization;
- authoritative operation does not imply privacy preservation;
- minimization must be evaluated at the composition level;
- assurance/audit value is not a blanket justification for retaining raw linkable verification artefacts.

## Provenance and authority boundary

The tranche was pressure-tested against the W3C **Verifiable Credentials Data Model Threat Model v2.1**.

That document is retained as research provenance for relevant cases. At the time of this release it is a draft/work in progress, and DTFC does not treat it as normative authority for corpus classifications.

The resulting cases are intentionally technology-neutral. They can be bound to VC systems, other credential systems, trust registries, assurance workflows, agent systems, or composed trust infrastructures where the same failure proposition applies.

## Cross-repository relationship

RAHP independently carries reusable risk mechanisms and assurance/control patterns for several of these privacy concerns. DTFC remains the technology-neutral corpus of falsifiable failure propositions.

References between the projects preserve traceability; they do not transfer authority or require an adopter to use RAHP.

## Reproduce validation

```bash
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python tools/validate.py
```

A green result establishes repository/schema invariants and the committed regression propositions. It does not establish normative correctness, severity, universal applicability, implementation certification, or ecosystem-wide privacy assurance.

## Release boundary

v0.4.0 is a reproducible privacy/correlation corpus expansion. It does not turn DTFC into a generic privacy threat catalogue, prescribe a credential technology, or claim that the six cases exhaust credential-system privacy failures.
