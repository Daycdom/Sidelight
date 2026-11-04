# ADR-0002: Use pywebview for the desktop shell

- Status: Accepted
- Date: 2026-11-04
- Deciders: Dominic

## Context and problem

The backend is Python. The UI should be a lightweight, modern web frontend. The original concept used Electron with a Python child process over a localhost WebSocket.

## Options considered

1. pywebview: Python hosts the OS web engine (WebView2 on Windows, WebKit on macOS) and exposes Python functions to JavaScript.
2. Tauri with a Python sidecar process.
3. Electron with a Python child process.

## Decision

pywebview. One language and one build. The built-in JS-to-Python bridge runs in-process, so there is no API port that another local process could connect to. (pywebview does start a localhost static-file server when the UI is loaded by relative path; load the bundled UI directly or enable its `ssl` option.) The shell itself adds tens of MB rather than the 150 MB or more of a bundled Chromium; the final size will be dominated by ML models.

## Consequences

- Good: simplest stack for a solo Python developer; smaller attack surface.
- Bad: tray, global hotkeys and auto-update need extra code: thin OS wrappers for tray and hotkeys (pystray and pynput are LGPL-3.0, see ADR-0006) and a custom updater.
- Follow-ups: all UI-to-Python calls go through `ui/src/api.ts` (UI-06) so the shell can be swapped for Tauri or Electron later by rewriting that file and the shell only.
