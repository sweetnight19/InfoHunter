"""Application settings and secret lookup in one place."""

from dataclasses import dataclass
import os
from typing import Mapping


API_KEYS = {
    "HIBP_API_KEY": "Have I Been Pwned",
    "BREACHDIRECTORY_API_KEY": "BreachDirectory",
    "INTELX_KEY": "Intelligence X",
    "SHODAN_API_KEY": "Shodan",
    "VT_API_KEY": "VirusTotal",
    "HUNTER_API_KEY": "Hunter.io",
}


@dataclass(frozen=True)
class Settings:
    """Environment-backed settings; secret values are never included in repr."""

    _api_keys: Mapping[str, str]

    @classmethod
    def from_environment(cls, environ=None) -> "Settings":
        environment = os.environ if environ is None else environ
        return cls({
            name: str(environment.get(name, "")).strip()
            for name in API_KEYS
        })

    def api_key(self, name: str) -> str | None:
        if name not in API_KEYS:
            raise KeyError(f"Unknown API key setting: {name}")
        return self._api_keys.get(name) or None

    def api_key_status(self) -> list[dict[str, str]]:
        return [
            {
                "Servicio": label,
                "Estado": "Configurada" if self._api_keys.get(name) else "No configurada",
            }
            for name, label in API_KEYS.items()
        ]


def get_api_key(name: str) -> str | None:
    """Read one known provider secret without caching environment state."""
    return Settings.from_environment().api_key(name)
