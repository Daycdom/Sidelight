# Glossary

| Term | Meaning |
| --- | --- |
| Approval | The user's OK before any text is sent anywhere (ADR-0012) |
| Backend | An AI provider: cloud (Anthropic, OpenAI), self-hosted (Ollama, vLLM) or on-device |
| Broker | The small unsandboxed process that reads windows; every other worker is sandboxed (ADR-0017) |
| Context store | Encrypted local database of per-file context and the redaction cache |
| Destination | Anywhere text could be sent: a backend or, later, an agent |
| HMAC key | A keyed hash used to look up cached redactions without storing originals |
| MCP | Model Context Protocol, the open standard agents use to call tools (Agent Bridge, ADR-0011) |
| OCR | Optical character recognition: turning pixels into text |
| Profile | Saved settings tied to one or more apps |
| Recycling | Restarting a worker process after a work limit or memory budget (ADR-0016) |
| Redaction | Masking sensitive data before text leaves Sidelight |
| Source | A way to get text from a window: UI Automation, Windows OCR, Tesseract |
| Spike | A small throwaway experiment that proves an API or approach before building on it |
| Target window | The one window the user approved for reading |
| UIA | UI Automation, Windows' accessibility API |
| Worker | A child process that does one job (capture, OCR, redaction, voice) |
