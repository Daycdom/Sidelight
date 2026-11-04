# ADR-0006: Open-source packages, closed-source desktop app

- Status: Accepted
- Date: 2026-11-04
- Deciders: Dominic

## Context and problem

The command-line tools should be open source. The desktop app is free but closed source. A paid enterprise tier may come later.

## Options considered

1. MIT: shortest, most permissive.
2. Apache 2.0: permissive, with an explicit patent grant and contribution terms.
3. A copyleft license (GPL): would require the closed app to be open if it links the packages. Rejected.

## Decision

Apache 2.0 for all open packages (LICENSE at the repo root, NOTICE alongside it). Its explicit patent grant reassures companies, which helps a future enterprise tier. The closed desktop app uses a proprietary EULA. Check every dependency's license is compatible (Tesseract and spaCy are Apache 2.0 / MIT; verify models separately).

## Consequences

- Good: permissive license lets the closed app and enterprise tier reuse the packages.
- Bad: others may also build closed products on the packages.
