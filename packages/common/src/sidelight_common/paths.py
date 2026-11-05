"""Standard per-user folders for settings and app data.

Everything here is machine-local (ADR-0014): on Windows this is %LOCALAPPDATA%, never the
roaming profile, so the context store, caches and settings don't follow the user to other PCs.
"""

from __future__ import annotations

from pathlib import Path

from platformdirs import user_config_path, user_data_path

APP_NAME = "Sidelight"


def config_dir() -> Path:
    return user_config_path(APP_NAME, appauthor=False, roaming=False)


def data_dir() -> Path:
    return user_data_path(APP_NAME, appauthor=False, roaming=False)
