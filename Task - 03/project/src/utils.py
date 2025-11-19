from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any, Dict

import yaml


def get_project_root() -> Path:
    """Return the absolute path to the project root directory."""
    return Path(__file__).resolve().parents[1]


def resolve_path(relative_path: str | Path) -> Path:
    """Resolve a path relative to the project root."""
    path = Path(relative_path) if isinstance(relative_path, str) else relative_path
    if path.is_absolute():
        return path
    return get_project_root() / path


@lru_cache()
def load_config() -> Dict[str, Any]:
    """Load the YAML configuration file once and cache the result."""
    config_path = get_project_root() / "config.yaml"
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found at {config_path}")
    with config_path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def ensure_directory(path: str | Path) -> Path:
    """Ensure the directory exists and return the path."""
    directory = resolve_path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def get_path_from_config(*keys: str) -> Path:
    """Retrieve a filesystem path from the nested configuration keys."""
    config = load_config()
    node: Any = config
    for key in keys:
        if key not in node:
            raise KeyError(f"Configuration key '{'.'.join(keys)}' not found")
        node = node[key]
    return resolve_path(str(node))
