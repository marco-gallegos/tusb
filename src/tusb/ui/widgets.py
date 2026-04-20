"""Custom widgets for tusb UI."""

from textual.widget import Widget
from textual.widgets import Button, DataTable, Static


class DeviceTable(DataTable):
    """Data table for displaying devices."""

    def __init__(self) -> None:
        super().__init__()
        self.add_columns("Name", "Size", "Type", "Mount")


class DeviceDetails(Widget):
    """Widget for displaying device details."""

    def __init__(self, device: dict | None = None) -> None:
        super().__init__()
        self._device = device

    def compose(self):
        yield Static("DEVICE DETAILS", id="details-title")
        if self._device:
            content = f"""Name:    {self._device.get('name', '-')}
Size:    {self._device.get('size', '-')}
Type:    {self._device.get('fstype', '-')}
Mount:   {self._device.get('mount_point', '-')}
Label:   {self._device.get('label', '-')}
UUID:    {self._device.get('uuid', '-')}"""
            yield Static(content, id="details-content")
        else:
            yield Static("Select a device to see details", id="details-content")


class ActionBar(Widget):
    """Widget for action buttons."""

    def __init__(self, actions: list | None = None) -> None:
        super().__init__()
        self._actions = actions or []

    def compose(self):
        for action in self._actions:
            yield Button(action.get("label", ""), id=action.get("id", ""), variant=action.get("variant", "default"))
