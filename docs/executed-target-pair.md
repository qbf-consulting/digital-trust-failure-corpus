# Executed synthetic target pair (DTF-001)

This example invokes two **actual Python subprocess targets** for the same revoked-authority request. The safe target returns DENY; the deliberately defective target returns PASS. The latter is a **VIOLATED** failure-prevention test, not a harness success.

From the repository root:

```bash
python -m tools.execute_target_pair --role paired
python -m unittest tests.test_target_pair
```

The JSON report includes the canonical case digest, target source SHA-256, request and raw response SHA-256, the target disposition, and replay command. The runner fails closed on unknown adapters, nonzero target exits, malformed JSON and unknown dispositions. The test verifies matching paired request hashes.

**Coverage:** 1/37 cases with an executed synthetic target pair; 0/37 cases with an independently maintained target through this runner; 0/37 cases with independent DTFC consumer evidence. Existing fixture-only paired coverage is separately 3/37 and must not be added to executed coverage. This is a bounded DTF-001 example, not a generic adapter protocol, independent adoption, or a conformance certification. #63, #48 and #45 remain open.

For safety, this runner exposes only a fixed allowlist of repository-local example scripts, not arbitrary shell commands. It does not collect external secrets or call external networks.
