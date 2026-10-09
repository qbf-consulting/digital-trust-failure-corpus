# Release publication and authorization

## Current state

**v0.4.0 is an already published historical release.** The existing `release/publish-request.json` records its provenance, not an instruction to republish it. A later maturity review concluded that the research then available did not justify *another* release; this does not invalidate the historical v0.4.0 tag.

**Prospective publication is manual-only and fail-closed.** Changing `release/publish-request.json` no longer triggers publication. A maintainer must explicitly dispatch `publish release` from `main`. The job references the GitHub environment `release-publication`, which **must be configured outside the repository** before use.

## Required one-time GitHub configuration

A repository administrator must configure **Settings → Environments → release-publication**:

1. Enable **required reviewers** with an authorized human approver, preferably separate from the dispatcher where team policy permits. Do not enable bypass by administrators for normal publication.
2. Restrict deployments to the protected `main` branch.
3. Only after verifying both settings, define environment-scoped variable `RELEASE_APPROVAL_CONFIGURED=true`. Do not set this at repository or organization scope. Without the variable, publication fails closed.
4. Maintain an active branch ruleset requiring a PR and validation checks. Current ruleset `protect-main` requires PRs and `validate` but **zero approving reviews**; strengthening review requirements for release-critical changes requires an administrator. CODEOWNERS alone is not approval enforcement.
5. Re-verify environment reviewers, branch restrictions and actor permissions before the first publication. These settings are **not asserted as configured by this PR**.

The release workflow permits dispatch by GitHub actor `sankarshanmukhopadhyay` only. The `requested_by` field is audit metadata, **not authentication**. The GitHub event actor, environment reviewer gate and branch ruleset supply separate controls. The job's write permission is scoped to release publication.

## Publication sequence

1. Prepare a normal PR changing `VERSION`, changelog, release notes, relevant baselines and `release/publish-request.json`. Record the release rationale and resolve review findings.
2. Merge after the required repository checks and any human review required by the configured ruleset.
3. Explicitly dispatch **Actions → publish release → Run workflow** from `main`. The protected `release-publication` environment must approve the job.
4. The preflight checks manual event, `main`, authorized dispatching actor, approval-configuration attestation, matching `VERSION` and nonempty rationale.
5. The workflow reruns tests and corpus validation on its checked-out commit, requires matching release notes, rejects existing tags/releases, publishes against `GITHUB_SHA`, marks **Latest** and verifies title and latest status.

The workflow's own tests execute against the checkout SHA, but **do not consume a separately attested, SHA-specific validation workflow result**. This remains a follow-up assurance requirement under issue #62. Never describe a green test alone as independent human authorization.

## Recovery and failure boundaries

There is no push-triggered or reviewer-free emergency publication bypass. For recovery, repair the environment/reviewer configuration and rerun an explicitly approved dispatch. An existing tag or GitHub Release is never overwritten by the workflow. If the protected environment is not configured, the publication job must not be run.

Release flower codenames are presentation metadata selected from a repository snapshot; the immutable version tag is the machine-readable release identity.
