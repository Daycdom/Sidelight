"""Command-line entry point for sidelight-reader."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from sidelight_reader import __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sidelight-reader",
        description="Turns an approved app window into live text, on-device.",
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
