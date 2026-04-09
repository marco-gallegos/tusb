"""Main Textual App for tusb."""

import queue
import threading
from typing import Any

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.screen import ModalScreen
from textual.widgets import Button, DataTable, Input, Static

from tusb.config import Config
from tusb.devices import mount_device, scan_devices, unmount_device
from tusb.models import Device, DeviceList
from tusb.utils import generate_fstab_line


class TusbApp(App):
    """Main application class."""

    CSS = """
    Screen {
        layout: vertical;
    }

    #title {
        height: 1;
        content-align: center middle;
        background: $accent;
    }

    #device-table {
        height: 40%;
    }

    #device-details {
        height: 40%;
        border: solid green;
        padding: 1;
    }

    #status-bar {
        height: 1;
        content-align: center middle;
    }
    """

    BINDINGS = [
        Binding("m", "mount", "Mount"),
        Binding("u", "unmount", "Unmount"),
        Binding("f", "fstab", "Fstab"),
        Binding("r", "refresh", "Refresh"),
        Binding("q", "quit", "Quit"),
    ]

    def __init__(self, config: Config) -> None:
        super().__init__()
        self.config = config
        self.devices: DeviceList = DeviceList()
        self.selected_device: Device | None = None
        self.data_queue: queue.Queue[Any] = queue.Queue()
        self.data_thread: threading.Thread | None = None
        self.running = True

        self.table: DataTable | None = None
        self.details: Static | None = None
        self.status: Static | None = None

    def compose(self) -> ComposeResult:
        yield Static("tusb - USB Device Manager", id="title")
        yield DataTable(id="device-table")
        yield Static("Select a device to see details", id="device-details")
        yield Static(
            "Press M to mount, U to unmount, F for fstab, R to refresh, Q to quit", id="status-bar"
        )

    def on_mount(self) -> None:
        self.table = self.query_one("#device-table", DataTable)
        self.details = self.query_one("#device-details", Static)
        self.status = self.query_one("#status-bar", Static)

        self.table.cursor_type = "row"
        self.table.add_columns("Name", "Size", "Type", "Mount")

        self._start_data_thread()
        self._refresh_devices()

    def _start_data_thread(self) -> None:
        self.data_thread = threading.Thread(target=self._data_loop, daemon=True)
        self.data_thread.start()

    def _data_loop(self) -> None:
        while self.running:
            try:
                request = self.data_queue.get(timeout=1)
                if request is None:
                    break

                action = request.get("action")
                if action == "refresh":
                    devices = scan_devices()
                    self.devices = devices
                    self.call_from_thread(self._update_ui)
                elif action == "mount":
                    device = request.get("device")
                    password = request.get("password")
                    if device:
                        success, msg = mount_device(device, self.config.mount_dir, password)
                        self.call_from_thread(self._set_status, msg)
                        if success:
                            self._refresh_devices()
                elif action == "unmount":
                    device = request.get("device")
                    password = request.get("password")
                    if device:
                        success, msg = unmount_device(device, password)
                        self.call_from_thread(self._set_status, msg)
                        if success:
                            self._refresh_devices()
            except queue.Empty:
                continue
            except Exception as e:
                self.call_from_thread(self._set_status, f"Error: {e}")

    def _refresh_devices(self) -> None:
        self.data_queue.put({"action": "refresh"})

    def _update_ui(self) -> None:
        if self.table is None:
            return

        self.table.clear()
        for device in self.devices:
            self.table.add_row(
                device.name,
                device.size,
                device.fstype or "-",
                device.mount_point or "-",
            )

    def _set_status(self, message: str) -> None:
        if self.status:
            self.status.update(message)

    def _update_details(self) -> None:
        if self.details is None or self.selected_device is None:
            return

        device = self.selected_device
        text = f"""Name:    {device.name}
Size:    {device.size}
Type:    {device.fstype or "-"}
Mount:   {device.mount_point or "-"}
Label:   {device.label or "-"}
UUID:    {device.uuid or "-"}
FSType:  {device.fstype or "-"}"""
        self.details.update(text)

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        self._handle_selection(event.cursor_row)

    def on_data_table_row_highlighted(self, event: DataTable.RowHighlighted) -> None:
        self._handle_selection(event.cursor_row)

    def _handle_selection(self, index: int) -> None:
        if 0 <= index < len(self.devices):
            self.selected_device = self.devices[index]
            self._update_details()

    def action_mount(self) -> None:
        if self.selected_device is None:
            self._set_status("No device selected")
            return
        if self.selected_device.is_mounted:
            self._set_status("Device already mounted")
            return
        self._prompt_password("mount")

    def action_unmount(self) -> None:
        if self.selected_device is None:
            self._set_status("No device selected")
            return
        if not self.selected_device.is_mounted:
            self._set_status("Device not mounted")
            return
        self._prompt_password("unmount")

    def _prompt_password(self, action: str) -> None:
        self._set_status(f"Enter sudo password for {action}...")

        def on_password_submit(password: str) -> None:
            if action == "mount":
                self.data_queue.put(
                    {"action": "mount", "device": self.selected_device, "password": password}
                )
            elif action == "unmount":
                self.data_queue.put(
                    {"action": "unmount", "device": self.selected_device, "password": password}
                )

        self.push_screen(PasswordInput(on_password_submit))

    def action_fstab(self) -> None:
        if self.selected_device is None:
            self._set_status("No device selected")
            return

        line = generate_fstab_line(self.selected_device, self.config.mount_dir)
        self._set_status(f"Fstab: {line}")

    def action_refresh(self) -> None:
        self._refresh_devices()
        self._set_status("Refreshing...")

    def action_quit(self) -> None:
        self.running = False
        self.data_queue.put(None)
        self.exit()


class PasswordInput(ModalScreen):
    def __init__(self, on_submit: callable) -> None:
        super().__init__()
        self.on_submit = on_submit

    CSS = """
    PasswordInput {
        align: center middle;
    }
    #prompt {
        margin-bottom: 1;
    }
    #container {
        width: 40;
    }
    """

    BINDINGS = [
        Binding("escape", "cancel", "Cancel"),
        Binding("enter", "submit", "Submit"),
    ]

    def compose(self) -> ComposeResult:
        with Static(id="container"):
            yield Static("Enter sudo password:", id="prompt")
            yield Input(placeholder="Password", password=True, id="password-input")
            yield Button("Submit", variant="primary", id="submit-btn")

    def on_mount(self) -> None:
        input_widget = self.query_one("#password-input", Input)
        input_widget.focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "submit-btn":
            self.action_submit()

    def action_submit(self) -> None:
        input_widget = self.query_one("#password-input", Input)
        password = input_widget.value
        self.app.pop_screen()
        self.on_submit(password)

    def action_cancel(self) -> None:
        self.app.pop_screen()
