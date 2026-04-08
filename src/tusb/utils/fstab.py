"""fstab line generator."""

from pathlib import Path

from tusb.models import Device


def generate_fstab_line(device: Device, mount_dir: str) -> str:
    """Generate an fstab automount line for the device."""
    if device.uuid is None:
        return "# Error: No UUID available for device"

    mount_point = str(Path(mount_dir) / device.get_mount_dir_name())
    fstype = device.fstype or "auto"

    return f"UUID={device.uuid}\t{mount_point}\t{fstype}\tdefaults,noauto,nofail\t0 0"
