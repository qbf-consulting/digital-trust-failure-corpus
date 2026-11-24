# Digital Trust Failure Corpus

A machine-readable corpus of failure conditions, adversarial configurations, invalid trust propositions, and expected safe outcomes for digital trust systems.

The project provides reusable failure cases, evidence requirements, and falsification criteria for conformance, assurance, interoperability, governance, and resilient trust infrastructure.

## Status

Current published repository release: **v0.5.0 (experimental)**. See [`VERSION`](VERSION), [`CHANGELOG.md`](CHANGELOG.md), and the [`v0.5.0 release notes`](docs/release-notes-v0.5.0.md).

v0.5.0 retains the v0.1.0 failure-case schema and contains thirty-seven draft cases, adding the privacy/correlation tranche to the previously released cross-specification seam and decision-resolution work. Repository release version, schema version, and case version are distinct lifecycle dimensions.

The corpus is **evidence, not authority**. A case can cite normative specifications, governance frameworks, implementations, papers, or incidents, but inclusion here does not make the case itself normative.

## Documentation site

The rendered documentation and generated corpus catalogue are published through GitHub Pages:

**https://qbf-consulting.github.io/digital-trust-failure-corpus/**

The Pages site is a presentation layer over this repository. Individual case pages are generated directly from the canonical JSON under `corpus/` during the documentation build; the rendered site does not become a second source of truth.

## Representative Trust Tasks applicability research

