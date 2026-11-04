# Documentation

| Area | Document | Answers |
| --- | --- | --- |
| Product | [PRD](product/PRD.md) | Why we're building this, for whom, and what success means |
| Product | [Roadmap](product/roadmap.md) | What ships in which phase |
| Requirements | [SRS](requirements/SRS.md) | Every testable requirement, with IDs and traceability |
| Architecture | [Architecture](architecture/architecture.md) | How the parts fit, data flows, process model |
| Architecture | [ADRs](architecture/adr/README.md) | Why each major decision was made |
| Security | [Threat model](security/threat-model.md) | What could go wrong and how it's prevented |
| Security | [Privacy and data handling](security/privacy.md) | What data exists, where, for how long |
| Quality | [Test plan](quality/test-plan.md) | How each release is verified |
| Process | [Development and release process](process/release-process.md) | Versioning, branching, CI, releasing |
| Process | [Developer setup](process/dev-setup.md) | Getting a working dev environment |

## Keeping docs current

- Docs live next to the code and change in the same pull request as the behavior they describe.
- Requirement IDs and ADR numbers are permanent.
- Each document has a status table at the top; bump "Last updated" when you edit it.
