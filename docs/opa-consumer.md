# Independent engine experiment: OPA

Candidate tracked in #48. The engine is maintained by the Open Policy Agent project; the example Rego policies and JSON fixtures remain DTFC-maintained. This demonstrates an **external engine integration**, not independent community adoption, external authority-state verification, or certification.

Install a pinned official OPA CLI binary using its upstream release instructions. Record the release version and SHA-256 digest of the executable. From the repository root:

```sh
python tools/run_opa_consumer.py --opa /path/to/opa --policy examples/opa-consumer/safe.rego --input examples/independent-consumer/stale-authority.json
python tools/run_opa_consumer.py --opa /path/to/opa --policy examples/opa-consumer/defective.rego --input examples/independent-consumer/stale-authority.json
```

The safe policy should return DENY for revoked authority. The deliberately defective policy ignores authority state and returns PASS on the **same input**. The second command intentionally exits nonzero when it observes PASS. An unavailable binary, malformed output, non-boolean decision, or subprocess failure must be treated as an execution failure, not a satisfied DTFC verdict.

The tool records the OPA version, executable digest, policy digest, input digest, raw JSON result and output digest, timestamp, and observed disposition. This is a provisional adapter experiment: the output has not been cryptographically attested by OPA or an external operator. The policies do not validate revocation evidence or the authenticity of the input authority state. Do not report an external adoption claim based on this experiment.
