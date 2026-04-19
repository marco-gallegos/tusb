"""Pydantic data models for tusb."""

from enum import StrEnum

from pydantic import BaseModel, Field


class FormatType(StrEnum):
    """Filesystem types for formatting."""

    KEEP = "keep"
    FAT32 = "fat32"
    EXFAT = "exfat"
    NTFS = "ntfs"
    EXT4 = "ext4"


class Device(BaseModel):
    """Represents a partition/device."""

    name: str = Field(description="Device name (e.g., sda1)")
    mount_point: str | None = Field(default=None, description="Current mount point")
    fstype: str | None = Field(default=None, description="Filesystem type (ext4, ntfs, etc)")
    size: str = Field(description="Size (e.g., 32G)")
    label: str | None = Field(default=None, description="Partition label")
    uuid: str | None = Field(default=None, description="Partition UUID")
    parttype: str | None = Field(default=None, description="Partition type")
    is_partition: bool = Field(default=False, description="Whether this is a partition (not whole disk)")

    @property
    def is_mounted(self) -> bool:
        """Check if device is mounted."""
        return self.mount_point is not None

    @property
    def display_name(self) -> str:
        """Get display name (label if available, else name)."""
        return self.label or self.name

    def get_mount_dir_name(self) -> str:
        """Get directory name for mounting."""
        if self.label:
            return self.label
        if self.uuid:
            return self.uuid
        return self.name


class DeviceList(BaseModel):
    """List of devices."""

    devices: list[Device] = Field(default_factory=list)

    def __iter__(self):
        return iter(self.devices)

    def __len__(self):
        return len(self.devices)

    def __getitem__(self, index: int) -> Device:
        return self.devices[index]


class CommandRequest(BaseModel):
    """Request from UI thread to data thread."""

    action: str = Field(description="Action to perform")
    device: Device | None = Field(default=None, description="Target device")
    mount_dir: str | None = Field(default=None, description="Mount directory")


class CommandResponse(BaseModel):
    """Response from data thread to UI thread."""

    success: bool = Field(description="Whether action succeeded")
    message: str = Field(description="Response message")
    devices: DeviceList | None = Field(default=None, description="Updated device list")


class AppState(BaseModel):
    """Shared application state."""

    devices: DeviceList = Field(default_factory=DeviceList)
    selected_index: int = 0
    last_refresh: str | None = None
    error: str | None = None
