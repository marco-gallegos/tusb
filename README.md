# tusb

TUI for managing USB devices on Linux.

## Current Features

- List block devices via `lsblk`
- Mount/unmount USB devices with sudo password
- Generate fstab entries
- Device details (UUID, label, filesystem type)
- Write permissions via uid/gid mapping
- Auto-refresh device list
- Cross-platform compatibility checks

## Upcoming Features

- Device favorites/persistence
- Auto-mount on device plugged in
- Mount options configuration
- Multiple mount points per device
- Device filtering by type

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

## References

- [caligula](https://github.com/ifd3f/caligula/) - TUI for managing LUKS volumes