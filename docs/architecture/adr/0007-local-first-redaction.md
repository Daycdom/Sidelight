# ADR-0007: Local by default; redact before any cloud call

- Status: Accepted
- Date: 2026-11-04
- Deciders: Dominic

## Context and problem

Screen text can contain passwords, personal data and secrets. Security is the product's main goal.

## Decision

- Everything runs on-device except AI Router calls to the backend the user chose and an opt-in update check.
- Co-pilot always passes text through Redactor before a cloud backend. For self-hosted or on-device backends, redaction is on by default and may be turned off by the user.
- Users can block apps from capture entirely.
- No telemetry in v1.

## Consequences

- Good: a clear, auditable privacy promise.
- Bad: redaction adds latency and can mask useful context (e.g. names in an essay); users can allow-list terms.
