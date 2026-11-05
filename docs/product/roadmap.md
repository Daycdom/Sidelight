# Roadmap

| Field | Value |
| --- | --- |
| Status | Draft |
| Last updated | 2026-11-04 |

Phases run in order. Highlighted releases ship publicly. No dates are set yet.

| Phase | Scope | Release |
| --- | --- | --- |
| 0 Foundations | Monorepo, CI, keyring, shared output-saving helpers | None |
| 1 Screen Reader | UI Automation text, Windows Graphics Capture + Windows OCR, change events, optional transcripts | **Screen Reader v0.1** |
| 2 Redactor | Rules plus local NER, mask/placeholder/remove modes, accuracy test set | **Redactor v0.1** |
| 3 Co-pilot | AI Router (Anthropic, OpenAI, Ollama), triggers, prompts, per-file context | **AI Router v0.1, Co-pilot CLI v0.1** |
| 3b Agent Bridge (proposed) | Local MCP server giving other agents read-only, redacted window text (ADR-0011). Needs only Reader and Redactor, so it can start any time after phase 2 | **Bridge v0.1** |
| 4 Desktop UI | pywebview shell, settings, profiles, suggestion panel, tray, hotkeys | Beta |
| 5 Voice | Local read-aloud, push-to-talk dictation, voice prompts | **Voice v0.1** |
| 6 Windows release | Signed installer, auto-update, first-run privacy screen, sandboxed workers (ADR-0017) | **Windows app 1.0** |
| 7 macOS port | ScreenCaptureKit, Accessibility API, Vision OCR, App Sandbox entitlements, notarization | **macOS 1.0** |
| 8 Later | Built-in on-device model, Linux, opt-in image input, game suggestions, enterprise tier | — |
