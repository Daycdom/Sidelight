# Architecture Decision Records

Decisions are recorded with [MADR](https://adr.github.io/madr/) (Markdown Architectural Decision Records). One file per decision, numbered, never deleted. A changed decision gets a new ADR that supersedes the old one.

| ADR | Title | Status | Date |
| --- | --- | --- | --- |
| [0001](0001-record-architecture-decisions.md) | Record architecture decisions | Accepted | 2026-11-04 |
| [0002](0002-pywebview-desktop-shell.md) | Use pywebview for the desktop shell | Accepted | 2026-11-04 |
| [0003](0003-python-backend.md) | Write all backend code in Python | Accepted | 2026-11-04 |
| [0004](0004-text-source-order.md) | Accessibility text first, native OCR second, Tesseract last | Accepted | 2026-11-04 |
| [0005](0005-standalone-subprojects-monorepo.md) | Standalone sub-projects in one monorepo | Accepted | 2026-11-04 |
| [0006](0006-licensing.md) | Open-source packages, closed-source desktop app | Accepted | 2026-11-04 |
| [0007](0007-local-first-redaction.md) | Local by default; redact before any cloud call | Accepted | 2026-11-04 |
| [0008](0008-opt-in-output-storage.md) | Output files are opt-in | Accepted | 2026-11-04 |
| [0009](0009-text-only-ai-input-v1.md) | Text-only AI input for v1 | Accepted | 2026-11-04 |
| [0010](0010-change-detection-on-text.md) | Detect changes on text, not pixels | Accepted | 2026-11-04 |
| [0011](0011-agent-bridge-mcp.md) | Offer screen text to other AI agents through a local MCP server | Proposed | 2026-11-05 |
| [0012](0012-approve-every-send.md) | Redact, show, then ask before anything is sent | Accepted | 2026-11-05 |
| [0013](0013-redaction-cache.md) | Redact ahead of time and reuse saved text files as the redaction cache | Accepted | 2026-11-05 |

New ADRs copy [template.md](template.md).
