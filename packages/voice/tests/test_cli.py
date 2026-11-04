import pytest

from sidelight_voice import __version__
from sidelight_voice.cli import main


def test_help_runs(capsys: pytest.CaptureFixture[str]) -> None:
    assert main([]) == 0
    assert "usage: sidelight-voice" in capsys.readouterr().out


def test_version(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit):
        main(["--version"])
    assert __version__ in capsys.readouterr().out
