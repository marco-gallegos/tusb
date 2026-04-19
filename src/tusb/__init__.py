"""tusb - TUI for managing USB devices on Linux."""

import tomllib
from importlib import metadata
from pathlib import Path


def get_version() -> str:
    """Get version from metadata (PyPI) or pyproject.toml fallback."""
    try:
        return metadata.version("tusb")
    except metadata.PackageNotFoundError:
        pass

    try:
        pyproject = Path(__file__).parent.parent / "pyproject.toml"
        with open(pyproject, "rb") as f:
            return tomllib.load(f)["project"]["version"]
    except (ImportError, FileNotFoundError, KeyError):
        return "0.3.0"
