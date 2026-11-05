# Definition of Done

A change, issue or release is done when every line that applies is true.

## Every change

- [ ] Lint, format, mypy and the affected tests pass locally and in CI
- [ ] New behavior has tests; non-platform code stays at 80%+ coverage (NFR-12)
- [ ] Platform code that needs real OS APIs has `windows`/`macos`-marked tests and was run on that OS
- [ ] No privacy rule broken (AGENTS.md): no new network path, no images on disk, no screen text in logs, nothing sent without redaction and approval
- [ ] Docs updated in the same commit: SRS, design spec or ADR if behavior or a decision changed
- [ ] Changelog line under "Unreleased" for user-visible changes
- [ ] Conventional Commit message, no AI attribution

## Every spike

- [ ] Result written into the design spec (works or not, numbers, gotchas)
- [ ] Spike code kept out of the shipped package

## Every release

- [ ] All "M" requirements for the release verified (test plan exit criteria)
- [ ] Privacy tests PT-01 to PT-08 pass
- [ ] Performance numbers measured and recorded in the changelog
- [ ] Threat model reviewed for minor and major releases
- [ ] Tagged `<package>-v<version>`, GitHub release created, website page updated
