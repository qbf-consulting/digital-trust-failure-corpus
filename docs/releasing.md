# Publishing a release

Digital Trust Failure Corpus publishes GitHub Releases through the manual `publish release` GitHub Actions workflow.

## Release identity

The machine-readable release identity remains the semantic version in `VERSION` and its corresponding `v<version>` Git tag. A flower codename is presentation metadata only.

Release titles use:

```text
<Flower> — v<version>
```

For example, a release may appear as `Lotus — v0.1.0` while the stable tag remains `v0.1.0`.

## Codename pool

Release codenames are selected randomly from [`release/national-flower-codenames.txt`](../release/national-flower-codenames.txt). The pool is a curated, deduplicated snapshot derived from Wikipedia's [List of national flowers](https://en.wikipedia.org/wiki/List_of_national_flowers), reviewed on 2026-09-15.

The workflow does not fetch Wikipedia at publication time. That keeps a release independent of an external content service and makes the eligible naming pool reviewable in the repository.

Previously used codenames are excluded while unused names remain. If the pool is eventually exhausted, selection starts again from the complete pool.

## Publication gate

Before publishing, the workflow:

1. requires dispatch from `main`;
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

From the GitHub repository:

1. open **Actions**;
2. select **publish release**;
3. choose **Run workflow**;
4. ensure the selected branch is `main`;
5. run the workflow.

Publication is intentionally manual. Merging release preparation or changing `VERSION` must never publish a release implicitly.

## Preparing a future release

Before dispatching the publication workflow, merge a normal release-preparation PR that updates at minimum:

- `VERSION`;
- `CHANGELOG.md`;
- `docs/release-notes-v<version>.md`;
- any release-baseline assertions that intentionally change with the version.

The resulting GitHub Release is explicitly designated Latest so the repository release surface identifies the newest published baseline clearly.
