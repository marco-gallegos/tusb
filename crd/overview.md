# USB Manager for linux

I want to have a tui to easly manage usb devices on linux systems.

## UI

ui should be a simple text user interface to easly manage USB devices.

## Technical Requirements

- writed on python.
- app should work in a two threads architecture, thread 1 is to handle ui, thread 2 is to data handling, fetching, command execution etc.
- make it simple and modular to be easy to extend.
- make it a package to upload it to pypi.
- use uv, and ruff.
- use real threads with python >= 3.14.

## Functionality

- devices should be listed from the lsblk command.
- my default mount dir should be /mnt subdirs.
- ui should tell me details about partition (where is mopunted, type of partition, size, etc).
- i want a quick action to mount on default dirs.
- i want a action to generate fstab automount line just to copy paste.
- should handle umount too.
- mount should allow write on devices so use `-o umask=000` or a better/secure option to allow it
- request sudo password on the fly to allow admin operation like mount.
  - do not store password on any var, ensure we drop that password after use it.

