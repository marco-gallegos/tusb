"""Storybook application."""

from textual.app import App

from tusb.storybook.screen import StorybookScreen


class StorybookApp(App):
    """Storybook app for testing TUI components."""

    CSS = """
    Screen {
        background: $surface;
    }
    """

    def __init__(self) -> None:
        super().__init__()
        self._storybook_screen = StorybookScreen()

    def on_mount(self) -> None:
        self.push_screen(self._storybook_screen)
