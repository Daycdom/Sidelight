# Development and Release Process

| Field | Value |
| --- | --- |
| Status | Draft |
| Version | 0.1 |
| Owner | Dominic |
| Last updated | 2026-11-04 |

## 1. Versioning

- [Semantic Versioning 2.0](https://semver.org/): `MAJOR.MINOR.PATCH`. Before 1.0, minor versions may break APIs.
- Each package is versioned independently. Tags: `<package>-v<version>`, e.g. `redact-v0.1.0`.
- Each package keeps a `CHANGELOG.md` in [Keep a Changelog](https://keepachangelog.com/) format.

## 2. Branching

- Trunk-based: `main` is always releasable.
- Short-lived branches: `feat/...`, `fix/...`, `docs/...`, `chore/...`.
- Merge via pull request with CI green; squash merge.

## 3. Commits

[Conventional Commits](https://www.conventionalcommits.org/) with the package as scope, e.g. `feat(redact): add Luhn check for card numbers`. This drives changelog generation.

## 4. Continuous integration

| Job | Runs on | Checks |
| --- | --- | --- |
| Lint and format | Ubuntu | ruff, ruff format, mypy |
| Unit and integration tests | Ubuntu, Windows | pytest with coverage report |
| Platform tests | Windows (macOS from phase 8) | Real OS API tests (planned; run manually on a Windows PC until then) |
| Security | Ubuntu | pip-audit in CI; GitHub secret scanning and Dependabot in repo settings |
| UI | Ubuntu | Vitest, Playwright, type check (desktop app repo, from phase 6) |

## 5. Release steps

1. Confirm the test plan exit criteria for the release.
2. Update the package `CHANGELOG.md`; move "Unreleased" items under the new version.
3. Bump the version, open a release PR, merge.
4. Tag `<package>-v<version>`; CI builds and publishes to PyPI with trusted publishing.
5. Desktop app only: build with PyInstaller, sign (Windows Authenticode; macOS Developer ID + notarization), create installer, publish update manifest signed with the release key.
6. Create a GitHub release with changelog notes and checksums.
7. Re-run the threat model review for minor and major releases.

## 6. Hotfixes

Fix on a branch from `main`, release as a PATCH version. Security fixes follow [SECURITY.md](../../SECURITY.md).

## 7. Documentation updates

A PR that changes behavior updates the matching SRS requirement, ADR (new one if a decision changes), and user docs in the same PR.

## 8. Distribution

Decided 2026-11-05: most users install from the web, so the website is the front door.

| Channel | For | Notes |
| --- | --- | --- |
| Website (GitHub Pages at sidelight.friendzone.dev) | Everyone | A landing page listing every tool and one page per tool, each with a "Download for Windows" button. Buttons link to the installer on that tool's GitHub release; a workflow refreshes the page on each release. Shows SHA-256 checksums |
| GitHub Releases | Downloads behind the website, developers | One release per tool tag, titled by tool ("Sidelight Redact 0.1.0") |
| PyPI | CLI users | `pipx install sidelight-<tool>`; each tool's README is its PyPI page |
| winget | Enthusiasts | Optional extra once installers exist |

Not planned: Microsoft Store (few users install from it), and separate repos per tool. Each tool still gets its own page, download and changelog.

Web downloads depend on code signing: unsigned or newly signed installers trigger a Windows SmartScreen warning until the certificate builds reputation. Sign every installer (NFR-07), keep one certificate for all tools so reputation is shared, and expect warnings for the first releases.
