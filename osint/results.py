"""Stable, UI-independent result contract for individual OSINT sources."""

from dataclasses import dataclass
from enum import Enum
from typing import Any


class SourceState(str, Enum):
    SUCCESS = "success"
    EMPTY = "empty"
    PARTIAL = "partial"
    ERROR = "error"
    NOT_CONFIGURED = "not_configured"
    UNAVAILABLE = "unavailable"


@dataclass(frozen=True)
class SourceResult:
    """Result envelope that preserves legacy values while exposing a stable state."""

    source: str
    state: SourceState
    value: Any
    message: str | None = None

    @classmethod
    def from_value(cls, source: str, value: Any) -> "SourceResult":
        if isinstance(value, cls):
            return cls(source, value.state, value.value, value.message)

        if isinstance(value, dict) and value.get("error"):
            message = str(value["error"])
            lowered = message.casefold()
            if "not configured" in lowered or "not set" in lowered:
                state = SourceState.NOT_CONFIGURED
            elif "not installed" in lowered or "not on path" in lowered:
                state = SourceState.UNAVAILABLE
            else:
                state = SourceState.ERROR
            return cls(source, state, value, message)

        if isinstance(value, (list, tuple, set)):
            items = list(value)
            errors = [
                str(item) for item in items
                if str(item).casefold().startswith("error running")
            ]
            if errors:
                state = SourceState.PARTIAL if len(errors) < len(items) else SourceState.ERROR
                return cls(source, state, value, "; ".join(errors))
            return cls(source, SourceState.SUCCESS if items else SourceState.EMPTY, value)

        if value is None or value == "":
            return cls(source, SourceState.EMPTY, value)
        return cls(source, SourceState.SUCCESS, value)

    @classmethod
    def from_exception(cls, source: str, error: Exception) -> "SourceResult":
        message = f"Unexpected source failure ({type(error).__name__})."
        return cls(
            source=source,
            state=SourceState.ERROR,
            value={"error": message},
            message=message,
        )

    def to_legacy(self) -> Any:
        """Return the original analyzer payload for existing CLI/PDF consumers."""
        return self.value

    @property
    def has_findings(self) -> bool:
        if self.state in {
            SourceState.ERROR,
            SourceState.NOT_CONFIGURED,
            SourceState.UNAVAILABLE,
            SourceState.EMPTY,
        }:
            return False
        if isinstance(self.value, dict):
            if "found" in self.value:
                return bool(self.value["found"])
            return any(
                bool(value) for key, value in self.value.items()
                if key not in {"error", "email", "username", "domain", "raw"}
            )
        if isinstance(self.value, (list, tuple, set)):
            return any(
                not str(item).casefold().startswith("error running")
                for item in self.value
            )
        return bool(self.value)
