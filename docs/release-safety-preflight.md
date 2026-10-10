# Non-publishing release safety preflight

The `.github/workflows/release-safety-preflight.yml` workflow is a **read-only** manual diagnostic. It has `contents: read`, no publication environment, no release API calls and no tag writes. It exercises the existing authorization and input negative tests (wrong actor/event/branch/mode, duplicate tag, missing notes, stale SHA), plus a duplicate-tag rejection probe.

Run via **Actions → release safety preflight (no publication) → Run workflow** on `main`. Preserve the run URL, exact head SHA, logs and summary as audit evidence. This diagnostic is **not** a live test of the protected publication environment: it cannot establish GitHub environment restrictions, who can dispatch the publishing workflow, or that a concurrent tag mutation is impossible.

## Administrative evidence still required

1. Obtain an administrator-visible capture or audit export of the `release-publication` environment showing its `main` branch restriction and `RELEASE_AUTHORIZATION_MODE=single-maintainer` setting (without disclosing secrets).
2. Record the repository ruleset and historical release/tag state. The `protect-main` ruleset requires PRs and strict validation but **zero approving reviews**; independent reviewer authorization is not claimed.
3. Record a green exact-SHA diagnostic run and separately attest the corresponding required validation check. Do not equate a repository-local unit test with external approval.
4. Preserve historical `v0.4.0` and its tag; do not run the publication workflow as part of these checks.

Closure of #62 requires an explicit maintainer disposition of any unavailable administrative evidence and of residual live authorization testing. This document alone does not satisfy those controls.
