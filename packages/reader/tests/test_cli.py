import pytest

from sidelight_reader import __version__
from sidelight_reader.cli import main


def test_help_runs(capsys: pytest.CaptureFixture[str]) -> None:
    assert main([]) == 0
    assert "usage: sidelight-reader" in capsys.readouterr().out


def test_version(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit):
        main(["--version"])
    assert __version__ in capsys.readouterr().out
