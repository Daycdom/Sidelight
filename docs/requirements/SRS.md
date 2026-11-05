# Software Requirements Specification: Sidelight

| Field | Value |
| --- | --- |
| Status | Draft |
| Version | 0.1 |
| Owner | Dominic |
| Last updated | 2026-11-04 |
| Structure | Follows ISO/IEC/IEEE 29148 (requirements specification) in simplified form |

## 1. Introduction

### 1.1 Purpose

This document lists the testable requirements for every Sidelight component. The [PRD](../product/PRD.md) explains why; this explains what.

### 1.2 Conventions

- **Shall** = required for the stated release. **Should** = desired, may slip. **May** = optional.
- Each requirement has an ID (`SR-` Screen Reader, `RD-` Redactor, `AR-` AI Router, `VO-` Voice, `CP-` Co-pilot, `UI-` Desktop app, `AG-` Agent Bridge, `NFR-` non-functional, `CON-` constraint).
- Priority: **M** must, **S** should, **C** could (MoSCoW).
- Requirement IDs never change once published; removed requirements are marked *Withdrawn*.

### 1.3 Definitions

| Term | Meaning |
| --- | --- |
| Target window | The one application window the user approved for capture |
| Text source | A way to get text: accessibility API, native OCR, or Tesseract |
| Backend | An AI provider: Anthropic, OpenAI, Ollama, or on-device model |
| Profile | A saved set of settings tied to one or more apps |
| Output file | Any file the suite writes with user content: transcripts, reports, history |

## 2. Overall description

### 2.1 Product perspective

Six open-source Python packages (Screen Reader, Redactor, AI Router, Voice, Co-pilot and the shared `common`), a proposed seventh (Agent Bridge, ADR-0011), and one closed-source desktop app. See [Architecture](../architecture/architecture.md).

### 2.2 Operating environment

| Platform | Release | Minimum |
| --- | --- | --- |
| Windows | v1.0 | Windows 11. Windows 10 22H2 best effort (Microsoft ended mainstream support on 14 October 2025; Windows Graphics Capture window capture itself needs 1903 or later) |
| macOS | after Windows 1.0 | macOS 13 or later (ScreenCaptureKit) |
| Linux | later | X11 first; Wayland via portals |

### 2.3 Assumptions and dependencies

- Users supply their own API keys or self-hosted server.
- Windows OCR needs at least one OCR language pack installed (default on most systems).
- Ollama, if used, is installed and run by the user.

## 3. Functional requirements

### 3.1 Screen Reader

| ID | Requirement | Priority |
| --- | --- | --- |
| SR-01 | The system shall list visible top-level windows with title and process name. | M |
| SR-02 | The system shall capture text from exactly one user-selected window. | M |
| SR-03 | The system shall use OS window-scoped capture so overlapping windows are never read. | M |
| SR-04 | The system shall try text sources in order: accessibility API, native OCR, Tesseract. | M |
| SR-05 | The system shall report the focused element and caret position when the accessibility API provides them. | S |
| SR-06 | The system shall emit an event only when the extracted text changes. | M |
| SR-07 | The system shall discard captured image data immediately after OCR and never write it to disk. | M |
| SR-08 | The system shall stop when the user stops it or the target window closes. | M |
| SR-09 | The system shall save transcripts only when saving is enabled, to the user-chosen folder, in .txt, .md or .jsonl. | M |
| SR-10 | The system shall delete saved transcripts older than the user-set retention period. | S |
| SR-11 | The system shall provide a CLI (`sidelight-reader list-windows`, `read`, `watch`, `sources`). | M |
| SR-12 | The system shall expose a Python API emitting text-change events. | M |
| SR-13 | The system shall never read text from elements the accessibility API marks as password fields. | M |

### 3.2 Redactor

| ID | Requirement | Priority |
| --- | --- | --- |
| RD-01 | The system shall detect API keys and tokens, payment card numbers (with Luhn check), emails and phone numbers by rule. | M |
| RD-02 | The system shall detect person names, addresses and organization names with a local ML model. | M |
| RD-03 | The system shall support modes: mask by type, consistent placeholders, or remove. | M |
| RD-04 | The system shall run entirely on-device with no network access. | M |
| RD-05 | The system shall accept text from a file, stdin, or Python call. | M |
| RD-06 | The system shall optionally write a report of entity types and counts masked, never the original values. | S |
| RD-07 | The system shall allow user-defined custom patterns and allow-lists. | S |
| RD-08 | The system shall process 2,000 characters in under 200 ms on the reference PC (see NFR-02). | S |
| RD-09 | The system shall redact text in the background as it changes, so redacted text is ready before a send is triggered (ADR-0013). | S |
| RD-10 | The system shall redact only changed paragraphs, reusing cached results for unchanged ones. | S |
| RD-11 | The redaction cache shall hold only redacted text keyed by an HMAC of the original, be stored in the encrypted per-file context store, and be discarded when the Redactor version, tier, patterns or allow-list change. | M |
| RD-12 | When a context store entry is expired, missing, corrupted or unreadable and saving is on, the system should refill the cache from saved text files, ignoring entries that fail their MAC check or ruleset match. | S |

