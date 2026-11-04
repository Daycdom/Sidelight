# ADR-0008: Output files are opt-in

- Status: Accepted
- Date: 2026-11-04
- Deciders: Dominic

## Context and problem

Users may want to keep transcripts, redaction reports or suggestion history. Saving screen text by default would contradict the privacy goal.

## Decision

Saving is off by default. When enabled, the user picks the folder, format (.txt, .md, .jsonl), and retention period, with optional encryption using a key in the OS credential store. Shared helpers live in `common`.

## Consequences

- Good: users who want records get them; nothing is left on disk otherwise.
- Bad: one more settings area to build and test.
