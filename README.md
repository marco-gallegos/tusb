# tusb

TUI for managing USB devices on Linux.

## Features

- List block devices via `lsblk`
- Mount/unmount USB devices with sudo password
- Generate fstab entries
- Device details (UUID, label, filesystem type)
- Write permissions via uid/gid mapping

## Installation

### uv ( Recommended )

```bash
uv tool install tusb
```

Or for development:

```bash
uv sync
.venv/bin/tusb
```

### From PyPI

```bash
pip install tusb
```

## Usage

```
tusb
```

### Key Bindings

| Key | Action |
|-----|--------|
| M | Mount selected device |
| U | Unmount selected device |
| F | Generate fstab line |
| R | Refresh device list |
| Q | Quit |

## Requirements

- Linux
- Python 3.14+
- sudo permissions