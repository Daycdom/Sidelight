# Test Plan: Sidelight

| Field | Value |
| --- | --- |
| Status | Draft |
| Version | 0.1 |
| Owner | Dominic |
| Last updated | 2026-11-04 |

## 1. Objectives

Show that each release meets its SRS requirements, keeps the privacy promise, and works on real apps.

## 2. Test levels

| Level | What | Tools | Runs |
| --- | --- | --- | --- |
| Unit | Pure logic: redaction rules, router limits, triggers, prompt builder, output saving | pytest, hypothesis | Every commit (CI) |
| Integration | Package boundaries with fakes: Co-pilot with fake Screen Reader and mocked AI providers | pytest, respx for HTTP mocks | Every commit (CI) |
| Platform | Real OS APIs: UI Automation, WGC, Windows OCR (later macOS) | pytest on Windows runner | Every PR to main |
| Replay | Saved text snapshots fed through Co-pilot to check suggestions and redaction end to end | fixtures in `tests/fixtures/` | Every PR |
| Redaction accuracy | Planted-PII test set; measures recall and precision per entity type | custom script | Every Redactor change; reported in PR |
| UI | Frontend components and api.ts contract | Vitest, Playwright against a stub bridge | Every PR touching `ui/` |
| Manual release check | Done-criteria from the build outline on clean Windows 10 and 11 machines | checklist below | Each release |

## 3. Privacy tests (must pass every release)

| ID | Check | Req |
| --- | --- | --- |
| PT-01 | Network monitor shows no traffic except the configured backend during a session | NFR-04 |
| PT-02 | No image files are created anywhere during a session | SR-07 |
| PT-03 | With saving off, no transcript, report or history files exist after a session | SR-09, CP-10 |
| PT-04 | Planted fake API keys and cards never appear in any request payload, cloud or local | CP-01 |
| PT-05 | Blocklisted app produces no capture events | CP-02 |
| PT-06 | Logs at default level contain no screen text | Threat T-13 |
| PT-07 | With default settings, no request reaches any backend or agent until the user approves it; denying sends nothing | CP-11 |
| PT-08 | The approval prompt lists every redaction made in the outgoing text | CP-13 |

## 4. Performance tests

| ID | Check | Target | Req |
| --- | --- | --- | --- |
| PF-01 | CPU while watching a static window for 10 minutes | Under 3% | NFR-01 |
| PF-02 | Accessibility text change to event | Under 500 ms | NFR-03 |
| PF-03 | Redactor on 2,000 characters | Under 200 ms | RD-08 |

## 5. Compatibility matrix (v1.0)

| App | Accessibility text | OCR fallback |
| --- | --- | --- |
| Notepad | To test | To test |
| Microsoft Word | To test | To test |
| VS Code | To test | To test |
| Chrome / Edge | To test | To test |
| Google Docs (browser) | To test | To test |

## 6. Entry and exit criteria

- Entry: feature merged to main, CI green.
- Exit for release: all M requirements for that release verified, all privacy tests pass, no open critical or high bugs.

## 7. Defect severity

| Severity | Definition | Release blocker? |
| --- | --- | --- |
| Critical | Privacy breach, data loss, crash on start | Yes |
| High | Core feature broken with no workaround | Yes |
| Medium | Feature broken with workaround | No |
| Low | Cosmetic | No |
