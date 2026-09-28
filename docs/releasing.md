# Publishing a release

Digital Trust Failure Corpus publishes GitHub Releases through the governed `publish release` GitHub Actions workflow. Publication can occur automatically after a reviewed release-preparation PR changes `release/publish-request.json` on `main`, or through an explicit `workflow_dispatch` run from `main`.

## Release identity

The machine-readable release identity remains the semantic version in `VERSION` and its corresponding `v<version>` Git tag. A flower codename is presentation metadata only.

Release titles use:

```text
<Flower> — v<version>
```

For example, a release may appear as `Lotus — v0.1.0` while the stable tag remains `v0.1.0`.

## Codename pool

Release codenames are selected randomly from [`release/national-flower-codenames.txt`](https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/main/release/national-flower-codenames.txt). The pool is a curated, deduplicated snapshot derived from Wikipedia's [List of national flowers](https://en.wikipedia.org/wiki/List_of_national_flowers), reviewed on 2026-09-15.

The workflow does not fetch Wikipedia at publication time. That keeps a release independent of an external content service and makes the eligible naming pool reviewable in the repository.

Previously used codenames are excluded while unused names remain. If the pool is eventually exhausted, selection starts again from the complete pool.

## Publication gate

Before publishing, the workflow:

1. requires execution from `main`;
2. reads the version from `VERSION`;
3. requires `docs/release-notes-v<version>.md`;
4. runs the complete unit-test suite;
5. validates the complete corpus;
6. refuses to overwrite an existing tag or GitHub Release;
7. selects the codename;
8. creates the release against the exact workflow commit SHA;
9. explicitly marks the release as **Latest**;
10. verifies the title and Latest designation after publication.

Only this release workflow receives `contents: write`; the ordinary validation workflow remains read-only.

## Publishing

### PR-gated publication

The preferred path is:

1. prepare a normal release PR that updates `VERSION`, release notes, baseline assertions, and `release/publish-request.json`;
2. require the request version to match `VERSION`;
3. merge the reviewed PR to `main`;
4. the `publish release` workflow runs because the publish request changed;
5. the workflow reruns the complete release gates before creating the tag and GitHub Release.

This keeps publication tied to an inspectable repository change rather than to an unrecorded manual decision.

### Manual recovery or explicit publication

The workflow also supports `workflow_dispatch` from `main`:

1. open **Actions**;
2. select **publish release**;
3. choose **Run workflow**;
4. ensure the selected branch is `main`;
5. run the workflow.

The workflow still refuses to overwrite an existing tag or release. Manual dispatch does not bypass release validation.

## Preparing a future release

Before publication, merge a normal release-preparation PR that updates at minimum:

- `VERSION`;
- `CHANGELOG.md`;
- `docs/release-notes-v<version>.md`;
- any release-baseline assertions that intentionally change with the version;
- `release/publish-request.json` when PR-gated automatic publication is intended.

The resulting GitHub Release is explicitly designated Latest so the repository release surface identifies the newest published baseline clearly.
