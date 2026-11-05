# ADR-0016: Contain and catch memory leaks

- Status: Accepted
- Date: 2026-11-05
- Deciders: Dominic

## Context and problem

Sidelight runs for hours. Its riskiest code for leaks is native: UI Automation COM objects, WinRT capture frames and Direct3D surfaces, OCR, and ML models (spaCy, GLiNER, faster-whisper). Python's garbage collector doesn't see most of that memory, and a slow leak shows up only after hours. Screen text lingering in memory is also a privacy concern.

## Options considered

1. Rely on Python's garbage collector.
2. Run capture inside a container or virtual machine.
3. OS subprocesses with an OS-enforced memory cap, recycling and leak tests.

Option 2 doesn't work for this app: a container or VM can't see the host's windows, so UI Automation and window capture are impossible from inside one. Windows' own isolation features that do allow it (Job Objects for limits) are used instead. Stricter sandboxing of the worker (an AppContainer or low-integrity token) is worth a spike, but may block UI Automation, which Windows restricts for lower-privilege processes.

## Decision

Option 3.


1. **Isolate in OS subprocesses (the original concept's "multiprocessing sandbox").** Capture and OCR run in a worker process (already NFR-09); Redactor ML and Voice models run in their own worker processes too. Workers only exchange text over pipes.
2. **Hard memory cap from the OS.** On Windows each worker is placed in a Job Object with a per-process memory limit (via pywin32, PSF license), so the OS stops a runaway worker even if the supervisor misses it. macOS has no equivalent, so it relies on the supervisor (step 4).
3. **Reuse buffers.** Frame and OCR buffers are allocated once per window size and reused rather than created per frame.
4. **Recycle workers.** A supervisor restarts a worker after a set amount of work (for example 10,000 frames or 4 hours) or as soon as its memory passes a budget. A restart is invisible to the user apart from a short pause, and it also clears any screen text the worker held.
5. **Watch memory.** The supervisor samples each process's memory with `psutil` (BSD) every 30 seconds and logs numbers only (never content). Steady growth triggers an early recycle and a warning in the log.
6. **Bound everything.** Every queue, buffer, cache and history has a maximum size. No unbounded lists of events, frames or suggestions.
7. **Release native objects explicitly.** COM and WinRT objects are released in `finally` blocks or context managers (frames closed, frame pools recreated on window resize, COM uninitialized per thread). Platform adapters must document who owns each native object.
8. **Test for leaks.** Unit tests use `tracemalloc` to check that repeated reads don't grow Python memory; a soak test watches a changing window for 1 hour (8 hours before each release) and fails if memory grows past the budget. `memray` (Apache 2.0) can be used for deeper profiling on Linux and macOS; on Windows use `tracemalloc` and `psutil`.

## Consequences

- Good: a leak can't crash the app or slowly eat the machine; it is caught in testing and contained in production.
- Bad: more processes mean more baseline memory (each Python worker costs tens of MB) and a small restart pause; the supervisor is extra code.
- Follow-ups: NFR-19 to NFR-21, PF-04 and PF-05; Reader spec §5.3 adds recycling.
