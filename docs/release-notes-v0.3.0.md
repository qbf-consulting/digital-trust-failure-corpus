# Digital Trust Failure Corpus v0.3.0

## Purpose

v0.3.0 expands the corpus from nineteen to thirty-one draft failure cases while retaining the existing failure-case schema v0.1.0.

The release adds two related tranches:

1. **cross-specification seam failures** — cases where locally valid components, evidence, bindings, thresholds, or workflows are incorrectly promoted into broader composition-level trust claims; and
2. **decision-resolution failures** — cases where authority is amplified from non-authoritative signals, decision changes are causally misattributed, unresolved conditions disappear without admissible resolution evidence, or valid resolution evidence fails to clear a prior unresolved state.

The governing release principle is:

> Local validity, operational success, or repeated assertion is not sufficient evidence of a broader authority, composition, or assurance proposition.

## Added cases

### Cross-specification seam tranche

- **DTF-020** — semantic ownership ambiguous at a composition seam.
- **DTF-021** — earlier lifecycle check reused at a later material stage.
- **DTF-022** — context binding mistaken for execution success.
- **DTF-023** — component validity mistaken for composition validity.
- **DTF-024** — quorum count mistaken for independent approval.
- **DTF-025** — provenance depth mistaken for assurance depth.
- **DTF-026** — selective valid evidence mistaken for complete evidence.
- **DTF-027** — workflow success mistaken for assurance success.

### Decision-resolution tranche

- **DTF-028** — authority laundering through non-authoritative signals.
- **DTF-029** — decision transition basis misattributed.
- **DTF-030** — unresolved material condition cleared without resolution evidence.
- **DTF-031** — resolved condition remains blocking after valid resolution.

## Compatibility

The machine-readable failure-case contract remains **schema v0.1.0**.

No new domain, failure-class, disposition, or evidence-category enum was required. This is deliberate evidence that the existing technology-neutral contract can represent the new failures without importing protocol- or assurance-specific semantics.

Repository release version, schema version, and individual case versions remain separate lifecycle dimensions.

## Assurance and falsification

All thirty-one cases remain `draft`.

Every new v0.3 case:

- prohibits PASS for the represented failure condition;
- preserves DENY and/or INDETERMINATE as safe outcomes according to available evidence and consuming policy;
- states explicit evidence requirements;
- includes falsification conditions suitable for negative, regression, contract, or interoperability testing.

The new regression suites additionally establish that:

- component PASS does not imply composition PASS;
- earlier lifecycle state does not silently become later-stage current state;
- valid context binding does not prove successful execution;
- quorum arithmetic does not prove independence;
- longer provenance does not automatically increase assurance;
- validity of disclosed evidence does not prove completeness;
- workflow/validator success does not prove substantive assurance;
- repeated, aggregated, endorsed, projected, or reputational signals do not manufacture authority;
- evidence, policy, lifecycle, correction, and evaluation-context changes remain distinguishable from authority change;
- unresolved material state cannot silently disappear;
- valid current resolution evidence must trigger reassessment rather than permanent blocking.

## Provenance and authority boundary

DTFC records reusable failure propositions. It does not become the normative owner of the semantics defined by external specifications or governance systems.

The decision-resolution tranche preserves read-only research provenance to the independent Protocol of Care for Agents project, including its brief and Simulation 01 runbook. Those references informed the investigation but do not create a normative dependency.

No writes were made to that upstream repository.

## Cross-repository relationship

The release keeps portfolio responsibilities separated:

- TSMM can own canonical trust-system semantics;
- TIS can carry portable evidence contracts;
- DTFC records reusable falsifiable failure propositions;
- ARPA, ARA, and interoperability cases can generate executable pressure evidence;
- RAHP can assess whether evidence demonstrates resistance to relevant risks and harms.

References between these projects preserve traceability; they do not transfer authority.

## Reproduce validation

```bash
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python tools/validate.py
```

A green result establishes repository/schema invariants and the committed regression propositions. It does not establish normative correctness, severity, universal applicability, implementation certification, or ecosystem-wide assurance.

## Release boundary

v0.3.0 is a reproducible corpus expansion, not a normative standard, incident database, threat encyclopedia, severity catalogue, or assurance certification scheme.
