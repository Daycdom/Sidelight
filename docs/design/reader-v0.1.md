# Design Spec: Screen Reader v0.1 (Windows)

| Field | Value |
| --- | --- |
| Status | Draft |
| Version | 0.1 |
| Owner | Dominic |
| Package | `sidelight-reader` |
| Requirements | SR-01 to SR-12, NFR-01, NFR-03, NFR-04, NFR-09, NFR-11 |
| Last updated | 2026-11-04 |

## 1. Goal

Ship `sidelight-reader` 0.1: a standalone CLI and Python library that, on Windows 10/11, lists windows, lets the user pick one, and streams that window's text as change events. Text comes from UI Automation first and Windows OCR second, all on-device. Useful on its own (accessibility, transcripts, scripting) and the input for every later package.

## 2. Scope

**In v0.1**

- Windows only (Windows 10 1903+ for Graphics Capture; Windows 11 recommended).
- Window listing, single-window watch, one-shot read.
- Sources: UI Automation text (accessibility), Windows.Media.Ocr over Windows Graphics Capture frames.
- Change events on text, not pixels (ADR-0010).
- Caret and focused element when UI Automation provides them (SR-05).
- Optional transcripts to a user-chosen folder with retention (SR-09, SR-10).
- Capture loop in a child process (NFR-09, architecture §8).

**Not in v0.1**

