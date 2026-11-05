# ADR-0014: Keep Sidelight's own data on this machine only

- Status: Accepted
- Date: 2026-11-05
- Deciders: Dominic

## Context and problem

Privacy comes first in every decision. Sidelight keeps a context store, a redaction cache, settings and logs. On Windows the roaming profile, folder redirection and OneDrive can copy app data to other machines or the cloud; on macOS iCloud Drive and backups can do the same. Users also pick their own folder for saved output, which may be a synced folder.

## Decision

1. **App data is machine-local.** The context store, redaction cache, settings, profiles and logs live in the local, non-roaming app data folder (`%LOCALAPPDATA%\Sidelight` on Windows, `~/Library/Application Support/Sidelight` on macOS), never in Documents or a roaming profile.
2. **Saved output is the user's choice, with a warning.** If the folder the user picks for saved output is inside a known sync or cloud folder (OneDrive, Dropbox, Google Drive, iCloud Drive), Sidelight warns that files will leave the device and asks for confirmation. The default suggested folder is local.
3. **Keys stay in the OS credential store**, which is device-local by default.
4. **Privacy first.** When a design choice trades privacy against convenience or speed, privacy wins unless the user explicitly opts out of that specific protection.

## Consequences

- Good: nothing Sidelight stores follows the user to the cloud or another PC without them choosing it.
- Bad: context and cache don't carry over to a second PC, and a reinstall or new machine starts fresh (the saved-file backup in ADR-0013 helps if the user saves output).
- Follow-ups: NFR-14, NFR-15; sync-folder detection in `sidelight-common`; macOS backup exclusion to be decided in phase 8.
