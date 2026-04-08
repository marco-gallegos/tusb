"""Device scanner using lsblk."""

import json
import subprocess

from tusb.models import Device, DeviceList


def scan_devices() -> DeviceList:
    """Scan for devices using lsblk."""
    try:
        result = subprocess.run(
            [
                "lsblk",
                "-J",
                "-o",
                "NAME,TYPE,MOUNTPOINT,FSTYPE,SIZE,LABEL,UUID,PARTTYPE",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        data = json.loads(result.stdout)
    except subprocess.CalledProcessError, json.JSONDecodeError, FileNotFoundError:
        return DeviceList(devices=[])

    devices = []
    for block in data.get("blockdevices", []):
        devices.extend(_extract_partitions(block))

    return DeviceList(devices=devices)


def _extract_partitions(block: dict) -> list[Device]:
    """Recursively extract partitions from block device."""
    devices = []
    block_type = block.get("type")

    if block_type == "part":
        devices.append(
            Device(
                name=block.get("name", ""),
                mount_point=block.get("mountpoint"),
                fstype=block.get("fstype"),
                size=block.get("size", ""),
                label=block.get("label"),
                uuid=block.get("uuid"),
                parttype=block.get("parttype"),
            )
        )
    elif block_type == "disk" and "children" in block:
        for child in block.get("children", []):
            devices.extend(_extract_partitions(child))

    return devices
