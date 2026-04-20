"""Storybook screen for testing TUI components."""

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import DataTable, Input, Static

from tusb.storybook.mocks import (
    MOCK_ACTIONS,
    MOCK_DEVICE_DETAILS,
    MOCK_TABLE_ROWS,
)
from tusb.ui.widgets import ActionBar, DeviceDetails, DeviceTable

WIDGET_REGISTRY = {
    "DeviceTable": {
        "class": DeviceTable,
        "default_props": {},
        "props_schema": {},
        "description": "Data table for displaying devices",
    },
    "DeviceDetails": {
        "class": DeviceDetails,
        "default_props": {"device": MOCK_DEVICE_DETAILS},
        "props_schema": {
            "name": "Device name",
            "size": "Device size",
            "fstype": "Filesystem type",
            "mount": "Mount point",
            "label": "Label",
            "uuid": "UUID",
        },
        "description": "Widget for displaying device details",
    },
    "ActionBar": {
        "class": ActionBar,
        "default_props": {"actions": MOCK_ACTIONS},
        "props_schema": {
            "button_count": "Number of buttons",
        },
        "description": "Widget for action buttons",
    },
}


class StorybookScreen(Screen):
    """Storybook screen with widget selector, preview, and props editor."""

    CSS = """
    StorybookScreen {
        layout: horizontal;
    }

    #widget-list {
        width: 25%;
        height: 100%;
        background: $panel;
        border-right: solid $primary;
    }

    #widget-list > Static#widget-header {
        height: auto;
        text-style: bold;
        padding: 1;
        background: $accent;
        color: $text;
    }

    #widget-list DataTable {
        height: 100%;
    }

    #preview {
        width: 50%;
        height: 100%;
        background: $surface;
        border-right: solid $primary;
    }

    #preview > Static#preview-header {
        height: auto;
        text-style: bold;
        padding: 1;
        background: $accent;
        color: $text;
    }

    #preview-content {
        height: 100%;
        padding: 1;
    }

    #props-panel {
        width: 25%;
        height: 100%;
        background: $panel;
    }

    #props-panel > Static#props-header {
        height: auto;
        text-style: bold;
        padding: 1;
        background: $accent;
        color: $text;
    }

    #props-form {
        height: 100%;
        padding: 1;
    }

    .prop-label {
        width: 100%;
        color: $text-muted;
    }

    .prop-input {
        width: 100%;
        margin-bottom: 1;
    }

    .help-text {
        color: $text-muted;
        padding: 1;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("left", "prev_widget", "Prev Widget"),
        ("right", "next_widget", "Next Widget"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.widget_names = list(WIDGET_REGISTRY.keys())
        self.current_index = 0
        self.current_widget: DeviceTable | DeviceDetails | ActionBar | None = None
        self.current_props: dict = {}

    @property
    def current_widget_name(self) -> str:
        return self.widget_names[self.current_index]

    def compose(self) -> ComposeResult:
        yield Horizontal(
            Vertical(
                Static("WIDGETS", id="widget-header"),
                DataTable(id="widget-table"),
                id="widget-list",
            ),
            Vertical(
                Static("PREVIEW", id="preview-header"),
                Container(id="preview-content"),
                id="preview",
            ),
            Vertical(
                Static("PROPS", id="props-header"),
                Container(id="props-form"),
                id="props-panel",
            ),
        )

    def on_mount(self) -> None:
        table = self.query_one("#widget-table", DataTable)
        table.add_column("Widget")
        table.add_column("Description")

        for name, info in WIDGET_REGISTRY.items():
            table.add_row(name, info["description"])

        table.cursor_type = "row"
        table.focus()

        self.watch_events()

        self.render_widget()

    def watch_events(self) -> None:
        table = self.query_one("#widget-table", DataTable)

        def on_row_selected(event: DataTable.RowSelected) -> None:
            if event.row_key:
                idx = self.widget_names.index(str(event.row_key.value))
                self.current_index = idx
                self.render_widget()

        table.on_row_selected = on_row_selected

    def render_widget(self) -> None:
        widget_info = WIDGET_REGISTRY[self.current_widget_name]
        widget_class = widget_info["class"]

        preview_content = self.query_one("#preview-content", Container)
        preview_content.remove_children()

        if self.current_widget_name == "DeviceTable":
            widget = DeviceTable()
            for row in MOCK_TABLE_ROWS:
                widget.add_row(*row)
        elif self.current_widget_name == "DeviceDetails":
            widget = DeviceDetails(device=MOCK_DEVICE_DETAILS)
        elif self.current_widget_name == "ActionBar":
            widget = ActionBar(actions=MOCK_ACTIONS)
        else:
            widget = widget_class()

        preview_content.mount(widget)
        self.current_widget = widget
        self.current_props = widget_info["default_props"].copy()

        self.render_props_form()

    def render_props_form(self) -> None:
        props_form = self.query_one("#props-form", Container)
        props_form.remove_children()

        widget_info = WIDGET_REGISTRY[self.current_widget_name]
        schema = widget_info["props_schema"]

        if not schema:
            props_form.mount(Static("No editable props for this widget", classes="help-text"))
            return

        props_form.mount(Static("Edit props and press Enter to apply:", classes="help-text"))

        for prop_key, prop_label in schema.items():
            current_value = self.current_props.get(prop_key, "")

            input_widget = Input(
                value=str(current_value),
                id=f"prop-{prop_key}",
                classes="prop-input",
            )

            def make_handler(key):
                def handler(event: Input.Submitted):
                    self.current_props[key] = event.input.value
                    self.render_widget()
                    self.query_one(f"#prop-{key}", Input).focus()

                return handler

            input_widget.on_submit = make_handler(prop_key)

            props_form.mount(Static(prop_label, classes="prop-label"))
            props_form.mount(input_widget)

    def action_prev_widget(self) -> None:
        self.current_index = (self.current_index - 1) % len(self.widget_names)
        self.render_widget()

    def action_next_widget(self) -> None:
        self.current_index = (self.current_index + 1) % len(self.widget_names)
        self.render_widget()

    def action_quit(self) -> None:
        self.app.exit()
