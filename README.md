# Sidelight

Privacy-first desktop assistant that reads the window you choose, removes sensitive data on your device, and gives real-time suggestions from the AI you pick: Claude, ChatGPT, a self-hosted Ollama server, or an on-device model.

> Status: pre-alpha, in planning. Windows first, macOS next. "Sidelight" is a working name pending a trademark check.

## Packages

| Package | What it does | Use it alone? |
| --- | --- | --- |
| `sidelight-reader` | Turns an approved window into live text | Yes, CLI and library |
| `sidelight-redact` | Finds and masks sensitive data, fully on-device | Yes, CLI and library |
| `sidelight-router` | One interface to Claude, ChatGPT and Ollama with limits and spend caps | Yes, CLI and library |
| `sidelight-voice` | Local read-aloud and push-to-talk dictation | Yes, CLI and library |
| `sidelight-copilot` | Combines the above into live suggestions | CLI (`sidelight`) |
| `sidelight-common` | Shared paths, settings and output saving | Internal |

The free desktop app (closed source) is built on these packages.

## Privacy in one paragraph

Only the one window you approve is read. Images are discarded right after text extraction. Text is redacted before it goes anywhere, you're shown what was redacted, and nothing is sent until you approve it (on by default; you choose when to be asked). It only goes to the backend you chose. Nothing is saved unless you turn saving on. No telemetry. Details: [privacy](docs/security/privacy.md), [threat model](docs/security/threat-model.md).

## Getting started

See [developer setup](docs/process/dev-setup.md). On Windows: `powershell -ExecutionPolicy Bypass -File scripts\setup-windows.ps1`.

## Documentation

See [docs/README.md](docs/README.md).

## Contributing and security

[CONTRIBUTING.md](CONTRIBUTING.md) · [SECURITY.md](SECURITY.md) · [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

## License

Apache License 2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE). The desktop app is separate and closed source.
