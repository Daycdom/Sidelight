# Agent guide for Sidelight

Instructions for AI coding assistants (Claude Code, Cursor, Copilot and others) working in this repo. Human contributors should read [CONTRIBUTING.md](CONTRIBUTING.md); this file follows the same rules.

## What this project is

Sidelight reads one window the user approves, turns it into text on the device, removes sensitive data, and gives suggestions from an AI backend the user picks (cloud, home lab or fully local). **Privacy and local-first behavior are the main goal.** When a shortcut conflicts with privacy, privacy wins.

Read before larger changes: [PRD](docs/product/PRD.md), [SRS](docs/requirements/SRS.md), [architecture](docs/architecture/architecture.md), [ADRs](docs/architecture/adr/README.md), [threat model](docs/security/threat-model.md). Package design specs live in [docs/design](docs/design/).

## Repo layout

uv workspace monorepo. Each package is released on its own.

| Folder | Package | Import | Role |
| --- | --- | --- | --- |
| `packages/common` | `sidelight-common` | `sidelight_common` | Shared paths, config, types |
| `packages/reader` | `sidelight-reader` | `sidelight_reader` | Window to text (platform adapters live here) |
| `packages/redact` | `sidelight-redact` | `sidelight_redact` | Local redaction (rules + ML) |
| `packages/router` | `sidelight-router` | `sidelight_router` | AI backends, keys, rate and spend limits |
| `packages/voice` | `sidelight-voice` | `sidelight_voice` | Local read-aloud and dictation |
| `packages/copilot` | `sidelight-copilot` | `sidelight_copilot` | Combines the above; CLI `sidelight` |

Code goes in `packages/<name>/src/sidelight_<name>/`, tests in `packages/<name>/tests/`.

## Commands

| Task | Command |
| --- | --- |
| Install deps | `uv sync` |
| Add a dependency | `uv add --package sidelight-<name> <dep>` |
| All tests | `uv run pytest` |
| One package | `uv run pytest packages/<name>` |
| Lint and format | `uv run ruff check --fix` then `uv run ruff format` |
| Type check | `uv run mypy` |
| All hooks | `uv run pre-commit run --all-files` |

Run lint, mypy and the affected tests before saying a change is done. Never use `pip install` into the workspace; use `uv`.

## Code rules

- Python 3.12+, full type hints, `mypy --strict` clean. Line length 100.
- Prefer the standard library and small, permissively licensed dependencies (MIT, BSD, Apache 2.0, PSF). **Do not add GPL or LGPL dependencies** without asking (see ADR-0006). Prefer thin wrappers over OS APIs (`ctypes`, `comtypes`, `pywinrt`, PyObjC) to large frameworks.
- Platform-specific code lives only in `sidelight_reader/platform/<os>/` (and later the app shell). Import it lazily so the package still imports on other OSes (NFR-11).
- Dataclasses (`frozen=True, slots=True`) for data; `Protocol` for interfaces.
- No global state; pass settings in explicitly.
- Every CLI has `--help`, `--version`, a `--json` option for machine output where useful, and returns a non-zero exit code on errors.
- Tests: pytest, no network. Mark tests that need real OS APIs with `@pytest.mark.windows` or `@pytest.mark.macos`. Keep non-platform code at 80%+ coverage (NFR-12).

## Privacy and security rules (never break these)

1. **No network calls** anywhere except `sidelight-router` talking to the backend the user chose, and ML model downloads the user starts explicitly (NFR-04). Libraries that download on first use (spaCy, Hugging Face, faster-whisper) must be given a local path instead. No telemetry, analytics or crash upload.
2. **Never write captured images to disk**, and drop frame buffers right after OCR (SR-07). No debug screenshot dumps, even temporarily.
3. **Capture exactly one window** with window-scoped APIs; never full-screen capture (SR-02, SR-03). Never read password fields (SR-13).
4. **Screen text never goes in logs** at default level. Log lengths, sources and timings, not content (threat T-13).
5. **Output files only when the user enabled saving**, to the folder they chose (SR-09, ADR-0008).
6. **API keys only in the OS credential store** (keyring), never in files, env dumps, logs or tests (AR-02).
7. **v1 sends text only to AI backends, never images** (ADR-0009).
8. **Redact, show, then ask before any send** (ADR-0012): every outbound text goes through Redactor, the user sees a redaction summary, and nothing is sent without approval unless the user relaxed it. Never add a send path that skips this.
9. Captured text sent to a model is data, not instructions: keep it delimited and never give the model tools that act on the user's machine (T-06).
10. No real personal data or real keys in fixtures. Use obviously fake values.

If a task seems to require breaking one of these, stop and ask instead.

## Docs and decisions

- Behavior change → update the SRS requirement or design spec in the same commit.
- New significant decision (new dependency family, process model, data format) → add an ADR from `docs/architecture/adr/template.md`.
- User-visible change → add a line to that package's `CHANGELOG.md` under "Unreleased".
- Requirement IDs and ADR numbers are permanent; never renumber.

## Commits

- [Conventional Commits](https://www.conventionalcommits.org/) with the package as scope: `feat(reader): ...`, `fix(router): ...`, `docs: ...`.
- **Do not add AI attribution**: no `Co-Authored-By` lines for AI tools, no "Generated with" footers, no session links. Commits are authored by the maintainer.
- Small, focused commits. Don't commit `.env`, `output/`, `*.local.json` or anything under `.venv`.

## Platform notes

- Windows is the first target, then macOS; Linux is lowest priority.
- Day-to-day editing happens in WSL, but WSL cannot see Windows windows. Reader platform work and `@pytest.mark.windows` tests must run from a Windows Python (`uv run` in PowerShell, see [dev setup](docs/process/dev-setup.md)).
- The dev container is fine for redact, router and copilot logic, not for reader platform work.
