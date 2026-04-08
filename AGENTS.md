# tusb Agent Guide

## Quick Start

```bash
cd /mnt/storage/code/python/tusb
uv sync                    # Install dependencies
.venv/bin/tusb            # Run the app
```

## Run Commands

| Task | Command |
|------|---------|
| Run app | `.venv/bin/tusb` or `tusb` (if installed) |
| Run as root (for mount) | `sudo .venv/bin/tusb` or `pkexec .venv/bin/tusb` |
| Lint | `.venv/bin/ruff check src/` |
| Fix lint | `.venv/bin/ruff check src/ --fix` |

## Architecture

- **Thread 1 (UI)**: Textual TUI in main thread - user input, display
- **Thread 2 (Data)**: Background thread - lsblk, mount/unmount polling via `queue.Queue`

## Key Files

| File | Purpose |
|------|---------|
| `src/tusb/app.py` | Main App class, CSS, key bindings |
| `src/tusb/devices/scanner.py` | lsblk parsing (handles nested partitions) |
| `src/tusb/devices/manager.py` | mount/unmount subprocess calls |
| `src/tusb/utils/fstab.py` | fstab line generator |

## Key Bindings

- `M` - Mount selected device
- `U` - Unmount selected device
- `F` - Generate fstab line (display for copy)
- `R` - Manual refresh device list
- `Q` - Quit

## Important Notes

- Python 3.14+ required (uses asyncio features)
- Textual 8.x API differs from 7.x (no `run_app()`, use `app.run()`)
- DataTable requires `cursor_type = "row"` for row selection
- Handle both `RowSelected` and `RowHighlighted` events for selection
- lsblk JSON has nested `children` for disk partitions - need recursive extraction
- Mount needs root: run with `sudo` or `pkexec`

## CLI Options

```bash
tusb --refresh-interval 30 --mount-dir /mnt --config ~/.config/tusb.toml
```