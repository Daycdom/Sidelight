# ADR-0012: Redact, show, then ask before anything is sent

- Status: Accepted
- Date: 2026-11-05
- Deciders: Dominic

## Context and problem

Sidelight sends screen text to AI backends (cloud, home lab, on-device server) and, if the Agent Bridge is used, to other agents. Redaction is probabilistic and the user is the only one who knows whether a given piece of text is fine to share. The privacy promise should not rely on redaction alone.

## Decision

Every outbound send follows the same three steps, in this order:

1. **Redact.** All text is redacted before it leaves Sidelight, for every destination: cloud, self-hosted, on-device server, or agent. This replaces ADR-0007's option to turn redaction off for local backends.
2. **Inform.** The user sees what was redacted: a summary of types and counts (for example "2 emails, 1 API key") and the outgoing text with placeholders highlighted. Original values are shown only on the user's screen, never stored or logged.
3. **Approve.** Nothing is sent until the user approves it. Approval is **required by default** (opt-in to needing approval). The user controls when approval is needed, per profile and per destination:
   - **Every send** (default)
   - **Once per session** for this window and destination
   - **Only when something was redacted**
   - **Never ask** (the user turns approval off; the redaction summary is still shown alongside the result)

   Denying a send discards it. The user can edit the outgoing text or allow-list a redacted term before approving.

The same flow applies in the CLIs (a terminal prompt showing the summary and redacted text, `y/n/e`) and in the desktop app (an approval card in the suggestions panel).

## Consequences

- Good: the user sees and controls every send; redaction mistakes are caught before they leave; consistent rule across Co-pilot, CLIs and Agent Bridge.
- Bad: automatic triggers (typing pause, every N words) prompt for each suggestion under the default, which may feel slow; users who want hands-free suggestions must relax approval for that profile. Redaction now always adds latency, even for local backends.
- Follow-ups: SRS CP-01, CP-11 to CP-13, UI-08, AG-07; privacy test PT-07; amend ADR-0007 and ADR-0011.
