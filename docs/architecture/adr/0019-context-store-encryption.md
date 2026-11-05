# ADR-0019: Encrypt the context store at the application level

- Status: Proposed (WIP, see open decisions #2)
- Date: 2026-11-05
- Deciders: Dominic

## Context and problem

The per-file context store and redaction cache (CP-05, ADR-0013) must be encrypted at rest. SQLite has no built-in encryption.

## Options considered

1. SQLCipher: an encrypted build of SQLite. Encrypts the whole file transparently, but is a native library that must be built or bundled for each platform, which complicates packaging and sandboxing (ADR-0017).
2. Application-level encryption: plain SQLite, with each stored value encrypted using AES-GCM from `cryptography` (Apache 2.0 / BSD) and a key held in the OS credential store. Only lookup keys (HMACs) and timestamps stay unencrypted.
3. OS disk encryption only (BitLocker, FileVault). Not under the app's control.

## Decision (proposed)

Option 2. It ships as ordinary wheels on Windows and macOS, needs no custom SQLite build, and the key never touches disk. Metadata exposure is limited to HMAC keys, sizes and timestamps.

## Consequences

- Good: simple packaging; per-entry encryption; works with `secure_delete` and auto-vacuum (ADR-0015).
- Bad: can't query inside encrypted values (not needed; lookups go by HMAC key); sizes and timestamps are visible to someone with file access.
- Follow-ups: confirm before phase 5; key rotation and "wipe everything" flows.
