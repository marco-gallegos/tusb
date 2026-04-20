"""Storybook entry point."""

from tusb.storybook.app import StorybookApp


def main() -> None:
    """Run the storybook."""
    app = StorybookApp()
    app.run()


if __name__ == "__main__":
    main()
