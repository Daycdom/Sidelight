# ADR-0005: Standalone sub-projects in one monorepo

- Status: Accepted
- Date: 2026-11-04
- Deciders: Dominic

## Context and problem

Parts of the suite are useful on their own: screen-to-text, redaction, multi-backend AI access, and voice. Building them as one application would hide that value and make testing harder.

## Options considered

1. One package.
2. Separate repositories per sub-project.
3. One monorepo with separately versioned packages (`uv` workspaces).

## Decision

Option 3. Packages (PyPI names): `sidelight-common`, `sidelight-reader`, `sidelight-redact`, `sidelight-router`, `sidelight-voice`, `sidelight-copilot`. The desktop app lives in a separate closed-source repo and depends on the published packages.

## Consequences

- Good: each package has its own CLI, tests, version and changelog; shared CI and tooling.
- Bad: release automation must handle multiple packages.
- Follow-ups: packages may only depend on `common` and on packages listed in the architecture doc; no circular dependencies.
