# Release publication

This repository supports two release-publication paths:

1. **PR-gated release request** — preferred for normal governed releases.
2. **Manual workflow dispatch** — retained for maintainer recovery or explicitly supervised publication.

## PR-gated release request

A release is requested by changing `release/publish-request.json` in a reviewed pull request:

```json
{
  "version": "0.2.0",
  "requested_by": "maintainer-login",
  "reason": "Short release rationale"
}
```

The request is intentionally separate from `VERSION`. This makes the publication authorization event explicit and auditable.

When the request PR is merged to `main`, the `publish release` workflow:

1. requires the request version to equal the repository `VERSION`;
2. runs the complete release-gate test suite and corpus validator;
3. requires the corresponding `docs/release-notes-v<version>.md`;
4. refuses to overwrite an existing tag or GitHub Release;
5. selects an unused codename from `release/national-flower-codenames.txt`;
6. publishes `v<version>` against the merged `main` commit;
7. marks the release as **Latest**; and
8. verifies the published title and Latest state.

A mismatched version, missing notes, failed validation, or existing tag/release stops publication.

## Preparing the next release

A release-preparation PR SHOULD update, as applicable:

- `VERSION`;
- `CHANGELOG.md`;
- `docs/release-notes-v<version>.md`;
- corpus/schema/tests for the release; and
- `release/publish-request.json` when publication is approved.

The release-request change SHOULD be the final explicit publication signal. Projects or automation consuming this repository should treat the GitHub Release/tag as the published release boundary, not the presence of an unreleased `VERSION` value alone.

## Authority boundary

Merging a change to `release/publish-request.json` is the repository-governed authorization to attempt publication. GitHub Actions is the enforcement mechanism; passing CI is evidence that the configured release gates were satisfied, not an independent certification of corpus correctness.
