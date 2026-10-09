# Independent engine experiment: OPA

Candidate tracked in #48. The engine is maintained by the Open Policy Agent project; the example Rego policies and JSON fixtures remain DTFC-maintained. This demonstrates an **external engine integration**, not independent community adoption, external authority-state verification, or certification.

CI installs the official OPA v1.9.0 Linux amd64 static executable and **verifies** its SHA-256 digest (`66fa66f3b730b2fb086003863428b382b2898d343adb4b5dfab5598b4d739eed`) before executing the integration test. The paired safe/defective policy run passed in GitHub Actions validation run 37949364290. For local reproduction, obtain the same binary from the upstream release, verify its SHA-256 digest, and use its absolute path below. Other platforms require their own verified release artifact. This digest is a local binary-integrity check, not independent evidence attestation. From the repository root:

```sh
python tools/run_opa_consumer.py --opa /path/to/opa --policy examples/opa-consumer/safe.rego --input examples/independent-consumer/stale-authority.json
python tools/run_opa_consumer.py --opa /path/to/opa --policy examples/opa-consumer/defective.rego --input examples/independent-consumer/stale-authority.json
```

The safe policy should return DENY for revoked authority. The deliberately defective policy ignores authority state and returns PASS on the **same input**. The second command intentionally exits nonzero when it observes PASS. An unavailable binary, malformed output, non-boolean decision, or subprocess failure must be treated as an execution failure, not a satisfied DTFC verdict.

The tool records the OPA version, executable digest, policy digest, input digest, raw JSON result and output digest, timestamp, and observed disposition. This is a provisional adapter experiment: the output has not been cryptographically attested by OPA or an external operator. The policies do not validate revocation evidence or the authenticity of the input authority state. Do not report an external adoption claim based on this experiment.
