# Separate-process DTFC consumption experiment

This bounded experiment addresses #45. The example authority decision target is a separate Python CLI that imports no DTFC code. The harness launches it as a subprocess, captures its stdout, exit code, UTC collection time, and SHA-256 digests of target source, request and canonicalized JSON response. It then evaluates the target disposition against DTF-001.

**Important:** This is an independently executable *process*, but the target is maintained within the same repository and is intentionally simplistic. It does not establish third-party implementation adoption, external governance authority, or production assurance.

## Reproduce

From the repository root, install `requirements-dev.txt`, then run `python -m unittest discover -s tests -v`.

To run the example, obtain the DTF-001 `version` from its canonical JSON file and use the exact `git rev-parse HEAD` value as `--case-revision`:

```sh
python -m tools.run_independent_consumer --request examples/independent-consumer/stale-authority.json --case-version 0.1.0 --case-revision "$(git rev-parse HEAD)"
```

The case-version argument must match the actual case version; replace `0.1.0` if necessary. The stale-authority example is expected to yield DENY and a SATISFIED harness verdict. The intentionally defective `defective_authority_target.py` returns PASS for the **same revoked-authority input** and produces a VIOLATED verdict. This paired adverse-condition test avoids the misleading comparison with a legitimately active authority. The harness does not prove the target's real-world authority semantics.

## Trust and evidence boundaries

The `verify_capture` helper recomputes target-source, request and canonicalized response digests; tests demonstrate detection of request and response tampering. These hashes do not provide an independently signed execution attestation. A digest binds recorded bytes to the local run; it does not authenticate the publisher or prove that the target's inputs correspond to real authority state. The example does not verify external evidence or validate the correctness of the target's authority-state oracle. A genuine independent implementation, controlled adverse fixtures, external provenance, and reproducible third-party results remain required before claiming external consumption.

The `fixture-v1` schema remains unchanged; the adapter wraps actual process output into the existing evaluator. The example is deliberately outside the core failure-case schema.