- macOS (AX, ScreenCaptureKit, Vision) and Linux. The platform layer must make these easy to add.
- Tesseract fallback (planned for macOS/Linux phase; the source chain already allows it).
- Redaction (that's `sidelight-redact`), AI calls, UI.
- Reading multiple windows at once.

## 3. User-facing CLI

The CLI is `sidelight-reader`. (SR-11 is updated to these names.)

```text
sidelight-reader list-windows [--json]
sidelight-reader read  TARGET [--source auto|uia|ocr] [--json]
sidelight-reader watch TARGET [--source auto|uia|ocr] [--interval SECONDS]
                              [--format text|jsonl]
                              [--save DIR] [--save-format txt|md|jsonl] [--retention-days N]
sidelight-reader sources TARGET   # diagnostics: which sources can read this window
```

`TARGET` is one of `--handle 0x1A2B`, `--title "substring"` (must match exactly one window, else exit with the matches listed), or `--pick` (interactive numbered list).

| Command | Behavior |
| --- | --- |
| `list-windows` | Visible, non-cloaked, titled top-level windows: handle, process name, title. Excludes Sidelight's own windows. |
| `read` | One snapshot of the target's text, then exit. |
| `watch` | Prints an event each time the text changes. Stops on Ctrl+C or when the window closes (SR-08). Shows a one-line "watching <title>" banner on stderr so capture is always visible (T-12). |
| `sources` | Tries each source once and reports which worked, character count and time taken. Never prints the text itself. Feeds the app compatibility list. |

Defaults: `--source auto`, `--interval 0.5`, `--format text`. Saving is off unless `--save` is given. Exit codes: `0` ok, `1` usage error, `2` target not found or ambiguous, `3` no source could read the window, `4` window closed before the first read.

### Output format (`--format jsonl`, one event per line)

```json
{"v": 1, "type": "text", "seq": 3, "ts": "2026-11-04T12:00:01.250Z",
 "window": {"handle": 6699, "process": "notepad.exe", "title": "notes.txt - Notepad"},
 "source": "uia", "text": "full current text…",
 "caret": 120, "focus": {"control": "Document", "name": "Text editor"}}
{"v": 1, "type": "status", "seq": 4, "ts": "…", "status": "source-changed", "source": "ocr"}
{"v": 1, "type": "end", "seq": 5, "ts": "…", "reason": "window-closed"}
```

- `text` is always the full current text (simple for consumers; diffs can come later).
- `caret` and `focus` are `null` when unknown.
- `reason` is one of `window-closed`, `user-stopped`, `error`.
- `v` is the schema version; any breaking change bumps it and is noted in the changelog.

## 4. Python API

```python
from sidelight_reader import Reader, WatchOptions

reader = Reader()                       # picks the platform backend
win = reader.find(title="Notepad")      # -> WindowInfo (raises on 0 or >1 matches)
snap = reader.read(win)                 # -> TextSnapshot | None
for event in reader.watch(win, WatchOptions(interval=0.5)):
    ...                                 # TextChanged | StatusChanged | Ended
```

- `watch()` is a blocking iterator; `reader.stop()` (or breaking the loop) ends it cleanly.
- Events are frozen dataclasses mirroring the JSON above. `TextChanged.to_json()` produces exactly the JSONL line.
- An async wrapper (`awatch`) is added only when the copilot needs it.
- Existing protocols in `platform/base.py` stay: `WindowLister`, `TextSource`, `FrameCapture`, `OcrEngine`. Add `focus` to `TextSnapshot` and an `is_alive(window)` check to `WindowLister`.

## 5. Internal design

```text
sidelight_reader/
  __init__.py        Reader, WatchOptions, event types (public API)
  cli.py             argparse commands, output formatting
  events.py          TextChanged, StatusChanged, Ended
  watch.py           watch loop, change detection, source fallback
  worker.py          child-process host; sends events back over a pipe
  transcript.py      optional saving and retention (only used with --save)
  platform/
    base.py          protocols and data types (no OS imports)
    __init__.py      get_backend() -> lazy-imports the current OS module
    windows/
      windows.py     EnumWindows, process names, cloaked filter (ctypes)
      uia.py         UIAutomation TextSource (comtypes)
      capture.py     Windows Graphics Capture for one HWND (pywinrt)
      ocr.py         Windows.Media.Ocr engine (pywinrt)
    fake.py          scripted backend for tests and non-Windows dev
```

### 5.1 Source chain (ADR-0004)

`auto` tries sources in order and sticks with the first that returns non-empty text:

1. **UIA**: find the window's element, look for a `TextPattern` (documents, editors) or `ValuePattern` (inputs). Read `DocumentRange.GetText(max_chars)`; caret from the selection range when present. Cap at 200,000 characters per read.
2. **OCR**: capture the window's own pixels with Graphics Capture (works when partly covered; never captures other windows, SR-03), run `OcrEngine.TryCreateFromUserProfileLanguages()`, join lines.

If the current source fails three reads in a row, fall back to the next one and emit a `source-changed` status event. Re-try the better source every 30 seconds.

### 5.2 Change detection (ADR-0010, SR-06)

- UIA: poll at `interval`; emit when text or caret differs from the last emitted value. Subscribe to UIA `TextChanged` events if the spike shows they're reliable, keeping polling as a backstop.
- OCR: skip OCR when the frame is unchanged (Graphics Capture dirty regions, else a cheap frame difference). After OCR, emit only if the text's similarity to the last text is below 0.99 (filters OCR jitter).
- Target budgets: under 3% idle CPU on a static window (NFR-01), under 500 ms from typing to event with UIA (NFR-03).

### 5.3 Process model (NFR-09)

`watch` runs the capture loop in a child process (`multiprocessing`, spawn start method). Only events (text, never pixels) cross the pipe. If the child dies, the parent emits `end` with `reason: "error"` and a short non-content error message. `read` and `sources` can run in-process.

### 5.4 Privacy rules this package enforces

| Rule | How | Test |
| --- | --- | --- |
| Frames never touch disk (SR-07) | Frames are `memoryview`/bytes in the child only; released after OCR; no file APIs in `capture.py`/`ocr.py` | Test watches the temp and data folders during an OCR watch; nothing new appears. Lint check: no `open(`/`Path.write` in those modules |
| One window only (SR-02, SR-03) | `CreateForWindow(hwnd)` only; no monitor capture code exists | Unit test that the capture API is only called with the target handle |
| No network (NFR-04) | No network imports in the package | Test that blocks sockets during the full test run |
| No text in logs (T-13) | Logs record lengths, source names and timings only | Test captures logs during a watch and asserts the sample text never appears |
| Saving only on request (SR-09) | `transcript.py` is only constructed when `--save` is given | Test that a plain watch writes no files |

## 6. Dependencies

All Windows-only, declared with `; sys_platform == 'win32'` markers so the package installs anywhere.

| Need | Package | License | Notes |
| --- | --- | --- | --- |
| Win32 window listing | `ctypes` (stdlib) | PSF | `EnumWindows`, `GetWindowText`, `DwmGetWindowAttribute(DWMWA_CLOAKED)`, `QueryFullProcessImageName` |
| UI Automation | `comtypes` | MIT | Load `UIAutomationCore` type library; thin wrapper only |
| Graphics Capture + OCR | `winrt-Windows.Graphics.Capture`, `winrt-Windows.Media.Ocr`, related `winrt-*` (pywinrt) | MIT | Confirm in spike S4 that `CreateForWindow` interop works from Python; fallback below |
| Capture fallback | `windows-capture` | MIT | Only if pywinrt interop proves impractical |

No GPL/LGPL. Each new dependency gets a line in this table before it's added.

## 7. Spikes (do these first)

Small throwaway scripts in `packages/reader/spikes/` (not shipped) to prove each API works before building on it. Each ends with a short note in this section: works / doesn't, numbers, gotchas.

| ID | Question | Pass when |
| --- | --- | --- |
| S1 | Can `ctypes` list the same windows the taskbar shows (skip cloaked, tool and untitled windows)? | List matches Alt+Tab on your PC |
| S2 | What text does UIA give for Notepad, Word, VS Code, Chrome, Windows Terminal? | Table of app → text yes/no, caret yes/no, ms per read. Note Chromium/Electron apps may need accessibility switched on (e.g. VS Code "screen reader optimized" mode) |
| S3 | Are UIA `TextChanged` events reliable enough to replace polling? | Events fire for typing in at least Notepad and Word |
| S4 | Can Python capture one window with Graphics Capture, including when it's partly covered? | Frame of the target only, other windows absent; note whether the yellow capture border can be turned off (`IsBorderRequired`, Windows 11) |
| S5 | Windows OCR quality and speed on S4 frames (light and dark themes, code font) | Readable text; ms per frame on your PC |
| S6 | CPU cost of a 0.5 s watch loop on a static window | Under 3% (NFR-01) |
| S7 | Child process + pipe overhead | Event latency increase under 50 ms |

Results feed `docs/design/app-compatibility.md` (ADR-0004 follow-up).

## 8. Build order

1. Spikes S1 to S5; record results here.
2. `platform/fake.py`, events, watch loop and CLI against the fake backend (testable in WSL and CI on Linux).
3. Windows backend: listing (S1), UIA source (S2), capture + OCR (S4, S5).
4. Child process worker (S7), source fallback, transcripts and retention.
5. Privacy tests (§5.4), Windows CI job running `-m "not windows"` plus a manual run of `-m windows` on your PC.
6. Docs: package README with examples, changelog, SR-11 update. Tag `reader-v0.1.0`.

## 9. Definition of done

- All "M" requirements SR-01 to SR-12 met and traced in tests.
- Privacy tests in §5.4 pass.
- `sources` results recorded for at least five common apps.
- NFR-01 and NFR-03 measured on your PC and written in the changelog.
- README shows install, `list-windows`, `watch` and JSONL examples.

## 10. Open questions

1. Should `watch` emit full text each time (current plan) or diffs? Full text is simpler; revisit if large documents make it slow.
2. Should the yellow capture border stay on? It's a privacy signal (T-12); proposal: keep it on by default, allow turning it off.
3. Which OCR language: user profile languages (proposal) or a `--lang` option too?
