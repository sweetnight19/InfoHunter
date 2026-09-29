"""Read-only availability checks for optional tools and local configuration."""
import shutil
from pathlib import Path

import yaml


OPTIONAL_TOOLS = {
    "Sherlock": "sherlock",
    "Maigret": "maigret",
    "Holehe": "holehe",
    "theHarvester": "theHarvester",
}


def optional_tool_status():
    """Return whether each optional executable can be resolved from PATH."""
    return {name: shutil.which(command) is not None
            for name, command in OPTIONAL_TOOLS.items()}


def harvester_key_file_status(paths=None):
    """Validate theHarvester YAML structure without returning or displaying secrets."""
    if paths is None:
        paths = (
            Path.home() / ".theHarvester" / "api-keys.yaml",
            Path("/etc/theHarvester/api-keys.yaml"),
            Path("/usr/local/etc/theHarvester/api-keys.yaml"),
        )
    config_path = next((Path(path) for path in paths if Path(path).is_file()), None)
    if config_path is None:
        return "missing"

    try:
        config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError):
        return "unreadable"
    except yaml.YAMLError:
        return "invalid_yaml"

    if not isinstance(config, dict) or not isinstance(config.get("apikeys"), dict):
        return "invalid_structure"
    return "valid"
