"""Command-line entry point for sidelight-copilot."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from sidelight_copilot import __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sidelight",
        description="Live AI suggestions for the window you choose.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    parser.parse_args(argv)
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
