"""Device mount/unmount operations."""

import os
import subprocess
from pathlib import Path

from tusb.models import Device, FormatType


def _get_mount_options(uid: int | None = None, gid: int | None = None) -> str:
    """Build mount options with uid/gid mapping for write permissions."""
    if uid is None:
        uid = os.getuid()
    if gid is None:
        gid = os.getgid()
    return f"uid={uid},gid={gid}"


def _run_sudo_cmd(cmd: list[str], password: str) -> subprocess.CompletedProcess:
    """Run a command with sudo using stdin for password."""
    return subprocess.run(
        ["sudo", "-S", "-n"] + cmd,
        input=f"{password}\n",
        capture_output=True,
        text=True,
    )


def mount_device(device: Device, mount_dir: str, password: str) -> tuple[bool, str]:
    """Mount a device to the specified directory."""
    mount_point = Path(mount_dir) / device.get_mount_dir_name()

    try:
        if device.uuid is None:
            return False, "No UUID available for device"

        mount_opts = _get_mount_options()
        cmd = [
            "sh",
            "-c",
            f"mkdir -p {str(mount_point)} && mount -o {mount_opts} /dev/{device.name} {str(mount_point)}",
        ]

        result = subprocess.run(
            ["sudo", "-S"] + cmd,
            input=f"{password}\n",
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            return False, f"Mount failed: {result.stderr.strip() or result.stdout.strip()}"

        return True, f"Mounted to {mount_point}"
    except PermissionError:
        return False, "Permission denied. Try running as root."
    except FileNotFoundError:
        return False, "mount command not found"
    except Exception as e:
        return False, f"Mount error: {e}"


def unmount_device(device: Device, password: str) -> tuple[bool, str]:
    """Unmount a device."""
    if not device.mount_point:
        return False, "Device is not mounted"

    try:
        result = subprocess.run(
            ["sudo", "-S", "umount", device.mount_point],
            input=f"{password}\n",
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


def format_device(device: Device, fs_type: FormatType, label: str | None, password: str) -> tuple[bool, str]:
    """Format a partition with the specified filesystem."""
    if not device.is_partition:
        return False, "Can only format partitions, not whole disks"

    if fs_type == FormatType.KEEP:
        return False, "Select a filesystem type to format"

    try:
        device_path = f"/dev/{device.name}"
        cmd = _build_format_cmd(device_path, fs_type, label)

        result = subprocess.run(
            ["sudo", "-S"] + cmd,
            input=f"{password}\n",
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            return False, f"Format failed: {result.stderr.strip() or result.stdout.strip()}"

        return True, f"Formatted {device.name} as {fs_type.value}"
    except FileNotFoundError:
        return False, f"mkfs.{fs_type.value} not found. Install corresponding package."
    except Exception as e:
        return False, f"Format error: {e}"


def _build_format_cmd(device_path: str, fs_type: FormatType, label: str | None) -> list[str]:
    """Build the format command based on filesystem type."""
    if fs_type == FormatType.FAT32:
        cmd = ["mkfs.fat", "-F", "32"]
        if label:
            cmd.extend(["-n", label[:11]])
        cmd.append(device_path)
    elif fs_type == FormatType.EXFAT:
        cmd = ["mkfs.exfat"]
        if label:
            cmd.extend(["-n", label])
        cmd.append(device_path)
    elif fs_type == FormatType.NTFS:
        cmd = ["mkfs.ntfs"]
        if label:
            cmd.extend(["--label", label[:128]])
        cmd.append(device_path)
    elif fs_type == FormatType.EXT4:
        cmd = ["mkfs.ext4"]
        if label:
            cmd.extend(["-L", label[:16]])
        cmd.append(device_path)
    else:
        cmd = [f"mkfs.{fs_type.value}", device_path]

    return cmd