### 3.3 AI Router

| ID | Requirement | Priority |
| --- | --- | --- |
| AR-01 | The system shall offer one interface for Anthropic, OpenAI, Ollama and OpenAI-compatible servers (e.g. vLLM, LM Studio). | M |
| AR-02 | The system shall store API keys only in the OS credential store. | M |
| AR-03 | The system shall enforce a per-hour request limit set by the user. | M |
| AR-04 | The system shall enforce an optional daily spend cap, using provider token prices. | S |
| AR-05 | The system shall support a fallback backend when the primary is unreachable. | S |
| AR-06 | The system shall stream responses when the backend supports it. | S |
| AR-07 | The system shall optionally log requests (time, backend, token counts, cost) without prompt content. | C |
| AR-08 | The system shall provide a CLI (`sidelight-router ask`, `sidelight-router keys`). | M |

### 3.4 Voice

| ID | Requirement | Priority |
| --- | --- | --- |
| VO-01 | The system shall read given text aloud using local OS voices. | M |
| VO-02 | The system shall transcribe speech on a push-to-talk hotkey using a local model. | M |
| VO-03 | The system shall never send audio off the device. | M |
| VO-04 | The system shall let the user choose voice, speed and input device. | S |
| VO-05 | The system shall save dictation transcripts only when saving is enabled. | S |

### 3.5 Co-pilot

| ID | Requirement | Priority |
| --- | --- | --- |
| CP-01 | The system shall pass captured text through the Redactor before any backend call, cloud or local (ADR-0012). | M |
| CP-02 | The system shall never capture apps on the user's blocklist. | M |
| CP-03 | The system shall support triggers: manual hotkey, typing pause, every N words, fixed interval. | M |
| CP-04 | The system shall use the user's custom prompt when given, otherwise build one from app type and recent text. | M |
| CP-05 | The system shall keep context per file, keyed by app and window title, in an encrypted local store. | M |
| CP-06 | The system shall let the user view and delete stored context per file or entirely. | M |
| CP-07 | The system shall apply per-app profiles automatically when the focused app changes. | S |
| CP-08 | The system shall support "when / then" rules (e.g. on save, check for bugs). | C |
| CP-09 | The system shall treat captured text as data in prompts, never as instructions. | M |
| CP-10 | The system shall save suggestion history only when saving is enabled. | M |
| CP-11 | The system shall not send any text to any destination until the user approves it. Approval shall be required by default. | M |
| CP-12 | The system shall let the user choose, per profile and destination, when approval is needed: every send (default), once per session, only when something was redacted, or never. | M |
| CP-13 | Before approval, the system shall show the user a summary of what was redacted (types and counts) and the outgoing text with placeholders highlighted, and let them edit it or allow-list a term. | M |

### 3.6 Desktop app

| ID | Requirement | Priority |
| --- | --- | --- |
| UI-01 | The app shall provide a window picker, settings, profiles and a suggestions panel. | M |
| UI-02 | The app shall show a persistent indicator whenever capture is active. | M |
| UI-03 | The app shall offer docked, floating and minimized ("pill") panel modes. | S |
| UI-04 | The app shall provide a system tray icon and global hotkeys. | M |
| UI-05 | The app shall let the user customize accent color, theme, text size and panel opacity. | S |
| UI-06 | All UI-to-Python calls shall go through one API module (`ui/src/api.ts`). | M |
| UI-07 | The app shall show a first-run privacy explanation before any capture. | M |
| UI-08 | The app shall show an approval card in the suggestions panel for each pending send, with the redaction summary and Approve, Edit and Deny actions. | M |

### 3.7 Agent Bridge (proposed, ADR-0011)

| ID | Requirement | Priority |
| --- | --- | --- |
| AG-01 | The system shall expose the approved window's text to other AI agents as a local MCP server over stdio. | S |
| AG-02 | The system shall offer read-only tools and resources only; no tool shall act on the user's machine. | M |
| AG-03 | The system shall let only the user choose the window; agents shall not list or switch windows. | M |
| AG-04 | The system shall pass every result through the Redactor, with no option to turn it off. | M |
| AG-05 | The system shall mark results as untrusted screen content. | M |
| AG-06 | The system shall show the capture indicator while an agent is connected and log each read without content. | M |
| AG-07 | The system shall enforce a per-minute read limit and require the user's approval for each read by default, with the redaction summary shown (ADR-0012). | M |

