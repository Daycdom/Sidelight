# ADR-0013: Redact ahead of time and reuse saved text files as the redaction cache

- Status: Accepted
- Date: 2026-11-05
- Deciders: Dominic

## Context and problem

ADR-0012 requires redaction before every send. Redaction is fast (roughly 5 to 600 ms per page depending on the tier) but it still sits in front of every suggestion, and most of a watched document doesn't change between suggestions.

## Decision

1. **Redact ahead of time.** Screen text is redacted in the background whenever it changes, so redacted text is ready when a trigger fires.
2. **Redact only what changed.** Text is split into paragraphs (or code blocks). Each paragraph's redacted form is cached and reused until that paragraph changes.
3. **The saved text files are the cache.** When the user has turned saving on (ADR-0008), the redacted transcript files double as the persistent cache, so reopening a file doesn't redo work. When saving is off, the cache lives in memory only and disappears when the session ends.
4. **What the cache holds.** Only redacted text, never originals. Each entry is keyed by an HMAC of the original paragraph, using a key held in the OS credential store. A plain hash isn't used because short values like emails could be recovered from it by guessing.
5. **Invalidation.** Each entry records the Redactor version, tier, custom patterns and allow-list it was made with; any change to those discards the entry.

## Consequences

- Good: redaction cost is close to zero at send time; reopening a saved document is instant.
- Bad: the transcript format must carry cache keys and the ruleset version (`.jsonl` does this naturally; `.txt` and `.md` need a small sidecar file); one more key in the credential store.
- Follow-ups: SRS RD-09 to RD-11; Redactor design spec; privacy data inventory.
