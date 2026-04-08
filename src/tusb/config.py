"""Configuration management for tusb."""

from pathlib import Path

from pydantic import BaseModel


class Config(BaseModel):
    """Application configuration."""

    mount_dir: str = "/mnt"
    refresh_interval: int = 30
    config_file: str | None = None

    @classmethod
    def load(
        cls,
        refresh_interval: int | None = None,
        mount_dir: str | None = None,
        config_file: str | None = None,
    ) -> "Config":
        """Load configuration with precedence: CLI > config file > defaults."""
        defaults = cls()

        config_path = config_file or cls._get_default_config_path()
        file_config = cls._load_from_file(config_path) if config_path else None

        return cls(
            mount_dir=mount_dir or file_config.mount_dir if file_config else defaults.mount_dir,
            refresh_interval=refresh_interval or file_config.refresh_interval
            if file_config
            else defaults.refresh_interval,
            config_file=config_file,
        )

    @staticmethod
    def _get_default_config_path() -> Path | None:
        """Get default config file path."""
        xdg_config = Path.home() / ".config" / "tusb.toml"
        if xdg_config.exists():
            return xdg_config
        return None

    @staticmethod
    def _load_from_file(path: Path | str) -> "Config | None":
        """Load configuration from TOML file."""
        try:
            import tomllib

            with open(path, "rb") as f:
                data = tomllib.load(f)
        except ImportError, FileNotFoundError, ValueError:
            return None

        default_section = data.get("default", {})
        return Config(
            mount_dir=default_section.get("mount_dir", "/mnt"),
            refresh_interval=default_section.get("refresh_interval", 30),
            config_file=str(path),
        )
