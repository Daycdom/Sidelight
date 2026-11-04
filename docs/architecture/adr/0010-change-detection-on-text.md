# ADR-0010: Detect changes on text, not pixels

- Status: Accepted
- Date: 2026-11-04
- Deciders: Dominic

## Context and problem

The original concept used a tiny perceptual image hash to decide when to run OCR. A small typed word rarely changes a coarse hash, so text changes would be missed.

## Decision

With accessibility text, compare text directly. With OCR, use the capture API's dirty-region information or a frame difference to decide when to OCR, then compare the resulting text. Emit events only on text change (SR-06).

## Consequences

- Good: never misses typing; avoids duplicate AI calls.
- Bad: OCR noise can create false changes; mitigate with a small similarity threshold.
