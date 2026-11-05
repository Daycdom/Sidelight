# Open Decisions (WIP)

| Field | Value |
| --- | --- |
| Status | WIP, for Dominic to review |
| Last updated | 2026-11-05 |

Each item below has a working answer so development isn't blocked. The docs already follow these answers; any of them can change after review.

| # | Question | Working answer (WIP) | Recorded in | Decide by |
| --- | --- | --- | --- | --- |
| 1 | Support Windows 10? | Best effort: Windows 11 is the target; run the Reader spikes once on a Windows 10 22H2 VM and only fix cheap issues | SRS §2.2, Reader spec §2 | Phase 7 (Windows release) |
| 2 | How is the context store encrypted? | App-level encryption with `cryptography` (AES-GCM per entry, key in the OS credential store) instead of SQLCipher, which is a native library that is harder to package and sandbox | ADR-0019 (Proposed) | Start of phase 5 (Co-pilot) |
| 3 | What are the v1.0 success targets? | Treat current PRD numbers as placeholders. Replace them with measured baselines from spikes S5/S6 and the Redactor benchmark, then set targets from those | PRD §8 | End of phase 2 |
| 4 | Is "Sidelight" safe to use as a name? | Keep as working name. Before the first public release with branding: search USPTO (classes 9 and 42) and WIPO Global Brand Database, including look-alikes such as "Slidelight"; consider a lawyer's knockout search | README, product-decisions | Before the Windows app 1.0 |
| 5 | Accept the Agent Bridge? | Deferred, not a priority | ADR-0011 | Later phase |
| 6 | Paid edition pricing | One-time purchase and/or cheap subscription, QoL features only, offline signed keys with one-time activation | ADR-0006 | Phase 7 |
| 7 | What context is missing from the Reader diagrams? | Draft diagrams are in the spec; Dominic to note what feels missing (for example timings, event names or the user-facing view) and the diagrams get a second pass | Reader spec §5.5 | Before the Reader build starts |
