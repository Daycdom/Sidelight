# ADR-0015: Keep storage small and deletions real

- Status: Accepted
- Date: 2026-11-05
- Deciders: Dominic

## Context and problem

Text is small (about 2 KB per page), but ML models, transcripts kept over months, context history and logs add up. Deleted data that stays on disk is also a privacy problem.

## Decision

| Data | Rule |
| --- | --- |
| ML models | Smallest model that meets accuracy targets by default; quantized (8-bit) builds where available; larger models are optional downloads; one shared copy per model; the user can remove models from settings |
| Saved transcripts | Store changed paragraphs, not full snapshots; compress (zlib from the standard library; zstd once Python 3.14 is the minimum), compressing **before** encrypting |
| Context store | Rolling summaries per file rather than full history; a cap on entries per file; retention applied on startup and daily |
| Redaction cache | Each unique paragraph stored once (shared with transcripts by its HMAC key); least-recently-used entries dropped past a size cap |
| Logs | Rotating, hard cap (default 3 files of 5 MB, 14 days) |
| SQLite databases | `PRAGMA secure_delete = ON` so deleted rows are overwritten, and incremental auto-vacuum so space is returned |

Settings include a **Storage** page showing usage per category, with clear buttons and an optional overall cap.

## Consequences

- Good: small, predictable disk use; "delete" removes data from disk, not just from view.
- Bad: diff-based transcripts are slower to read back than full snapshots; `secure_delete` makes deletes slightly slower.
- Follow-ups: NFR-16 to NFR-18.
