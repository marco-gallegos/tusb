"""Custom widgets for tusb UI."""

from textual.widget import Widget
from textual.widgets import DataTable, Static


class DeviceTable(DataTable):
    """Data table for displaying devices."""

    def __init__(self) -> None:
        super().__init__()
        self.add_columns("Name", "Size", "Type", "Mount")


class DeviceDetails(Widget):
    """Widget for displaying device details."""

    def __init__(self) -> None:
        super().__init__()

    def compose(self):
        yield Static("DEVICE DETAILS", id="details-title")
        yield Static("", id="details-content")


class ActionBar(Widget):
    """Widget for action buttons."""

    def __init__(self) -> None:
        super().__init__()
