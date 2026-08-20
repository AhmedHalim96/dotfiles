#!/usr/bin/env python3
import json
import time

def get_default_iface():
    """Finds the primary active network interface from kernel routing table."""
    try:
        with open("/proc/net/route", "r") as f:
            for line in f.readlines()[1:]:
                fields = line.strip().split()
                # 00000000 destination and RTF_UP flag
                if fields[1] == '00000000' and int(fields[3], 16) & 2:
                    return fields[0]
    except Exception:
        pass
    return None

def read_bytes(iface):
    """Reads cumulative RX and TX bytes for an interface."""
    if not iface:
        return 0, 0
    try:
        with open("/proc/net/dev", "r") as f:
            for line in f.readlines()[2:]:
                if iface in line:
                    parts = line.split(":")
                    if len(parts) > 1:
                        stats = parts[1].split()
                        return int(stats[0]), int(stats[8]) # rx_bytes, tx_bytes
    except Exception:
        pass
    return 0, 0

def format_speed(speed_bytes):
    if speed_bytes < 1024:
        return f"{str(int(speed_bytes))} B/s"
    elif speed_bytes < 1024 * 1024:
        return f"{speed_bytes / 1024:.1f} KB/s"
    else:
        return f"{speed_bytes / (1024 * 1024):.1f} MB/s"

def main():
    last_rx, last_tx = 0, 0
    last_time = time.time()
    iface = get_default_iface()

    if iface:
        last_rx, last_tx = read_bytes(iface)

    while True:
        time.sleep(1)
        curr_time = time.time()
        dt = curr_time - last_time
        last_time = curr_time

        curr_iface = get_default_iface()
        curr_rx, curr_tx = read_bytes(curr_iface) if curr_iface else (0, 0)

        # Calculate speed if interface didn't change
        if curr_iface != iface or last_rx == 0:
            rx_speed, tx_speed = 0, 0
        else:
            rx_speed = max(0, (curr_rx - last_rx) / dt)
            tx_speed = max(0, (curr_tx - last_tx) / dt)

        iface = curr_iface
        last_rx, last_tx = curr_rx, curr_tx

        is_wifi = iface.startswith("w") if iface else False
        icon = "󰤨 " if is_wifi else ("󰈀 " if iface else "󰤭 ")

        payload = {
            "iface": iface or "Disconnected",
            "icon": icon,
            "down": format_speed(rx_speed),
            "up": format_speed(tx_speed)
        }
        print(json.dumps(payload), flush=True)

if __name__ == "__main__":
    main()
