#!/usr/bin/env python3
"""
Watches CapsLock state by reading raw Linux input events from /dev/input.
The kernel emits EV_LED / LED_CAPSL events whenever CapsLock toggles —
no polling, no inotify, zero CPU between keystrokes.
"""
import glob
import json
import os
import select
import struct
import sys

# ── Linux input_event constants ──────────────────────────────────────────────
# struct input_event { struct timeval tv; __u16 type; __u16 code; __s32 value; }
# timeval = two longs (8 bytes each on 64-bit)
_EVENT_FMT  = "llHHi"
_EVENT_SIZE = struct.calcsize(_EVENT_FMT)

EV_SYN  = 0x00
EV_LED  = 0x11

LED_CAPSL = 0x01   # CapsLock LED code

# ── find keyboards ───────────────────────────────────────────────────────────

def _has_capsl(fd: int) -> bool:
    """
    Ask the kernel (EVIOCGBIT) whether this device has an EV_LED / LED_CAPSL bit.
    We use a 4-byte bitmask — enough to cover LED codes 0-31.
    """
    import ctypes, fcntl
    EVIOCGBIT = lambda ev, n: (0x80000000 | 0x00000000 | (n << 16) | (ord('E') << 8) | (0x20 + ev))
    # LED bits
    buf = ctypes.create_string_buffer(4)
    try:
        fcntl.ioctl(fd, EVIOCGBIT(EV_LED, 4), buf)
        bits = int.from_bytes(buf.raw, "little")
        return bool(bits & (1 << LED_CAPSL))
    except OSError:
        return False

def find_keyboards() -> list[str]:
    """Return /dev/input/eventN paths that expose the CapsLock LED."""
    devices = []
    for path in sorted(glob.glob("/dev/input/event*")):
        try:
            fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
            if _has_capsl(fd):
                devices.append(path)
            os.close(fd)
        except OSError:
            pass
    return devices

# ── read initial caps state via LED bitmask ──────────────────────────────────

def get_caps_state(fd: int) -> bool:
    """Read the current LED state bitmask from the device."""
    import ctypes, fcntl
    EVIOCGLED = 0x80004519   # get LED bits, 4-byte buffer
    buf = ctypes.create_string_buffer(4)
    try:
        fcntl.ioctl(fd, EVIOCGLED, buf)
        bits = int.from_bytes(buf.raw, "little")
        return bool(bits & (1 << LED_CAPSL))
    except OSError:
        return False

# ── output ───────────────────────────────────────────────────────────────────

def emit(state: bool) -> None:
    print(json.dumps({"active": state, "icon": "󰘲", "text": "CAPS"}), flush=True)

# ── main loop ────────────────────────────────────────────────────────────────

def watch(paths: list[str]) -> None:
    fds = []
    for path in paths:
        try:
            fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
            fds.append(fd)
        except OSError as e:
            print(f"# warning: cannot open {path}: {e}", file=sys.stderr)

    if not fds:
        print("# no keyboard devices found (try running as root or add user to 'input' group)",
              file=sys.stderr)
        emit(False)
        return

    # Emit initial state from first device
    last = get_caps_state(fds[0])
    emit(last)

    buf = bytearray(_EVENT_SIZE)
    try:
        while True:
            # select blocks with zero CPU until at least one device has data
            readable, _, _ = select.select(fds, [], [])
            for fd in readable:
                while True:
                    try:
                        n = os.readinto(fd, buf)
                    except BlockingIOError:
                        break   # no more events queued on this fd right now
                    if n < _EVENT_SIZE:
                        continue
                    _, _, etype, code, value = struct.unpack_from(_EVENT_FMT, buf)
                    if etype == EV_LED and code == LED_CAPSL:
                        state = bool(value)
                        if state != last:
                            last = state
                            emit(state)
    finally:
        for fd in fds:
            try:
                os.close(fd)
            except OSError:
                pass

if __name__ == "__main__":
    try:
        watch(find_keyboards())
    except KeyboardInterrupt:
        pass
