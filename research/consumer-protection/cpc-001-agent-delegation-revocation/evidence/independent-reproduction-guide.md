# CPC-001 independent reproduction guide

Status: **readiness guide, not completed reproduction evidence**.

This guide defines how a reviewer can independently reproduce the CPC-001 synthetic fixture evidence. It does not itself establish that independent reproduction has occurred.

## Purpose

The previous CPC-001 tranches established:

- source contracts and protection requirements;
- a repository-owned synthetic protected-resource fixture;
- a deliberately defective target;
- CI-executed synthetic evidence; and
- an evidence manifest that prevents synthetic CI success from becoming a full assurance claim.

This tranche prepares the next evidence gate: independent reproduction by a reviewer or environment distinct from the original authoring path.

## Minimum reviewer criteria

A reproduction record may be treated as independent only when the record identifies:

1. the reviewer or reproducing environment;
2. the relationship of that reviewer/environment to the original authoring path;
3. the exact source revision checked out;
4. the commands executed;
5. the observed results;
6. retained evidence artifacts or logs; and
7. discrepancies, limitations, or conflicts.

A self-run by the original authoring path may be useful diagnostic evidence, but it is not independent reproduction.

## Required commands

A reviewer should execute, at minimum:

```bash
git clone https://github.com/qbf-consulting/digital-trust-failure-corpus
cd digital-trust-failure-corpus
git checkout <source_revision>
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python tools/validate.py
python tools/execute_cpc001.py --role paired
```

## Required record

The reviewer should complete:

```text
research/consumer-protection/cpc-001-agent-delegation-revocation/evidence/independent-reproduction-record-template.yaml
```

and submit it as a new file or issue attachment with the relevant logs or retained evidence references.

## Interpretation boundary

A completed independent reproduction record may support only this bounded statement:

> The repository-owned CPC-001 synthetic fixture was independently reproduced under the recorded environment and source revision.

It still cannot support claims of:

- production product or service safety;
- consumer usability validation;
- ARPA conformance;
- RAHP assessment;
- non-synthetic implementation evidence; or
- general agent safety.

## Failure handling

If reproduction fails, the result should not be discarded. The record should state whether the failure is due to:

- environment setup;
- dependency resolution;
- repository test failure;
- fixture-output mismatch;
- evidence-manifest inconsistency;
- incomplete instructions; or
- reviewer-determined ambiguity.

A failed reproduction is evidence about the reproducibility boundary and should be retained until resolved or explicitly superseded.
