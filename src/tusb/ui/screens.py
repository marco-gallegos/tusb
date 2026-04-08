"""Main screen for tusb."""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import DataTable, Static


class MainScreen(Screen):
    """Main screen with device list and details."""

    def __init__(self) -> None:
        super().__init__()
        self.table: DataTable | None = None
        self.details: Static | None = None
        self.status: Static | None = None

    def compose(self) -> ComposeResult:
        yield Static("tusb - USB Device Manager", id="title")
        yield DataTable(id="device-table")
        yield Static("Select a device to see details", id="details")
        yield Static("", id="status-bar")

    def on_mount(self) -> None:
        self.table = self.query_one("#device-table", DataTable)
        self.details = self.query_one("#details", Static)
        self.status = self.query_one("#status-bar", Static)

        self.table.add_columns("Name", "Size", "Type", "Mount")

    def update_table(self, devices: list) -> None:
        if self.table is None:
            return

        self.table.clear()
        for device in devices:
            self.table.add_row(
                device.name,
                device.size,
                device.fstype or "-",
                device.mount_point or "-",
            )

    def update_details(self, device) -> None:
        if self.details is None or device is None:
            return

        details_text = f"""Name:    {device.name}
Size:    {device.size}
Type:    {device.fstype or "-"}
Mount:   {device.mount_point or "-"}
Label:   {device.label or "-"}
UUID:    {device.uuid or "-"}
FSType:  {device.fstype or "-"}"""

        self.details.update(details_text)

    def set_status(self, message: str) -> None:
        if self.status:
            self.status.update(message)
