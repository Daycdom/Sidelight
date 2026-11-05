# ADR-0017: A small unsandboxed broker reads windows; everything else runs sandboxed

- Status: Accepted (sandbox switch-on gated by a phase 7 spike)
- Date: 2026-11-05
- Deciders: Dominic

## Context and problem

ADR-0016 splits the app into worker processes to contain memory leaks. The same split can contain security bugs: a malicious model file, a crafted document that breaks OCR, or a prompt-injection bug in the router. Only reading other windows needs access to the desktop. Windows blocks lower-privilege processes from using UI Automation on normal apps (User Interface Privilege Isolation), so the window-reading code itself can't be sandboxed.

## Options considered

1. Plain worker processes, no sandbox.
2. Sandbox everything, including window reading. Breaks UI Automation.
3. Broker model, as browsers use: one small unsandboxed broker for window access, every other worker sandboxed with only the permissions it needs.

## Decision

Option 3.

| Process | Access | Sandbox |
| --- | --- | --- |
| Broker: list windows, UI Automation, window capture | Desktop | None, normal user privileges, kept minimal |
| OCR | Pixels passed in | Yes, no network, no files |
| Redactor, context store | Text passed in, own data folder | Yes, no network |
| AI Router | Network to the user's chosen backend | Yes, network allowed only here |
| Voice | Microphone and speakers | Yes, those devices only |
| UI | WebView2 | Already sandboxed by WebView2 |

- **Windows:** sandboxed workers run in an AppContainer with only the capabilities listed. This doesn't require an MSIX package: an app can start AppContainer processes itself. It does need the app's files somewhere AppContainers may read, such as `C:\Program Files`, which a normal signed installer provides. Development runs from a venv, so the sandbox has a `--no-sandbox` developer switch that release builds don't offer.
- **macOS:** each helper gets its own App Sandbox entitlements; the broker holds the Screen Recording and Accessibility permissions.
- **Elevated windows:** neither the broker nor anything else can read windows running as administrator; Windows forbids this for normal processes. Sidelight won't run elevated. A signed build installed in Program Files could later request `uiAccess` (the mechanism screen readers use) if users need this; that needs its own ADR.

## Consequences

- Good: a compromised OCR, Redactor, router or voice process can't read files, see other windows, or reach the network (except the router, to the chosen backend).
- Bad: more setup (capabilities, file permissions, an installer); debugging sandboxed workers is harder; it only works fully in installed builds.
- Follow-ups: phase 7 spike (Python worker in an AppContainer: start-up, Windows OCR, model loading, pipes); NFR-22; threat model T-19; phase 8 macOS entitlements.
