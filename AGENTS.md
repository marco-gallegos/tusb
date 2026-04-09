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
| `src/tusb/devices/manager.py` | mount/unmount with sudo password, uid/gid mapping |
| `src/tusb/utils/fstab.py` | fstab line generator |

## Key Bindings

- `M` - Mount selected device (prompts for sudo password)
- `U` - Unmount selected device (prompts for sudo password)
- `F` - Generate fstab line (display for copy)
- `R` - Manual refresh device list
- `Q` - Quit

## CRD Status (crd/overview.md)

| Requirement | Line | Status |
|-------------|------|--------|
| Python TUI | 11 | ✅ Implemented |
| Two-thread architecture | 12 | ✅ Implemented |
| uv + ruff | 15 | ✅ Implemented |
| Real threads (Python >= 3.16) | 16 | ✅ Implemented |
| lsblk device listing | 20 | ✅ Implemented |
| Default mount dir `/mnt` | 21 | ✅ Implemented |
| Device details | 22 | ✅ Implemented |
| Quick mount action | 23 | ✅ Implemented |
| fstab line generation | 24 | ✅ Implemented |
| Unmount action | 25 | ✅ Implemented |
| Write permissions on mount | 26 | ✅ Implemented (uid/gid mapping) |
| Sudo password on-the-fly | 27-29 | ✅ Implemented (sudo -S, prompt via getpass) |
| pypi-ready package | 14 | ✅ Updated (license, classifiers) |
| LICENSE file | - | ✅ Added (GPLv3 full text) |

## Important Notes

- Python 3.14+ required
- Textual 8.x API differs from 7.x (no `run_app()`, use `app.run()`)
- DataTable requires `cursor_type = "row"` for row selection
- Handle both `RowSelected` and `RowHighlighted` events for selection
- lsblk JSON has nested `children` for disk partitions - need recursive extraction
- Mount/unmount prompts for sudo password via stdin (`sudo -S`)
- Password is stored temporarily then deleted immediately after use
- Write permissions via uid/gid mapping (e.g., `uid=1000,gid=1000`) instead of insecure umask=000

## CLI Options

```bash
tusb --refresh-interval 30 --mount-dir /mnt --config ~/.config/tusb.toml
```