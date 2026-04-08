"""Device mount/unmount operations."""

import subprocess
from pathlib import Path

from tusb.models import Device


def mount_device(device: Device, mount_dir: str) -> tuple[bool, str]:
    """Mount a device to the specified directory."""
    mount_point = Path(mount_dir) / device.get_mount_dir_name()

    try:
        if device.uuid is None:
            return False, "No UUID available for device"

        mount_point.mkdir(parents=True, exist_ok=True)

        result = subprocess.run(
            ["mount", f"/dev/{device.name}", str(mount_point)],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            return False, f"Mount failed: {result.stderr}"

        return True, f"Mounted to {mount_point}"
    except PermissionError:
        return False, "Permission denied. Try running as root."
    except FileNotFoundError:
        return False, "mount command not found"
    except Exception as e:
        return False, f"Mount error: {e}"


def unmount_device(device: Device) -> tuple[bool, str]:
    """Unmount a device."""
    if not device.mount_point:
        return False, "Device is not mounted"

    try:
        result = subprocess.run(
            ["umount", device.mount_point],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            if "busy" in result.stderr.lower():
                return False, "Device is in use"
            return False, f"Unmount failed: {result.stderr}"

        mount_point = Path(device.mount_point)
        try:
            mount_point.rmdir()
        except OSError:
            pass

        return True, f"Unmounted from {device.mount_point}"
    except PermissionError:
        return False, "Permission denied. Try running as root."
    except FileNotFoundError:
        return False, "umount command not found"
    except Exception as e:
        return False, f"Unmount error: {e}"
