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