## 4. Non-functional requirements

| ID | Category | Requirement | Priority |
| --- | --- | --- | --- |
| NFR-01 | Performance | Idle CPU while watching a static window shall be under 3% on the reference PC. | M |
| NFR-02 | Performance | Reference PC: 4-core x86-64, 16 GB RAM, Windows 11, no discrete GPU. | M |
| NFR-03 | Performance | Text change to event shall take under 500 ms with accessibility text. | S |
| NFR-04 | Privacy | No component shall make network calls except AI Router to the user's chosen backend, the opt-in update check, a one-time license activation when a paid user first enters their key (ADR-0006), and model downloads the user starts explicitly (Redactor and Voice models). | M |
| NFR-05 | Privacy | No telemetry shall be collected in v1. | M |
| NFR-06 | Security | Saved output files shall support encryption with a key held in the OS credential store. | S |
| NFR-07 | Security | Release binaries shall be code-signed (Windows) and notarized (macOS). | M |
| NFR-08 | Security | Dependencies shall be scanned for known vulnerabilities in CI. | M |
| NFR-09 | Reliability | A crash in capture shall not crash the UI; the app shall show an error and allow restart. | M |
| NFR-10 | Accessibility | The desktop app shall meet WCAG 2.2 AA for contrast, keyboard navigation and screen-reader labels. | M |
| NFR-11 | Portability | Platform-specific code shall live only in Screen Reader platform adapters and the app shell. | M |
| NFR-12 | Maintainability | Each package shall have at least 80% line coverage on non-platform code. | S |
| NFR-13 | Usability | A new user shall reach their first suggestion within 3 minutes of install. | S |
| NFR-14 | Privacy | The context store, redaction cache, settings and logs shall be stored only in the local, non-roaming app data folder (ADR-0014). | M |
| NFR-15 | Privacy | When the user picks a save folder inside a known sync or cloud folder, the system shall warn that files will leave the device and require confirmation. | M |
| NFR-16 | Storage | ML models shall default to the smallest version meeting accuracy targets; larger models shall be optional downloads the user can remove (ADR-0015). | M |
| NFR-17 | Storage | Saved transcripts shall store changed paragraphs only, compressed before encryption; logs shall rotate with a hard size cap. | S |
| NFR-18 | Privacy | SQLite stores shall use secure delete and auto-vacuum; settings shall show storage use per category with clear buttons. | M |
| NFR-19 | Reliability | Capture, OCR, Redactor ML and Voice models shall run in worker processes with an OS-enforced memory cap where available (Windows Job Objects), recycled by the supervisor after a work limit or memory budget (ADR-0016). | M |
| NFR-20 | Reliability | Every queue, buffer, cache and history shall have a maximum size. | M |
| NFR-21 | Reliability | Memory of the main process shall not grow more than 50 MB over 8 hours of watching a changing window on the reference PC (proposed target). | S |
| NFR-22 | Security | In installed builds, every worker except the window-reading broker shall run in an OS sandbox with only the access it needs: network for AI Router only, microphone for Voice only (ADR-0017). | M |

## 5. Constraints

| ID | Constraint |
| --- | --- |
| CON-01 | Backend language is Python 3.12+. |
| CON-02 | Desktop UI is a web frontend hosted by pywebview (see ADR-0002). |
| CON-03 | v1 sends text only to AI backends; no images. |
| CON-04 | Solo developer; scope is held to the phase plan in the build outline. |

## 6. Traceability

| User story (PRD) | Requirements |
| --- | --- |
| US-01 | SR-01, SR-02, SR-03, SR-13 |
| US-02 | AR-01, AR-05 |
| US-03 | CP-04 |
| US-04 | CP-03, AR-03, AR-04 |
| US-05, US-06 | CP-03, CP-04, CP-05 |
| US-07 | CP-03, CP-08 |
| US-08 | RD-01 to RD-04, CP-01, CP-11 to CP-13, UI-08 |
| US-09 | SR-09, SR-10, VO-05, CP-10, NFR-06 |
| US-10 | CP-05, CP-06 |
| US-11, US-12 | VO-01 to VO-04 |
| US-13 | CP-07 |
| US-14 | CP-02 |
| US-15 | SR-11, RD-05, AR-08 |
| US-16 | AG-01 to AG-07 |
