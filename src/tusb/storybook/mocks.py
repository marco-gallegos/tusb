"""Hardcoded mock data for storybook widgets."""

from tusb.models import Device

MOCK_DEVICES = [
    Device(
        name="sda1",
        mount_point=None,
        fstype="ext4",
        size="50G",
        label="Linux",
        uuid="a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        parttype="0x83",
        is_partition=True,
    ),
    Device(
        name="sdb1",
        mount_point="/mnt/usb",
        fstype="vfat",
        size="32G",
        label="USB Drive",
        uuid="B2C3D4E5F6",
        parttype="0xc",
        is_partition=True,
    ),
    Device(
        name="sdc1",
        mount_point="/mnt/backup",
        fstype="ntfs",
        size="500G",
        label="Backup",
        uuid="1234567890ABCDEF",
        parttype="0x07",
        is_partition=True,
    ),
]

MOCK_DEVICE_DETAILS = {
    "name": "sdb1",
    "mount_point": "/mnt/usb",
    "fstype": "vfat",
    "size": "32G",
    "label": "USB Drive",
    "uuid": "B2C3D4E5F6",
    "fstype_full": "FAT32",
}

MOCK_ACTIONS = [
    {"id": "mount", "label": "Mount", "variant": "primary"},
    {"id": "unmount", "label": "Unmount", "variant": "default"},
    {"id": "format", "label": "Format", "variant": "error"},
    {"id": "refresh", "label": "Refresh", "variant": "default"},
]

MOCK_TABLE_ROWS = [
    ("sda1", "50G", "ext4", "-"),
    ("sdb1", "32G", "vfat", "/mnt/usb"),
    ("sdc1", "500G", "ntfs", "/mnt/backup"),
]
