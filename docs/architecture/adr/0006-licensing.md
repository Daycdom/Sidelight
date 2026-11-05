# ADR-0006: Open-source packages, closed-source desktop app

- Status: Accepted
- Date: 2026-11-04
- Deciders: Dominic

## Context and problem

The command-line tools are the free, open-source version of Sidelight. The desktop app (graphical interface) is closed source and may be sold, possibly with a free tier. A paid enterprise tier may come later. (Updated 2026-11-05: the desktop app was originally planned as free.)

## Options considered

1. MIT: shortest, most permissive.
2. Apache 2.0: permissive, with an explicit patent grant and contribution terms.
3. A copyleft license (GPL): would require the closed app to be open if it links the packages. Rejected.

## Decision

Apache 2.0 for all open packages (LICENSE at the repo root, NOTICE alongside it). Its explicit patent grant reassures companies, which helps a future enterprise tier. The closed desktop app uses a proprietary EULA. Check every dependency's license is compatible (Tesseract is Apache 2.0 and spaCy is MIT; ML model weights have their own licenses per checkpoint and must be checked separately). Avoid GPL and LGPL dependencies (e.g. pystray and pynput are LGPL-3.0) so the closed app can bundle the packages without relinking obligations.

## Consequences

- Good: permissive license lets the closed, possibly paid app and enterprise tier reuse the packages.
- Paid licensing (decided 2026-11-05): a license key signed with the developer's private key (Ed25519) and verified on the device with a public key built into the app. Containing only an order ID, edition and an "updates until" date, no name or email.
- One-time activation: when a paid user first enters the key, the app makes a single, visible activation call. After that the app never contacts the license server again and works offline indefinitely. Users with no internet can activate from another device through the website and paste back an activation code. No check on launch.
- Models (possible, far future): a one-time purchase (works forever, with an "updates until" date) and a cheap subscription. A subscription license carries a `valid_until` date (renewal date plus a short grace period); the day after renewal the app makes one visible check and receives a fresh signed license. If the check fails, the app keeps working through the grace period, then only paid features stop; data, settings and free features always keep working. Offline users can import a renewed license from the website or the renewal email.
- Free vs paid: core usability is the same for everyone. Paid adds quality-of-life features only. Privacy and security features (redaction, approval before sending, sandboxing, local storage) are never paid-only.
- Bad: others may also build closed products on the packages.
