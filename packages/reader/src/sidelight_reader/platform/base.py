"""Interfaces every platform adapter implements (see ADR-0004 and SRS SR-01 to SR-08)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class WindowInfo:
    """A visible top-level window the user can choose to watch."""

    handle: int
    title: str
    process_name: str


@dataclass(frozen=True, slots=True)
class TextSnapshot:
    """Text read from a window at one moment."""

    text: str
    source: str  # "accessibility", "native-ocr" or "tesseract"
    caret_offset: int | None = None


class WindowLister(Protocol):
    def list_windows(self) -> list[WindowInfo]: ...


class TextSource(Protocol):
    """Reads text from one window. Returns None when this source cannot read it."""

    name: str

    def read(self, window: WindowInfo) -> TextSnapshot | None: ...


class FrameCapture(Protocol):
    """Captures pixels of exactly one window (never the whole screen)."""

    def capture(self, window: WindowInfo) -> bytes: ...


class OcrEngine(Protocol):
    def recognize(self, frame: bytes, width: int, height: int) -> str: ...
