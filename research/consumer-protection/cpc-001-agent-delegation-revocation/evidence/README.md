# CPC-001 evidence bundle boundary

Status: **synthetic executable evidence boundary**.

This directory documents how CPC-001 evidence is generated, validated, and interpreted. It does not contain independent third-party implementation evidence and does not make a production assurance claim.

## Evidence package contents

| Artifact | Purpose | Status |
| --- | --- | --- |
| `current-determination.yaml` | Claim-by-claim current determination boundary | Present |
| `evidence-manifest.yaml` | Source revisions, CI run identifiers, fixture evidence class and assurance boundary | Present |
| `reproduction-instructions.md` | Commands and interpretation rules for synthetic fixture reproduction | Present |

## Evidence classes

| Evidence class | Source | Current status | Assurance meaning |
| --- | --- | --- | --- |
| `source-contract` | CPC-001 Markdown/YAML artifacts | Present | Describes intended claims and protection contracts |
| `executed-synthetic-target` | `tools/execute_cpc001.py` invoking repository-owned safe/defective targets | Added as executable path | Demonstrates local fixture behaviour and known-defect detection |
| `ci-executed-synthetic-target` | GitHub Actions running repository tests | Present for PR #112 | Confirms repository-owned fixture and guardrail tests executed successfully in CI for the recorded PR head |
| `independent-reproduction` | Separate reviewer/environment replaying the fixture | Not present | Required before claiming independent reproducibility |
| `non-synthetic-implementation` | Externally maintained or product-like enforcement implementation | Not present | Required before claiming product/service implementation evidence |

## Executable command

Run the synthetic CPC-001 fixture locally with:

```bash
python tools/execute_cpc001.py --role paired
```

The command executes both:

- `examples/cpc-001/protected_resource.py` — the expected safe target; and
- `examples/cpc-001/defective_protected_resource.py` — the intentionally defective target.

The paired result is valid only if:

1. the safe target satisfies every mandatory synthetic scenario;
2. the defective target is classified as a violation;
3. the same scenario identifiers are evaluated by both targets;
4. post-revocation, stale-authority, and replay defects are specifically observed; and
5. no result is interpreted as independent adoption evidence.

## Evidence interpretation rule

Synthetic execution can support a statement such as:

> The repository-owned CPC-001 fixture detects the deliberately defective protected-resource target under the included scenarios.

It cannot support statements such as:

- CPC-001 is independently reproduced;
- ARPA is conformant;
- RAHP has assessed the case;
- a production product or service is safe;
- consumers can successfully use the revocation control in practice.

## Persistence rule

Generated evidence should be treated as a build artifact unless it is intentionally versioned as a release evidence bundle. If persisted in the repository, it must be labelled as synthetic and bound to exact source revisions or file digests.

## Stop condition for this evidence tranche

The evidence-package tranche reaches a defensible stop point when the repository contains:

- a manifest identifying PR #112, the merged source revision, the PR head revision and CI run identifiers;
- reproduction instructions for the synthetic fixture;
- tests that prevent CI success from being promoted to full assurance;
- explicit disclosure that independent reproduction, non-synthetic implementation evidence, RAHP assessment and consumer-usability evidence remain absent.
