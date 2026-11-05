# ADR-0011: Offer screen text to other AI agents through a local MCP server

- Status: Proposed
- Date: 2026-11-05
- Deciders: Dominic

## Context and problem

Users already run AI agents and assistants: Hermes Agent, Claude Desktop and Claude Code, Cursor, VS Code, and agent frameworks. Those tools can't see what the user is working on in other apps. Sidelight already turns one approved window into redacted text, so it could give these agents that context. Each agent has its own plugin system, so a per-agent integration would not scale for a solo developer.

## Options considered

1. No agent integration.
2. A custom plugin per agent.
3. One local server speaking the Model Context Protocol (MCP), the open standard most agents and assistants support.
4. A local HTTP API.

## Decision

Option 3, as a new standalone package `sidelight-bridge` (CLI `sidelight-bridge`), built on Screen Reader and Redactor only. It does not need Co-pilot or AI Router, so it can ship right after Redactor v0.1.

Rules:

- **Read-only.** Tools and resources only return text. Sidelight never acts on the user's machine for an agent.
- **The user approves the window, not the agent.** The window is chosen when the bridge starts (or in the desktop app). Agents cannot list or switch windows.
- **Always redacted.** Sidelight can't know where an agent sends text, so Redactor runs on every result and can't be turned off in the bridge.
- **Local transport only.** stdio (the agent launches the bridge as a child process). No network port in v0.1 (NFR-04).
- **Visible.** The capture indicator shows while an agent is connected, and the bridge logs each read (time, tool, character count, never content).
- **Untrusted content.** Results are marked as untrusted screen content, so agents treat them as data (T-06).
- **Approval.** Each read needs the user's approval by default, with the redaction summary shown, following ADR-0012. A per-minute read limit applies too.

## Consequences

- Good: one integration works with every MCP-capable agent; useful on its own; reuses existing packages; the official `mcp` Python SDK is MIT.
- Bad: once text reaches an agent, that agent's own privacy and tool behavior apply. Sidelight's promise ends at the bridge boundary and the docs must say so plainly. Screen text can try to steer an agent that has its own tools (prompt injection); Sidelight can mark it as data but can't control the agent.
- Follow-ups: SRS section 3.7 (AG-), threats T-17 and T-18, a design spec before building, and setup notes for common agents.