The current research deliverable is a [source-pinned Consent family assessment](docs/trust-tasks-representative-consent-study.md), covering eight consent versions against the 37 existing DTF failure propositions. It is author-side, non-normative research with falsifiable consumer-boundary hypotheses, not a certification or observed implementation audit. The full registry census is maintained as a reproducible source index, **not as a commitment to exhaustively assess all 1,391 pinned versions**. The [generated version navigator](https://qbf-consulting.github.io/digital-trust-failure-corpus/trust-tasks/) is published through GitHub Pages; the [tracked landing file](docs/trust-tasks/index.md) explains the distinction.

## Core design principles

- Failure propositions should be falsifiable.
- Missing, stale, conflicting, or unverifiable evidence must not silently become success.
- The core model remains independent of any single DID method, credential format, registry protocol, assurance methodology, or agent architecture.
- Consumers may have legitimate policy differences; a case can therefore permit more than one safe disposition.
- Taxonomy and schema evolution should be driven by concrete cases rather than speculative completeness.

## Repository structure

```text
schemas/                     Versioned machine-readable case contract
corpus/authority/            DTF-001–003, DTF-013–019, DTF-028
corpus/lifecycle/            DTF-004–006 and DTF-031
corpus/composition/          DTF-007–009 and DTF-020–024
corpus/evidence/             DTF-010–012, DTF-025–027, DTF-029–030
corpus/privacy/              DTF-032–037
docs/taxonomy.md             Classification vocabulary
docs/authoring-cases.md      Case authoring guidance
docs/consuming-the-corpus.md Adopter guidance
docs/*-observations.md       Non-normative downstream research signals
tests/                       Schema, validator, corpus, and baseline invariants
tools/validate.py            Repository and adopter validation CLI
licensing/                   Machine-readable artifact licensing policy
```

## Corpus coverage (37 draft cases)

| Range | Focus | Representative failures |
|---|---|---|
| DTF-001–003 | Authority | stale authority, scope escalation, dependent delegation after authority loss |
| DTF-013–019 | Authority at commitment | signature/authority substitution, expiry, revocation, iterative scope exceedance, approval binding, historical reconstruction |
| DTF-004–006 | Lifecycle | revocation, supersession, current vs historical validity |
| DTF-007–009 | Composition | false independence, authoritative conflict, undeclared transitivity |
| DTF-010–012 | Evidence | missing evidence, unresolved freshness, policy/version mismatch |
| DTF-020–027 | Cross-specification seams | semantic ownership, lifecycle stage reuse, composition validity, quorum independence, provenance/evidence sufficiency, workflow/assurance substitution |
| DTF-028–031 | Decision resolution | authority laundering, causal-basis misattribution, silent resolution, false persistence |
| DTF-032–037 | Privacy and correlation | proof-metadata correlation, status-query observability, purpose overrun, issuer-side unlinkability failure, aggregation, retention concentration |

Derived research signals and tranche judgments are recorded separately in `docs/*-observations.md`, including [`docs/privacy-correlation-tranche-observations.md`](docs/privacy-correlation-tranche-observations.md), so they do not expand the core schema by accident.

## Validate the contract and corpus

```bash
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python tools/validate.py
```

The tests and validator establish structural conformance, collection-level identity uniqueness, baseline case continuity, and rejection of important unsafe forms. A green result does not establish normative correctness, case completeness, severity, applicability, or implementation assurance.

## Experimental execution bindings

A separate, fixture-only consumption experiment is documented in [Executable consumption](docs/executable-consumption.md). It defines separate binding/result contracts and a reference evaluator with positive and negative regression tests for DTF-001, DTF-023 and DTF-027. Synthetic observations are not external implementation evidence or assurance certification. The canonical 37-case corpus and v0.1.0 case schema remain unchanged.

A separate-process [authority consumer experiment](docs/independent-consumer.md) invokes a standalone target and records response/source digests. It is a reproducible local integration demonstration, **not** proof of independent third-party adoption.

The [paired conformance vectors](docs/conformance-vectors.md) now execute **three of 37** cases (DTF-001, DTF-023, DTF-027) against DTFC-authored safe and deliberately defective subprocess targets. Experimental vector contract v0.2.0 pins Git blob IDs before execution and records observed outputs and source/response digests. This is **synthetic local execution only**: zero independently maintained targets and zero independently operated consumers have been evidenced. The [older DTF-001 standalone demonstration](docs/executed-target-pair.md) remains reproducible using `python -m tools.execute_target_pair --role paired`; it is part of the same synthetic coverage, not an additional case. The portable v0.2 fixture experiment remains fixture-only and is not additive. See the [evidence-gated execution plan](docs/evidence-gated-execution-tranche.md) for independent evidence gates.

## External source research and mappings

A [deployment manifestation pilot](docs/deployment-manifestation-pilot.md) examines three public-source observations against canonical cases, preserves competing causal explanations and separates consequences from assurance. The decision is to retain this as research rather than adopt a new machine contract; no demonstrated case or independent execution is claimed.

A [bounded external corpus crosswalk](docs/external-corpus-crosswalk.md) and its [machine-readable research register](research/external-sources/crosswalk.json) examine CWE, MITRE ATLAS, the W3C VC 2.0 test suite, and AVID. These non-normative research sidecars distinguish cross-references, test patterns, and unconfirmed coverage gaps. The DTF-001 case carries an informative CWE-863 mapping. No external records were imported, and the canonical schema and 37-case baseline are unchanged.

A [tool-output instruction/data boundary review](docs/tool-output-boundary-research.md) examines MITRE ATLAS indirect prompt injection and OWASP agentic scenarios against existing DTFC authority cases, with a [hypothetical paired scenario](research/tool-output-boundary/scenario.json). It concludes that the core authorization failure is already represented by DTF-028/002/018; the fixture is **not** an executed agent test.


The [experimental case maturity and release gates](docs/case-maturity-and-release-gates.md) distinguish draft cases from independently reviewed, evidenced, and externally exercised cases. A [bounded eight-record CWE triage](https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/main/research/external-sources/record-triage.json) is available as preliminary research, **not** a complete external-corpus overlap audit.

A [three-source, 37-case semantic screening](docs/external-semantic-screening.md) includes an initial 111 judgments and was expanded to 296 judgments across eight inspected source records and 37 cases, with explicit evidence limits. It is research, not an executed conformance or independent adoption test.

The [eight directly inspected external records](docs/inspected-external-records.md) include case-specific W3C T4/DTF-032 and T18/DTF-035 provenance bindings; these are informative research mappings, not evidence of third-party adoption.

The [historical Trust Tasks registry checkpoint](docs/trust-tasks-research-checkpoint.md) preserves the earlier 1,391-version pinned census, preliminary screening records and generated version navigator. The earlier exhaustive research objective was explicitly superseded; [issue #135](https://github.com/qbf-consulting/digital-trust-failure-corpus/issues/135) closed with the representative Consent-family study, not with a claim of registry-wide semantic coverage. The **current report, experimental design and contribution guidance** are in the [representative Consent study](docs/trust-tasks-representative-consent-study.md).

## Authoring and adoption

Contributors should start with [`CONTRIBUTING.md`](CONTRIBUTING.md), [`docs/authoring-cases.md`](docs/authoring-cases.md), and [`docs/taxonomy.md`](docs/taxonomy.md). Adopters should read [`docs/consuming-the-corpus.md`](docs/consuming-the-corpus.md) before binding cases to an implementation or assurance process.

The unchanged v0.1 case schema is at [`schemas/failure-case.schema.json`](schemas/failure-case.schema.json); the v0.5.0 release continues to use that same contract.

## Licensing

This repository uses a dual-license model based on artifact type:

- Human-readable documentation, taxonomy prose, governance and contribution prose, diagrams, narrative examples, and release notes are licensed under **Creative Commons Attribution 4.0 International (CC-BY-4.0)**. See [`LICENSE-CONTENT`](LICENSE-CONTENT).
- Source code, validators, tests, machine-readable schemas, fixtures, corpus entries, executable configuration, and generated machine-readable evidence are licensed under **Apache License 2.0 (Apache-2.0)**. See [`LICENSE-CODE`](LICENSE-CODE).

The repository-level mapping is summarized in [`LICENSE`](LICENSE) and published in machine-readable form at [`licensing/artifact-license-policy.json`](licensing/artifact-license-policy.json). An explicit file-level license notice takes precedence if one is present.

## Security

Security-sensitive implementation findings should follow [`SECURITY.md`](SECURITY.md), not be disclosed through public corpus cases or issues. The public corpus is not an incident repository.

## Project ownership

Digital Trust Failure Corpus is an open QBF Consulting project intended to be consumable by independent standards, assurance, governance, interoperability, and implementation communities without requiring adoption of QBF-specific semantics.


## Authority-at-commitment failure tranche

Cases `DTF-013`–`DTF-019` cover signature/authority substitution, expired and revoked mandates, iterative scope expansion, stale or mismatched approvals, reputation/capability substitution, and unreconstructable historical commitment authority. They reuse the existing failure-case contract; no schema expansion was required.

## Historical Trust Tasks research milestones (archived context)

The initial [12-task pilot](docs/trust-tasks-crosswalk.md) and [pinned registry inventory](docs/trust-tasks-inventory.md) established bounded screening and the complete upstream source census. Early counts in those documents represent **their dated research stages**, not the current assessment scope or a commitment to evaluate every registry entry. The active reader-facing deliverable is the [eight-version Consent case study](docs/trust-tasks-representative-consent-study.md); the earlier issue #135 was closed under that revised contract.

