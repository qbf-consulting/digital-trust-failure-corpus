# Deployment manifestation pilot

Research revision 0.1.0 | Evaluation and retrieval: 2026-11-24 | Author-side research, independent review pending | Issue #134

## Decision

Retain as research. Three public-source candidates establish different observation and attribution boundaries, but none establishes every precondition and falsification condition of its selected canonical case. Do not adopt a machine-readable DMR contract yet: the recurring analytical questions justify this human-readable method, but no demonstrated mapping or machine consumer requirement yet justifies a permanent format. No coverage, maturity, conformance, severity or external adoption claim follows. No release is proposed.

## Baseline and reuse

Baseline main commit [2ccd8cd](https://github.com/qbf-consulting/digital-trust-failure-corpus/tree/2ccd8cd2b2c445a3926dd8326df6f25e1b1e09e9). The canonical failure-case schema v0.1.0, 37 draft cases, taxonomy, authoring, consuming and maturity guidance govern case interpretation. The canonical preconditions, evidence requirements, disposition and falsification rules are not replaced here. Existing external-source registers (#50/#54) map source semantics; observability vectors (#105/#107) are synthetic; #45/#48 govern independent execution/consumer evidence; CPC-001 (#111/#118/#126) is a bounded assurance study; #132 concerns Trust Tasks applicability. None is a substitute for evidence of an observed consequential transaction. Reuse the existing case identifiers and provenance conventions, not their execution contracts or coverage metrics.

## Method

A record identifies a bounded observation, the transaction and actors, the governing policy and trust boundary, and distinct occurrence, observation, publication and evaluation times (unknown is explicit). It links a canonical case ID, version and immutable repository revision. An observed outcome is not a causal explanation. Evaluate every material precondition, trigger and falsification condition against source evidence; record alternatives and missing evidence. Record effects as observed/reported by a named source or inferred, never interchangeably.

Relationship vocabulary (research only):

- demonstrates: evidence establishes material preconditions, decision boundary, mechanism and unsafe behavior; an unexplained outcome alone is insufficient.
- consistent-with: compatible observation or mechanism, but at least one material requirement remains unestablished.
- contradicts: identify the exact claim, assumption or interpretation and evidence that challenges it; not a blanket negative case result.
- illustrates: synthetic or hypothetical only, never an observed deployment.

Evidence classes distinguish public observation (including adjudication, audit and maintainer documentation, with their different scopes), independently reproduced result, author-executed synthetic result and hypothetical illustration. No independent reproduction or synthetic execution is claimed in this pilot. No numeric confidence or PASS is inferred from a relationship. Records below are screened research candidates, not admitted demonstrations.

## Candidate register

| ID / revision | Case / version | Source identifier | Evidence class | Relationship |
|---|---|---|---|---|
| DMR-P01 / 0.1.0 | DTF-013 / 0.1.0 | 2024 BCCRT 149 | Public adjudicated observation | consistent-with (weak, adjacent) |
| DMR-P02 / 0.1.0 | DTF-023 / 0.1.0 | ECA Special Report 01/2023 | Public audit observation | consistent-with |
| DMR-P03 / 0.1.0 | DTF-033 / 0.1.0 | Chromium Security FAQ, certificate revocation | Public implementation documentation | consistent-with (mechanism only) |

All case references pin the baseline revision above. All candidates have author-side research status; none has independent review. Retrieval/evaluation date is 2026-11-24. Source identifiers are documentary pins, not cryptographic attestations. No confidential transcripts, personal details or live credentials are retained. Only factual paraphrase and links are used; third-party rights remain with their holders, and DTFC's license does not relicense linked sources.

## DMR-P01: institutional representation and participant reliance

Canonical [DTF-013](https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/2ccd8cd2b2c445a3926dd8326df6f25e1b1e09e9/corpus/authority/DTF-013.json). Source: [2024 BCCRT 149](https://www.canlii.org/en/bc/bccrt/doc/2024/2024bccrt149/2024bccrt149.html), issued 2024-02-14; primary host returned 403, [decision reproduction inspected](https://longangz.com/ai/case-documents/canada-moffatt-air-canada/source-1.pdf), paragraphs 14–18, 22, 24–32, 44. Reproduction authenticity not separately verified. Occurrence November 2022; contemporaneous participant screenshot described in decision; exact capture time unknown. Adjudication is retrospective, not runtime instrumentation.

Actors: airline, automated website information channel, participant, adjudicator. Boundary: participant's reliance on institutional fare information when buying travel. The adjudicator found misleading advice and reasonable reliance; damages of CAD 650.88 were awarded. The order is evidenced, payment is not. The governing fare policy was inconsistent with the automated message; the adjudicator's legal responsibility finding is not evidence of a technical delegation.

Case assessment: authenticated actor/valid signature not established; material commitment presented for reliance not established (advice is not necessarily a commitment); action-specific principal mandate not evidenced, but absence of proof is not proof of absence. Trigger (acceptance because identity/signature verified) and falsification not established. Technical evidence of authentication, exact action binding, mandate and relying policy is missing. Alternative explanations: incorrect content, inconsistent policy publication or negligent representation rather than mandate substitution. Observed consequence: adjudicated economic injury and remedy. Inferred consequence: institutional reliance risk in automated channels. Do not classify as a demonstrated DTF-013 failure or assume the chatbot architecture. A competing reviewer could reject even the weak consistent-with link on the advice/commitment distinction; retain that challenge.

## DMR-P02: national issuance and cross-system assurance

Canonical [DTF-023](https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/2ccd8cd2b2c445a3926dd8326df6f25e1b1e09e9/corpus/composition/DTF-023.json). Source: [ECA Special Report 01/2023](https://op.europa.eu/webpub/eca/special-reports/free-movement-01-2023/en/), paragraphs 43–56, 81, 84; adopted 2022-11-22; published January 2023. Context: gateway in operation from June 2021; exact incident and observation times not published. Policy context: [Regulation (EU) 2021/953](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32021R0953), historical, not a current travel requirement.

Actors: national issuing systems, Commission gateway, national verifiers and competent authorities. Boundary: local security and issuance evidence relied on across jurisdictions. The audit describes favorable central gateway security assessments alongside limitations on verification of national compliance. It reports a national issuance incident involving a small number of unlawful certificates and resolution of the underlying issue. It does not identify a specific successful cross-border reliance on an affected certificate. The audit expressly acknowledged limits to assurance; it did not itself claim unconditional composition validity.

Case assessment: independent local validation of every component not established; additional seam obligation (national issuance integrity and cross-border governance) supported; national compliance verification limitations supported. Trigger (deriving composed PASS solely from local PASS) and falsification not established. Missing local test outputs, verifier policy, affected transaction and composed decision trace. Alternative explanations for unlawful issuance include local access control failure or misuse by a privileged operator; neither entails composition PASS. Observed consequence: reported unlawful issuance and remediation; no observed travel harm established. Inferred consequence: potential cross-border acceptance or restrictions following loss of confidence. Positive counterevidence: report found the certificate scheme effective in facilitating travel overall. Keep that finding separate from the assurance limitation.

## DMR-P03: status lookup observability

Canonical [DTF-033](https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/2ccd8cd2b2c445a3926dd8326df6f25e1b1e09e9/corpus/privacy/DTF-033.json). Source: [Chromium Security FAQ](https://chromium.googlesource.com/chromium/src/%2B/HEAD/docs/security/faq.md), section on certificate revocation, inspected 2026-11-24. [Versioned historical comparator 66.0.3359.138](https://chromium.googlesource.com/chromium/src.git/%2B/66.0.3359.138/docs/security/faq.md) surfaced in indexed search; full comparator not independently retrieved. Current FAQ mutable; exact immutable revision not verified, publication date unknown. This is a provenance limitation preventing promotion. The FAQ dates removal of Extended Validation online checks to 2022; individual request/observation times unknown.

Actors: browser, certificate issuer/status responder, website and user. Boundary: certificate status request discloses context to a third party beyond the local connection validation. Maintainer documentation identifies browsing-history disclosure as a reason to avoid online checks, alongside availability and security trade-offs. This is an inspectable mechanism claim, not a captured presentation event.

Case assessment: observable status request supported as a mechanism; privacy objective supported by documented design rationale; actual minimal/correct response in a particular interaction not evidenced. Trigger's correlation possibility supported, but an actual cross-context observation and a contemporaneous privacy assurance PASS are not established. Missing request timing, observer identity, join evidence and relying privacy determination. Alternative explanations for browsing correlation include ordinary service logs, network metadata and identifiers unrelated to status resolution. Observed/reported consequence: maintainer reports changed browser checking behavior in 2022. Inferred consequence: potential disclosure of browsing relationships; no individual harm claimed. This does not assert that current Chrome defaults exhibit the failure.

## Cross-case findings

A common pattern is a locally plausible result being relied on beyond its justified scope: institutional advice, a component security assessment or a certificate status result. This is an analytical hypothesis, not evidence of one shared canonical mechanism. A single mechanism could manifest as denial of a refund, acceptance of an unauthorized certificate, or other downstream effects only if transaction-specific evidence links them; the pilot does not demonstrate one mechanism causing multiple observed manifestations. Similar reliance outcomes could arise through content errors, missing authority, local access control or seam-policy failure. Privacy disclosure can arise from status resolution or unrelated network observability. Outcome labels alone cannot discriminate those mechanisms.

The three candidates establish a recurring need for explicit provenance, time, boundary and alternatives. They do not establish demand for automated ingestion or a stable machine contract. The explanatory gap is missing transaction-level causal evidence, not missing canonical propositions. Retain this document as the candidate register and pilot findings; do not generate individual machine records or additional schemas until a later evidence-backed decision warrants it.

## Reviewer and consumer path

1. Select and open the pinned canonical case; compare its full preconditions, trigger, evidence and falsification, not just title.
2. Open the cited source and locator; check publisher competence, version/date, retrieval and rights. If unavailable, stale for the claimed decision, or contradictory, record the limitation and do not upgrade the relationship.
3. Reconstruct only the supported actor, event, policy and decision boundary. Distinguish source observation from inference and actual consequences from possible consequences.
4. Challenge each missing precondition and competing mechanism. For example, P01 has an observed misleading representation and adjudicated reliance; mandate substitution is an inference, not a demonstrated mechanism. A demonstration would require evidence of exact-action authority, verified identity/signature and acceptance on that basis despite an unestablished mandate. Do not fabricate that evidence.
5. Validate canonical references using the existing repository commands: install requirements-dev.txt, run python -m unittest discover -s tests -v and python tools/validate.py. These commands validate the corpus, not this prose's causal judgments.
6. Record a challenge on #134 or a linked issue with candidate ID/revision, exact case clause, source locator, competing interpretation, and proposed relationship. Independent review must identify reviewer, date and evidence actually checked. A reviewer can downgrade or reject a candidate without changing a canonical case.

## Adversarial review and closure boundary

An unexplained adverse outcome cannot be a demonstration (P01); a favorable local assessment does not establish global assurance (P02); documented exposure potential is not an observed privacy breach (P03). A missing source or timestamp cannot become verified evidence, and a hypothetical example cannot be relabeled as independent evidence. These are manual review controls in this research-only decision, not claims of machine-enforced DMR invariants. Conditional schema/validator/negative-test work is not applicable because no contract is adopted. Existing corpus validation and PR review remain required. No canonical changes, no independent execution or review claims, no publication release. Proposed closure decision: retain as research, subject to repository validation and review.
