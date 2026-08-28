#!/usr/bin/env python3
import json
import subprocess
import sys

ICON_MAP = {
    "performance": "󰓅",
    "balanced": "󰾅",
    "power-saver": "󰌪"
}

def get_profile_data():
    try:
        res = subprocess.run(["powerprofilesctl", "get"], capture_output=True, text=True, timeout=1)
        active = res.stdout.strip()
    except Exception:
        active = "balanced"

    return {
        "active": active,
        "icon": ICON_MAP.get(active, "󰾅"),
        "profiles": [
            {"id": "performance", "name": "Performance", "icon": "󰓅"},
            {"id": "balanced", "name": "Balanced", "icon": "󰾅"},
            {"id": "power-saver", "name": "Power Saver", "icon": "󰌪"}
        ]
    }

def main():
    # Emit initial state
    last_data = get_profile_data()
    print(json.dumps(last_data), flush=True)

    # Monitor D-Bus signals for system power profile switches
    proc = subprocess.Popen(
        ["dbus-monitor", "--system", "type='signal',interface='org.freedesktop.DBus.Properties',path='/net/hadess/PowerProfiles'"],
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True
    )

    for line in iter(proc.stdout.readline, ''):
        data = get_profile_data()
        if data != last_data:
            print(json.dumps(data), flush=True)
            last_data = data

if __name__ == "__main__":
    main()
