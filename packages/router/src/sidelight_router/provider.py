"""The interface every AI backend adapter implements (SRS AR-01)."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class Message:
    role: str  # "system", "user" or "assistant"
    content: str


class Provider(Protocol):
    name: str

    def stream(self, messages: list[Message], model: str) -> Iterator[str]:
        """Yield response text chunks."""
        ...
