# Release configuration

Design Reviewer uses GitHub Actions for both continuous validation and release packaging.

## CI

`.github/workflows/ci.yml` runs on pushes, pull requests and manual dispatches. It:

1. installs the Python dependencies used by the project tools,
2. lints the canonical project,
3. runs the structural eval suite,
4. checks project hygiene,
5. builds the canonical project package and all four runtime distributions,
6. validates every distribution,
7. verifies runtime parity,
8. uploads the generated ZIP files, checksums and delivery manifest as a CI artifact.

The CI build uses version `0.0.0-ci`; it is not a release version.

## Release

`.github/workflows/release.yml` runs when a GitHub Release is published.

The release tag must start with `v` and contain a semantic version, for example `v1.0.0` or `v1.0.0-rc.1`. The workflow derives the distribution version from the tag by removing the leading `v`.

Before uploading anything, the workflow runs the same lint, eval, hygiene, build, distribution validation and runtime-parity gates used by CI.

A successful release uploads:

- the canonical project ZIP,
- ChatGPT Chat ZIP,
- ChatGPT Custom GPT ZIP,
- Claude Projects ZIP,
- OpenCode ZIP,
- `SHA256SUMS.txt`,
- `DELIVERY-MANIFEST.json`.

The build remains reproducible because distribution ZIP timestamps are normalized by the canonical build script.
