import sys

import pytest


@pytest.mark.windows
def test_windows_mark_only_runs_on_windows() -> None:
    assert sys.platform == "win32"


@pytest.mark.macos
def test_macos_mark_only_runs_on_macos() -> None:
    assert sys.platform == "darwin"
