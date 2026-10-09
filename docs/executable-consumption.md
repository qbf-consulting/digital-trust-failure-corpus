# Experimental executable consumption (v0.1)

This additive demonstration addresses #21 and #43. The canonical corpus remains under `corpus/`; no core case schema changes are needed.

## Execution

`python -m unittest tests.test_execution_binding -v` (from the repository root), followed by `python -m unittest discover -s tests -v`. The CLI accepts a JSON binding file: `python tools/execute_binding.py path/to/binding.json`. The tests generate fixtures directly from the canonical case records.

A binding names a canonical case ID/version and source revision, identifies an adapter, and records an illustrative observed target disposition. The reference `fixture-v1` adapter **does not invoke a real system**: it demonstrates portable evaluation and evidence-record shape only. A real consumer must replace the fixture adapter with an authenticated target invocation and verifiable evidence collection. The declared `case_revision` must match the exact Git HEAD of the checked-out corpus. This establishes which repository snapshot was evaluated, but does not authenticate target-system observations or establish evidence provenance.

The test verdict SATISFIED means the observed disposition is permitted for this failure case. VIOLATED means it is prohibited. This is not the same as the target's PASS decision. A successful schema validation or synthetic SATISFIED verdict does not prove implementation conformance, underlying evidence truth, normative correctness, or independent external adoption.

## Evidence boundary

The fixture adapter requires nonempty evidence references but does not resolve or authenticate them. Future adapters must validate provenance, freshness, applicability, target identity, and collection integrity. An unverified evidence reference must not be promoted to assurance PASS.

## Next consumer experiment

Bind the same cases to a genuinely external implementation. Capture target version, input fixtures, observed decision, evidence digests, collection timestamp and replay instructions. Compare results across two independent runs. Record any schema pressure before extending the core contract.

No confidential assessment or incident materials belong in this public repository.

## Portable fixture binding v0.2 (additive)

The new `schemas/execution-binding-v0.2.schema.json` and `schemas/execution-result-v0.2.schema.json` are **opt-in**, preserving the existing v0.1 `case_revision`/Git HEAD contract. The portable v0.2 binding uses `case_sha256` computed over UTF-8 JSON with sorted keys, compact separators, Unicode preserved and NaN prohibited. This is **DTFC normalization, not RFC 8785 JSON Canonicalization Scheme**. Whitespace and object key ordering do not change the digest; changes to values and array order do. A consumer must supply the canonical case JSON in its local corpus directory.

Reproduce from a checkout or vendored archive without Git metadata:

```bash
python -m unittest tests.test_portable_binding -v
python tools/execute_portable_binding.py my-binding-v0.2.json --corpus-root ./corpus
```

Example binding structure:

```json
{
  "binding_version": "0.2.0",
  "case_id": "DTF-001",
  "case_version": "0.1.0",
  "case_sha256": "<64-character SHA-256 of canonical case JSON>",
  "adapter": "fixture-v1",
  "scenario": "synthetic revoked authority",
  "expected": "DENY",
  "observed": "PASS",
  "evidence": ["synthetic:unverified"]
}
```

The example digest is intentionally a placeholder and must be computed from the exact canonical case using `tools.case_digest.case_sha256`; check the actual case version and permitted expected disposition before use. The runner rejects missing, duplicated, mismatched-version or changed cases. A `SATISFIED` result only means that **author-supplied** `observed` data agrees with the case's disposition rule. The result explicitly states `execution_class: author-supplied-fixture`. This is **not an executed target test**, verified evidence, independent adoption or conformance.

Current illustrative paired coverage: **3/37 cases** (DTF-001, DTF-023, DTF-027), all fixture-only in this runner. Independently executed target coverage from this new v0.2 runner: **0/37**. The separate pinned OPA demonstration executes a synthetic safe/defective policy pair for DTF-001 and must be reported separately; it does not change fixture-only coverage. See #63 for the next actual target-adapter and conformance-report increment.
