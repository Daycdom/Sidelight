# ADR-0018: Two repositories, with a standalone app per tool

- Status: Accepted
- Date: 2026-11-05
- Deciders: Dominic

## Context and problem

Each part should work on its own, both as a CLI and, where it makes sense, as an app with its own interface. The CLIs are the free, open-source version; every graphical interface is closed source (ADR-0006). Separate repositories per tool would multiply CI, tooling and cross-repo changes for a solo developer.

## Options considered

1. One repository per tool (public CLI repos plus private UI repos).
2. Two repositories: the public monorepo for every engine and CLI, and one private repository for every app.

## Decision

Option 2.

- **Public `Daycdom/Sidelight`:** every engine and CLI, each released and installable on its own (ADR-0005).
- **One private apps repository:** the full desktop app (Sidelight Desk) and small standalone apps for the tools where a UI makes sense: **Sidelight Reader** (pick a window, live text, save, copy, read aloud) and **Sidelight Redact** (paste or drop text, see redactions highlighted, approve, export). Later possibly Voice and Router apps.
- All apps share one pywebview shell, one component library and one look; each app is a separate build showing a subset of screens, signed with the same certificate.
- Users find each tool through the website, with one page and download per tool (release process §8).

## Consequences

- Good: one place for shared UI code; each tool still has its own app, page, version and download.
- Bad: the private repo depends on published (or pinned) versions of the public packages, so UI work sometimes waits on a package release.
- Follow-ups: create the private repo when the first app starts; Screen Reader's app is the first, and builds the shared shell.
