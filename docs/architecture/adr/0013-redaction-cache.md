# ADR-0013: Redact ahead of time and cache results in the context store

- Status: Accepted
- Date: 2026-11-05
- Deciders: Dominic

## Context and problem

ADR-0012 requires redaction before every send. Redaction is fast (roughly 5 to 600 ms per page depending on the tier) but it still sits in front of every suggestion, and most of a watched document doesn't change between suggestions.

## Options considered

1. Saved text files as the only persistent cache.
2. The encrypted context store, with saved text files as a backup when the store has expired.

## Decision

Option 2.


1. **Redact ahead of time.** Screen text is redacted in the background whenever it changes, so redacted text is ready when a trigger fires.
2. **Redact only what changed.** Text is split into paragraphs (or code blocks). Each paragraph's redacted form is cached and reused until that paragraph changes.
3. **Primary cache: the encrypted per-file context store** (CP-05). Cached entries live with that file's context, are always encrypted, and are wiped with it (by the user or by its retention period, default 30 days).
4. **Backup: the saved text files.** When the context store entry has expired and the user has saving turned on (ADR-0008), the redacted transcript files are used to refill the cache instead of redacting again. Each saved entry carries its cache key, ruleset version and a MAC; entries that were edited, or don't match the current ruleset, are ignored and redacted fresh. With saving off there is no backup.
5. **What the cache holds.** Only redacted text, never originals. Each entry is keyed by an HMAC of the original paragraph, using a key held in the OS credential store. A plain hash isn't used because short values like emails could be recovered from it by guessing.
6. **Invalidation.** Each entry records the Redactor version, tier, custom patterns and allow-list it was made with; any change to those discards the entry.

## Consequences

- Good: redaction cost is close to zero at send time; the cache is always encrypted and can't be broken by editing, moving or syncing transcripts; saved files still save work after the context store expires.
- Bad: the cache outlives the session even when saving is off (redacted, encrypted text only, under the context store's retention). For the backup, transcripts must carry cache keys, ruleset version and a MAC (`.jsonl` does this naturally; `.txt` and `.md` need a small sidecar file). One more key in the credential store.
- Follow-ups: SRS RD-09 to RD-11; Redactor design spec; privacy data inventory.
