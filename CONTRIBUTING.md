# Contributing

Thanks for helping. This repo holds the open-source packages of Sidelight: `sidelight-common`, `sidelight-reader`, `sidelight-redact`, `sidelight-router`, `sidelight-voice` and `sidelight-copilot` (see the [package map](docs/process/dev-setup.md#package-map)).

## Getting started

1. Follow [developer setup](docs/process/dev-setup.md), or install [uv](https://docs.astral.sh/uv/) and run `uv sync` at the repo root.
2. All packages install in editable mode into `.venv`.
3. `uv run pytest` runs the tests. Platform tests need Windows (or macOS once supported).
4. `uv run pre-commit install` enables lint and format hooks.

## Making a change

1. Open or find an issue first for anything beyond a small fix.
2. Branch from `main`: `feat/...`, `fix/...`, `docs/...`.
3. Use [Conventional Commits](https://www.conventionalcommits.org/) with the package as scope.
4. Add or update tests. Privacy-related changes need a privacy test (see the [test plan](docs/quality/test-plan.md)).
5. Update docs: requirements, ADRs and changelog as described in the [release process](docs/process/release-process.md).
6. Open a pull request; CI must pass.

## Ground rules

- Never add network calls outside AI Router, telemetry, or code that writes screen content to disk without the saving setting.
- Never commit real personal data or real API keys, including in test fixtures.
- Platform-specific code goes only in Screen Reader platform adapters.

## Code of conduct

This project follows the [Contributor Covenant](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
