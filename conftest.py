"""Skip platform-marked tests on other operating systems."""

from __future__ import annotations

import sys

import pytest

_PLATFORM_MARKS = {"windows": "win32", "macos": "darwin"}


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    for item in items:
        for mark, platform in _PLATFORM_MARKS.items():
            if mark in item.keywords and sys.platform != platform:
                item.add_marker(pytest.mark.skip(reason=f"needs {mark}"))
