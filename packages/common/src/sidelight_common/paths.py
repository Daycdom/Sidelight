"""Standard per-user folders for settings and app data."""

from __future__ import annotations

from pathlib import Path

from platformdirs import user_config_path, user_data_path

APP_NAME = "Sidelight"


def config_dir() -> Path:
    return user_config_path(APP_NAME, appauthor=False)


def data_dir() -> Path:
    return user_data_path(APP_NAME, appauthor=False)
