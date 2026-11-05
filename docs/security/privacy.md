# Privacy and Data Handling

| Field | Value |
| --- | --- |
| Status | Draft |
| Version | 0.1 |
| Owner | Dominic |
| Last updated | 2026-11-04 |

## 1. Principles

1. **Local by default.** Nothing leaves the device except text the user sends to the AI backend they chose.
2. **Minimum data.** Only one approved window is read; images are discarded right after text extraction.
3. **Redact, show, then ask.** Everything is redacted before it is sent anywhere, the user sees what was redacted, and nothing is sent without their approval. Approval is on by default; the user decides when it's needed (ADR-0012).
4. **User decides storage.** Saving is off unless the user turns it on.
5. **No telemetry** in v1.

## 2. Data inventory

| Data | Collected when | Stored where | Retention | Shared with |
| --- | --- | --- | --- | --- |
| Window text | While watching | Memory | Session | Chosen AI backend, redacted |
| Window images | OCR fallback only | Child-process memory | Milliseconds | Nobody |
| Transcripts | Saving on | User folder | User setting | Nobody |
| Redaction reports | Saving on | User folder | User setting | Nobody (contain types and counts only) |
| Suggestion history | Saving on | User folder | User setting | Nobody |
| Per-file context | While watching | Encrypted SQLite, app data folder | User setting, default 30 days | Chosen AI backend, redacted, as prompt context |
| Redaction cache | While watching | Encrypted context store; saved text files as backup only when saving is on | Context store retention (default 30 days); saving retention for the backup | Nobody (redacted text and HMAC keys only, no originals) |
| Dictation audio | Push-to-talk held | Memory | Until transcribed | Nobody |
| API keys | User enters them | OS credential store | Until removed | Their own provider only |
| Settings and profiles | Always | App data folder | Until uninstall | Nobody |
| Crash logs | On error | App data folder | 14 days | Only if the user attaches them to a bug report |

## 3. User controls

- Pick which window is read; stop any time; capture indicator always visible.
- Blocklist apps (password managers and banking apps suggested at first run).
- Turn saving on or off; choose folder, format, retention and encryption.
- View and delete per-file context, or wipe everything from settings.
- Choose the AI backend per profile, including local-only.

## 4. Third-party processing

When a cloud backend is used, the provider's own terms and retention apply. The settings screen links to each provider's data-use policy. Self-hosted and on-device backends involve no third party.

## 5. Legal notes (to review before enterprise release)

- Capturing calls or chats may record other people; the docs advise users to follow local consent laws.
- Enterprise deployment may count as employee monitoring under GDPR or local labor law; an enterprise tier needs a data processing review.
