# Roadmap

| Field | Value |
| --- | --- |
| Status | Draft |
| Last updated | 2026-11-04 |

Build each part on its own first, release it, then combine them (decided 2026-11-05). Phases run in order. Highlighted releases ship publicly. No dates are set yet.

| Phase | Scope | Release |
| --- | --- | --- |
| **Build the parts** | | |
| 0 Foundations | Monorepo, CI, keyring, shared output-saving helpers | None |
| 1 Screen Reader | Built to completion first: UI Automation text, Windows Graphics Capture + Windows OCR, change events, optional transcripts, plus a small packaging spike (a signed .exe that lists windows) | **Screen Reader v0.1** |
| 1b Reader app | First standalone app (private apps repo, ADR-0018): pick a window, live text, save, copy. Builds the shared pywebview shell and components every later app reuses | **Sidelight Reader app** |
| 2 Redactor | Rules plus local NER, mask/placeholder/remove modes, background and cached redaction, accuracy test set | **Redactor v0.1** |
| 3 AI Router | Anthropic, OpenAI, Ollama and OpenAI-compatible backends, keys in the credential store, rate limits and spend caps | **AI Router v0.1** |
| 4 Voice | Local read-aloud and push-to-talk dictation | **Voice v0.1** |
| **Combine them** | | |
| 5 Co-pilot | Joins Reader, Redactor, Router and Voice: triggers, prompts, approval flow, per-file context | **Co-pilot CLI v0.1** |
| **Desktop app** | | |
| 6 Desktop UI | Full app (Sidelight Desk) on the shared shell: settings, profiles, suggestion panel with approval cards, tray, hotkeys | Beta |
| 7 Windows release | Signed installer, auto-update, first-run privacy screen, sandboxed workers (ADR-0017) | **Windows app 1.0** |
| 8 macOS port | ScreenCaptureKit, Accessibility API, Vision OCR, App Sandbox entitlements, notarization | **macOS 1.0** |
| 9 Later | Agent Bridge for other AI agents (ADR-0011, not a priority), built-in on-device model, Linux, opt-in image input, game suggestions, enterprise tier | — |

Each part's phase ends with a standalone release: its own CLI, tests, docs and changelog, usable without the others. Where a UI makes sense (Redactor next, later Voice and Router), a small standalone app can follow its CLI, reusing the shell from phase 1b.
