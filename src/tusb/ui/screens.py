"""Main screen for tusb."""

from textual.app import ComposeResult
from textual.screen import ModalScreen, Screen
from textual.widgets import Button, DataTable, Input, Select, Static

from tusb.models import Device, FormatType


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


class FormatModal(ModalScreen):
    """Modal for formatting a partition."""

    def __init__(self, device: Device, on_format: callable) -> None:
        super().__init__()
        self.device = device
        self.on_format = on_format
        self.fs_select: Select[str] | None = None
        self.label_input: Input | None = None
        self.confirm_input: Input | None = None

    CSS = """
    FormatModal {
        align: center middle;
    }
    #container {
        width: 60;
        height: auto;
    }
    #warning {
        color: $error;
        text-style: bold;
    }
    .form-row {
        layout: horizontal;
        height: auto;
    }
    """

    BINDINGS = [
        ("escape", "cancel", "Cancel"),
    ]

    def compose(self) -> ComposeResult:
        with Static(id="container"):
            yield Static("Format Partition", id="title")
            yield Static(f"Device: {self.device.name} ({self.device.size})", id="device-info")
            current_fs = self.device.fstype.lower() if self.device.fstype else "unknown"
            yield Static(f"Current: {current_fs.upper()}", id="current-fs")
            yield Static("Select filesystem:", id="fs-label")
            options = [
                ("keep", f"Same ({current_fs.upper()})"),
                (FormatType.FAT32.value, "FAT32"),
                (FormatType.EXFAT.value, "ExFAT"),
                (FormatType.NTFS.value, "NTFS"),
                (FormatType.EXT4.value, "EXT4"),
            ]
            yield Select(options=options, id="fs-select")
            yield Static("Label (optional):", id="label-label")
            yield Input(placeholder="Enter label", id="label-input")
            yield Static("Type 'yes' to confirm:", id="confirm-label")
            yield Input(placeholder="yes", id="confirm-input")
            yield Button("Format", variant="error", id="format-btn")

    def on_mount(self) -> None:
        self.fs_select = self.query_one("#fs-select", Select)
        self.label_input = self.query_one("#label-input", Input)
        self.confirm_input = self.query_one("#confirm-input", Input)
        self.fs_select.focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "format-btn":
            self.action_format()

    def action_format(self) -> None:
        if self.confirm_input is None or self.fs_select is None:
            return

        if self.confirm_input.value.lower() != "yes":
            self.app.pop_screen()
            return

        selected = self.fs_select.value
        fs_key = selected[0] if isinstance(selected, tuple) else str(selected)
        fs_type = FormatType(fs_key.lower())
        label = self.label_input.value if self.label_input.value else None

        self.app.pop_screen()
        self.on_format(fs_type, label)

    def action_cancel(self) -> None:
        self.app.pop_screen()
