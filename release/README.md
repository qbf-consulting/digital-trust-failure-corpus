# Release publication and authorization

## Current state

**v0.4.0 is an already published historical release.** The existing `release/publish-request.json` records its provenance, not an instruction to republish it. A later maturity review concluded that the research then available did not justify *another* release; this does not invalidate the historical v0.4.0 tag.

**Prospective publication is manual-only and fail-closed.** Changing `release/publish-request.json` no longer triggers publication. A maintainer must explicitly dispatch `publish release` from `main`. The job references the GitHub environment `release-publication`, which **must be configured outside the repository** before use.

## Required one-time GitHub configuration

A repository administrator must configure **Settings → Environments → release-publication**:

1. For the explicitly selected **single-maintainer model**, leave **required reviewers disabled**. There is no separation-of-duties claim. Disable administrator bypass where possible; this does not add an independent approver.
2. Restrict deployments to the protected `main` branch.
3. After verifying the `main` restriction, define environment-scoped variable `RELEASE_AUTHORIZATION_MODE=single-maintainer`. Remove the obsolete `RELEASE_APPROVAL_CONFIGURED` variable. Do not set authorization mode at repository or organization scope. Without the exact mode the preflight fails closed.
4. Maintain an active branch ruleset requiring a PR and validation checks. Current ruleset `protect-main` requires PRs and `validate` but **zero approving reviews**; strengthening review requirements for release-critical changes requires an administrator. CODEOWNERS alone is not approval enforcement.
5. Re-verify environment reviewers, branch restrictions and actor permissions before the first publication. These settings are **not asserted as configured by this PR**.

The release workflow permits dispatch by GitHub actor `sankarshanmukhopadhyay` only. The `requested_by` field is audit metadata, **not authentication**. The GitHub event actor, environment branch restriction and branch ruleset supply separate controls, but **no independent approval**. The job's write permission is scoped to release publication.

## Publication sequence

1. Prepare a normal PR changing `VERSION`, changelog, release notes, relevant baselines and `release/publish-request.json`. Record the release rationale and resolve review findings.
2. Merge after the required repository checks and any human review required by the configured ruleset.
3. Explicitly dispatch **Actions → publish release → Run workflow** from `main`. The `release-publication` environment must allow only `main`; no reviewer gate is configured.
4. The preflight checks manual event, `main`, authorized dispatching actor, explicit single-maintainer authorization mode, matching `VERSION` and nonempty rationale.
5. The workflow reruns tests and corpus validation on its checked-out commit, requires matching release notes, rejects existing tags/releases, publishes against `GITHUB_SHA`, marks **Latest** and verifies title and latest status.

The workflow's own tests execute against the checkout SHA, but **do not consume a separately attested, SHA-specific validation workflow result**. This remains a follow-up assurance requirement under issue #62. Never describe a green test alone as independent human authorization.

## Recovery and failure boundaries

There is no push-triggered or reviewer-free emergency publication bypass. For recovery, repair the environment branch restriction and authorization-mode configuration and rerun an explicitly approved dispatch. An existing tag or GitHub Release is never overwritten by the workflow. If the environment is not configured, the publication job must not be run. An environment variable is not evidence that the GitHub administrative branch restriction actually exists.

Release flower codenames are presentation metadata selected from a repository snapshot; the immutable version tag is the machine-readable release identity.

## Governance limitation

This operating model authorizes the named GitHub dispatcher without a second-person review. `requested_by` and `RELEASE_AUTHORIZATION_MODE` are not independent authorization attestations. Required validation is rerun within the publication job, but SHA-specific external CI attestation, independent review and live negative dispatch tests remain unresolved under #62. No new release is authorized merely by merging this change.
