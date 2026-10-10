# Publishing a release

**Current workflow: explicit, protected manual dispatch only.** The previously published v0.4.0 release remains the historical latest baseline. Editing `release/publish-request.json` does **not** trigger a release.

For complete release authorization, environment setup, failure behaviour and recovery, see [release/README.md](https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/main/release/README.md).

## Before dispatch

Prepare and merge a reviewed PR with `VERSION`, `CHANGELOG.md`, `docs/release-notes-v<version>.md`, case/schema changes as applicable, and a matching `release/publish-request.json` carrying a rationale. Complete a prospective release-readiness assessment; passing CI alone does not confer maturity or independent adoption.

A repository administrator must have configured GitHub environment `release-publication` with required human reviewers and deployment-branch restrictions to `main`, and **only then** its environment-scoped `RELEASE_APPROVAL_CONFIGURED=true` variable. The repository cannot itself enforce or attest the presence of reviewers. Without the attestation variable the preflight rejects publication.

## Publication

1. Open **Actions → publish release → Run workflow** and select `main`.
2. The dispatching GitHub actor must be `sankarshanmukhopadhyay`. A request file's `requested_by` is not identity evidence.
3. Wait for protected-environment approval. The job checks event, branch, actor, configuration attestation, version/rationale, tests, corpus, release notes and existing tags.
4. On success, the workflow publishes `v<version>` against its exact `GITHUB_SHA`, marks the release Latest, and verifies the result.

The protected workflow now also runs `python -m tools.verify_release_inputs` against its exact checkout SHA, the nonempty version-specific notes and remote tags before resolving release metadata. This is an internal preflight, not external CI attestation or proof of configured human reviewers. The workflow will not overwrite an existing tag or release. There is no push-triggered publication path. The workflow re-executes its own validation on the checked-out SHA; externally attested SHA-specific validation remains tracked in #62.

## Version and naming

`VERSION` and `v<version>` identify the release. A national-flower codename is presentation-only metadata from a fixed repository-maintained pool; no live external naming service is consulted at publication.
