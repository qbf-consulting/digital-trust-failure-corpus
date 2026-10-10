# Non-publishing release safety preflight

The `.github/workflows/release-safety-preflight.yml` workflow is a **read-only** manual diagnostic. It has `contents: read`, no publication environment, no release API calls and no tag writes. It exercises the existing authorization and input negative tests (wrong actor/event/branch/mode, duplicate tag, missing notes, stale SHA), plus a duplicate-tag rejection probe.

Run via **Actions → release safety preflight (no publication) → Run workflow** on `main`. Preserve the run URL, exact head SHA, logs and summary as audit evidence. This diagnostic is **not** a live test of the protected publication environment: it cannot establish GitHub environment restrictions, who can dispatch the publishing workflow, or that a concurrent tag mutation is impossible.

## Administrative evidence still required

1. Obtain an administrator-visible capture or audit export of the `release-publication` environment showing its `main` branch restriction and `RELEASE_AUTHORIZATION_MODE=single-maintainer` setting (without disclosing secrets).
2. Record the repository ruleset and historical release/tag state. The `protect-main` ruleset requires PRs and strict validation but **zero approving reviews**; independent reviewer authorization is not claimed.
3. Record a green exact-SHA diagnostic run and separately attest the corresponding required validation check. Do not equate a repository-local unit test with external approval.
4. Preserve historical `v0.4.0` and its tag; do not run the publication workflow as part of these checks.

Closure of #62 requires an explicit maintainer disposition of any unavailable administrative evidence and of residual live authorization testing. This document alone does not satisfy those controls.

## Administrator evidence and bounded residual — 2026-10-10

The maintainer supplied a two-page capture of the GitHub `release-publication` environment settings and a separate full-width environment-variable screenshot. The captures visibly establish:

- **Deployment restriction:** selected branches and tags, one allowed branch (`main`), zero allowed tags.
- **Authorization mode:** environment variable `RELEASE_AUTHORIZATION_MODE` has value `single-maintainer`.
- **Approval model:** required reviewers disabled; administrator bypass option unchecked. This is a single-maintainer model and **does not** claim independent approval.

The captures were reviewed in the issue #62 conversation, **not committed to the public repository**. They are administrator-visible snapshots, not a GitHub API attestation, proof of continued settings immutability or a live authorization-enforcement test.

**Residual risk:** No deliberately unauthorized dispatch was run against the actual protected `publish release` workflow. The green read-only diagnostic run [38017265136](https://github.com/qbf-consulting/digital-trust-failure-corpus/actions/runs/38017265136) exercised negative authorization/input probes without acquiring the publication environment or write permission. Consequently it does not demonstrate that GitHub would reject every unauthorized publication attempt. Environment settings could also change after the screenshots.

**Proposed bounded disposition:** Accept the absence of a live unauthorized publishing-dispatch test **for the current single-maintainer experimental development-release process**, subject to maintainer confirmation in #62. Compensating controls are: `main`-only environment, authorized-actor and authorization-mode checks, manual workflow dispatch, exact-checkout preflight, duplicate-tag rejection, immutable Action pins and green non-publishing negative tests. The residual is **not** accepted on behalf of the maintainer merely by merging documentation.

**Before any publication:** the maintainer must explicitly record acceptance or request further live-negative testing in #62; confirm environment settings remain in force; run required checks on the intended exact commit; disposition #60's other outstanding audit risks; and separately authorize release preparation/publication. No release or tag is created by this record.
