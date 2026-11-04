# ADR-0003: Write all backend code in Python

- Status: Accepted
- Date: 2026-11-04
- Deciders: Dominic

## Context and problem

Capture, OCR, ML redaction, AI calls and voice all need a backend language with strong OS bindings and ML libraries.

## Decision

Python 3.12+ for every package. OS APIs are reached through `winrt` / `comtypes` / `uiautomation` on Windows and PyObjC on macOS.

## Consequences

- Good: best ML ecosystem (spaCy, Presidio, faster-whisper); developer's preferred language.
- Bad: packaging native dependencies with PyInstaller needs care; Python is slower for tight loops, mitigated by native OS APIs doing the heavy work.
