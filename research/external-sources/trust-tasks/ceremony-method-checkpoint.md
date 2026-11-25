# Ceremony assessment: source and method checkpoint

Issue [#168](https://github.com/qbf-consulting/digital-trust-failure-corpus/issues/168). Author-side research, AI-assisted; not a completed Gate A, not an independent review or an implementation assessment.

## Source authority

Registry revision [f21a98ec8383352d18629a08dd5dd23935456142](https://github.com/trustoverip/dtgwg-trust-tasks-tf/tree/f21a98ec8383352d18629a08dd5dd23935456142), generated SPEC.md blob fa908af0593defe18f651fea50de7a7dae952a1f. Canonical framework [bdf2cdd9256f9d7b98fe8b40c776124fc27a6084, spec/body.md](https://github.com/trustoverip/dtgwg-trust-tasks-spec/blob/bdf2cdd9256f9d7b98fe8b40c776124fc27a6084/spec/body.md), blob f89b80005fa3453f3097acbda08aa9ec44b845c8. Request and response variants distinguish success, error and continuation; continuation leaves work blocked. Ceremony membership is not permission; definition content is outside the framework revision. Use the registry snapshot for task versions, not as authority for the framework.

VTI snapshot [83e88fcf8760f6bd159bbac09a27b002f5b656c2](https://github.com/trustoverip/dtgwg-vti-spec/tree/83e88fcf8760f6bd159bbac09a27b002f5b656c2) is a separately pinned, later draft source; do not assume cross-version compatibility. Directly inspected normative chapters:

- [Membership lifecycle](https://github.com/trustoverip/dtgwg-vti-spec/blob/83e88fcf8760f6bd159bbac09a27b002f5b656c2/spec/12-vtc-lifecycle.md), blob 3d44ac109e196e91c374d38d51680550b9ff03e2: VTI-MEM-001/002 (authorized, audited transitions), 010–013 (admission decision, evidence and presentation), 020–022 (credential evidence), 030–034 (suspension, departure, erasure, publication and separate status timing).
- [Composition](https://github.com/trustoverip/dtgwg-vti-spec/blob/83e88fcf8760f6bd159bbac09a27b002f5b656c2/spec/14-composition.md), blob cd77bbc46fa456bb737b7d49eecd8878b3472d00: VTI-CMP-001/002, 010/011, 020–023, 030–032, 040–042, 050–053, 060–064, 070–074, 080–082, 090–092, 110–113. These are explicit upstream composition requirements, not novel DTFC requirements. The chapter also records unresolved ownership questions (120).
- [Approvals](https://github.com/trustoverip/dtgwg-vti-spec/blob/83e88fcf8760f6bd159bbac09a27b002f5b656c2/spec/03b-approvals.md), blob 3547ef07baaccdd3b46b3c0eab04971eb4bff210: VTI-APV-001–008, 011, 013, 015–017, 019, 022–023. Re-authentication is not another party's consent; pending operations require re-evaluation at execution; recommended second-party consent has expressly bounded alternatives.

## Analytical profiles (provisional, not upstream definitions)

### Joining
Application-based VTC membership under manifest/0.4, submit/0.3 and decide/0.1. Automatic admission and review are alternative paths under the criterion, not cumulative steps. Direct admit/0.1 is a separate contrast with live capability, role bounds, policy referral and re-evaluation; make-membership/0.1 is a bootstrap contrast. Do not infer that manifest rules for applicants outlaw authorized direct admission, or that direct admission establishes subject consent. Credential delivery can be best effort without negating the community's completed admission. Evaluate membership versus access separately. VTI-MEM-011 directly requires separating join exchange completion and admission.

### Separation
Same VTC membership. self-remove/0.1 and self-remove-receipt/0.1 distinguish request and effective departure; admin-remove/0.1 is a distinct authorization path. The self-remove response prose and asynchronous receipt require careful reconciliation against schemas; no assumption that an acceptance acknowledgement constitutes removal. VTI-MEM-032 forbids downgrading subject-initiated erasure; MEM-034 prohibits delaying credential status merely to batch publication for privacy. Historical audit evidence and current status are distinct. Group/network departure are contrast cases only.

### Consent-mediated delivery
Reuse #135's pinned Consent family; distinguish direct operator decision from bridge attestation. Routing, grant and synchronization success do not establish current permission at release. Do not treat a bridge as legal representative. Apply VTI composition requirements only where their preconditions hold; operation approval rules are not automatically identical to message-delivery grants.

## Assessment contract

For each selected profile and canonical DTF case, separately determine local task result, ceremony execution/completion, legitimacy of the intended outcome, and effective state at reliance. A valid refusal can be correct execution without the requested outcome. Unknown is not false and not PASS. Distinguish conditional candidate, not established in profile, and unresolved evidence; distinguish task-local, compositional and cross-ceremony attribution. Compare identical observations, including cases where ceremony context adds no new explanatory value. Cross-ceremony path: VTC admission → membership-derived access → separation → later reliance. Require explicit causal premises and preserve unrelated entitlements.

The existing receipt assessment and Consent study remain unchanged. A receipt does not confer authority. VTI already explicitly states the semantic-completion distinction: research contribution must be operationalizing it through pinned cases, alternative paths and falsification designs, not asserting novelty of the principle.

## Remaining Gate A obligations

Inspect selected payload schemas against inventory blob pins; read full selected Consent and receipt contracts; inspect governing VTC chapter and relevant credential/access requirements; resolve or explicitly bound version/source tensions; freeze actual canonical case blobs; produce validated profiles with task dependencies, completion and legitimacy predicates. The 111-cell assessment and publication remain pending. No independent review, live execution, or conformance claim.
