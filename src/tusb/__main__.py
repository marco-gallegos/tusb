"""Entry point for tusb package."""

import os
import shutil
import subprocess
import sys

import click

from tusb.app import TusbApp
from tusb.config import Config


def _check_compatibility() -> None:
    if sys.platform != "linux":
        click.echo(f"Error: tusb only runs on Linux (detected: {sys.platform})", err=True)
        sys.exit(1)

    if not shutil.which("lsblk"):
        click.echo("Error: lsblk not found. Install util-linux (e.g., sudo apt install util-linux)", err=True)
        sys.exit(1)

    if os.geteuid() == 0:
        click.echo("Error: Do not run tusb as root. Use a regular user account.", err=True)
        sys.exit(1)

    result = subprocess.run(["groups"], capture_output=True, text=True)
    if "sudo" not in result.stdout and "wheel" not in result.stdout:
        click.echo("Warning: User not in sudo/wheel group. Mount operations may fail.", err=True)


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
    _check_compatibility()
    cfg = Config.load(refresh_interval, mount_dir, config)
    app = TusbApp(cfg)
    app.run()


if __name__ == "__main__":
    main()
