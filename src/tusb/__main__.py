"""Entry point for tusb package."""

import click

from tusb.app import TusbApp
from tusb.config import Config


@click.command()
@click.option(
    "--refresh-interval",
    type=int,
    default=None,
    help="Auto-refresh interval in seconds (default: 30)",
)
@click.option(
    "--mount-dir",
    type=click.Path(),
    default=None,
    help="Base mount directory (default: /mnt)",
)
@click.option(
    "--config",
    type=click.Path(),
    default=None,
    help="Path to config file",
)
def main(refresh_interval: int | None, mount_dir: str | None, config: str | None) -> None:
    """TUI for managing USB devices on Linux."""
    cfg = Config.load(refresh_interval, mount_dir, config)
    app = TusbApp(cfg)
    app.run()


if __name__ == "__main__":
    main()
