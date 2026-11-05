# Product Requirements Document: Sidelight

| Field | Value |
| --- | --- |
| Status | Draft |
| Version | 0.1 |
| Owner | Dominic |
| Last updated | 2026-11-04 |
| Related | [SRS](../requirements/SRS.md), [Architecture](../architecture/architecture.md) |

## 1. Summary

Sidelight is a privacy-first desktop assistant. It reads the text of one application window the user approves, removes sensitive data locally, and offers real-time suggestions from the AI backend the user chooses: a cloud API, a self-hosted server, or an on-device model.

It is built as standalone sub-projects. Each is useful on its own:

| Sub-project | Purpose |
| --- | --- |
| Screen Reader | Turns an approved window into live text |
| Redactor | Finds and masks sensitive data in text, on-device |
| AI Router | One interface to Claude, ChatGPT and Ollama with limits and spend caps |
| Voice | Local read-aloud and push-to-talk dictation |
| Co-pilot | Combines the above into live suggestions |
| Desktop app | Graphical interface over the Co-pilot |
| Agent Bridge (proposed) | Gives other AI agents (Hermes Agent, Claude, Cursor and others) read-only, redacted text from the approved window over MCP |

## 2. Problem

People working in documents, code editors and browsers want help in context without copying text into a chat window. Existing assistants either live inside one app, send whole screenshots to the cloud, or cost a lot to run continuously. Privacy-minded users have no option that keeps raw screen data on their own machine.

## 3. Goals

1. Give useful, context-aware suggestions while the user works in any app.
2. Keep raw screen data on the device; send only redacted text, only to the backend the user chose.
3. Let the user control cost, frequency, tone and storage.
4. Make each component usable on its own.

## 4. Non-goals (v1)

- Controlling the mouse or keyboard, or acting on the user's behalf.
- Sending images to AI models (planned later as opt-in).
- Monitoring other users or employees.
- Linux support (later, lower priority).
- Built-in bundled language model (later; Ollama covers local models in v1).

## 5. Target users and personas

| Persona | Context | Need |
| --- | --- | --- |
| Student | Writing an essay in Word or Google Docs | Feedback on argument, clarity and evidence as they write |
| Developer | Writing code in an editor | Early warning on simple bugs; runtime analysis on request |
| Accessibility user | Low vision, limited typing, or reading difficulty | Text read aloud; dictate questions and get answers by voice |
| Privacy-conscious power user | Runs a home lab | Full control: self-hosted AI, no cloud, no stored data |

## 6. User stories

| ID | As a... | I want to... | So that... |
| --- | --- | --- | --- |
| US-01 | user | pick exactly one window to watch | nothing else on my screen is read |
| US-02 | user | choose Claude, ChatGPT, Ollama or an on-device model | I control cost and where my data goes |
| US-03 | user | write my own instructions before starting | suggestions follow my goal |
| US-04 | user | set how often suggestions appear, or trigger them by hotkey only | it never feels noisy or costs too much |
| US-05 | student | get suggestions as I write more | I improve the draft while working |
| US-06 | developer | see likely bugs before running my code | I catch simple mistakes early |
| US-07 | developer | ask for a runtime analysis of a function by hotkey | I get deeper help on demand |
| US-08 | user | have secrets and personal data masked, see what was masked, and approve before anything is sent | private information never leaves my PC without my say |
| US-09 | user | choose whether captured text and suggestions are saved, where, and for how long | I control what stays on disk |
| US-10 | user | have the assistant remember context per file | suggestions build on earlier work in that file only |
| US-11 | accessibility user | have text or suggestions read aloud | I can work without reading the screen |
| US-12 | accessibility user | dictate a question by voice | I can ask without typing |
| US-13 | user | set different behavior per app | my code editor and word processor each get the right help |
| US-14 | user | block apps entirely (e.g. password managers) | they are never captured |
| US-15 | CLI user | run each sub-project from the command line | I can script and automate it |
| US-16 | agent user | let the AI agent I already use read my approved window, redacted | it can help with what I'm working on without me copying text |

## 7. Requirements summary

Detailed, testable requirements live in the [SRS](../requirements/SRS.md). Headline requirements:

- Window-scoped capture with explicit OS consent.
- Text from accessibility APIs first, native OCR second, Tesseract last; all local.
- Local redaction before anything is sent, a summary of what was redacted, and user approval before every send (on by default, user-adjustable).
- Opt-in, user-located, retention-limited output storage.
- Per-app profiles, user prompts and suggestion frequency controls.
- Windows first, macOS second.

## 8. Success metrics

| Metric | Proposed target for v1.0 |
| --- | --- |
| Text accuracy on tested apps (Notepad, Word, VS Code, Chrome) | 98% or higher character accuracy |
| Redactor recall on the planted-PII test set | 95% or higher |
| Idle CPU while watching a static window | Under 3% |
| Time from typing pause to suggestion shown (local model on test PC) | Under 3 seconds |
| Suggestions dismissed without action | Tracked locally only; target under 50% |

## 9. Release plan

| Release | Contents |
| --- | --- |
| Screen Reader v0.1 | Windows CLI |
| Redactor v0.1 | CLI and library |
| AI Router v0.1 | CLI and library |
| Co-pilot CLI v0.1 | Combined suggestions in the terminal |
| Voice v0.1 | Read-aloud and dictation |
| Windows app 1.0 | Free desktop app, signed installer |
| macOS 1.0 | Port of all of the above |

## 10. Distribution and licensing

- Sub-projects and Co-pilot CLI: open source under Apache 2.0 (see ADR-0006).
- Desktop app: free, closed source.
- Enterprise tier: paid, later, with extra features (admin policy, managed deployment, audit logs).

## 11. Risks and open questions

| Item | Notes |
| --- | --- |
| Apps with poor accessibility text | OCR fallback; publish a compatibility list |
| Suggestion quality varies by backend | Per-profile prompts; recommend models per use case |
| Employee-monitoring law for enterprise | Review before an enterprise tier |
