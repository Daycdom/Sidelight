# ADR-0009: Text-only AI input for v1

- Status: Accepted
- Date: 2026-11-04
- Deciders: Dominic

## Context and problem

Sending screenshots to vision models costs far more per call and exposes everything visible, including content redaction cannot see.

## Decision

v1 sends only redacted text to AI backends. Image input may be added later as an explicit opt-in.

## Consequences

- Good: lower cost, stronger privacy, simpler pipeline.
- Bad: no help with visual content (charts, images, games) until image input is added.
