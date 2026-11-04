# CLAUDE.md

All project instructions for AI assistants live in AGENTS.md, so Claude Code, Cursor and other tools share one source of truth.

@AGENTS.md

## Claude Code specifics

- Before finishing a task, run `uv run ruff check --fix`, `uv run ruff format`, `uv run mypy` and the affected tests.
- Do not add `Co-Authored-By` or other Claude attribution to commits or pull requests.
- For reader platform work, remember WSL cannot see Windows windows; say when a change needs testing from Windows.
