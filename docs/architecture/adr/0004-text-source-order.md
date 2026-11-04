# ADR-0004: Accessibility text first, native OCR second, Tesseract last

- Status: Accepted
- Date: 2026-11-04
- Deciders: Dominic

## Context and problem

The original concept ran Tesseract OCR on every frame. OCR is slower and less accurate than reading text directly, and Tesseract struggles with dark themes and colored UI.

## Options considered

1. Tesseract only.
2. OS-native OCR only (Windows.Media.Ocr, macOS Vision).
3. Accessibility API text (UI Automation, macOS AX), falling back to native OCR, then Tesseract.

## Decision

Option 3. All three run on-device and send nothing over the network. Accessibility text is exact and cheap and gives caret position. Native OCR handles apps that expose no text. Tesseract covers Linux and edge cases.

## Consequences

- Good: higher accuracy, lower CPU, smaller install on Windows and macOS.
- Bad: three code paths per platform to test.
- Follow-ups: keep a compatibility list of apps and which source works.
