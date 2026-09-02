#!/usr/bin/env python3
import json
import subprocess
import sys

def get_brightness():
    try:
        cur = float(subprocess.run(["brightnessctl", "get"], capture_output=True, text=True).stdout.strip())
        max_b = float(subprocess.run(["brightnessctl", "max"], capture_output=True, text=True).stdout.strip())
        pct = int(round((cur / max_b) * 100))
    except Exception:
        pct = 100

    # Dynamic Sun Icon selection
    if pct <= 33:
        icon = "󰃞" # Low sun
    elif pct <= 66:
        icon = "󰃟" # Medium sun
    elif pct <= 90:
        icon = "󰃝" # High sun
    else:
        icon = "󰃠" # High sun

    # Smooth solar color gradient: Amber (#FF9E00) -> Warm Yellow (#FFC300) -> Brilliant Gold (#FFEA00)
    if pct <= 50:
        r = 255
        g = int(158 + (pct / 50.0) * (195 - 158))
        b = 0
    else:
        r = 255
        g = int(195 + ((pct - 50) / 50.0) * (234 - 195))
        b = 0

    return {
        "pct": pct,
        "icon": icon,
        "color": f"#{r:02x}{g:02x}{b:02x}"
    }

def main():
    # Emit initial state immediately
    last_data = get_brightness()
    print(json.dumps(last_data), flush=True)

    # Watch backlight udev events directly with unbuffered stdout
    try:
        proc = subprocess.Popen(
            ["stdbuf", "-oL", "udevadm", "monitor", "--udev", "--subsystem-match=backlight"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            bufsize=1
        )
    except FileNotFoundError:
        proc = subprocess.Popen(
            ["stdbuf", "-oL", "brightnessctl", "m"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            bufsize=1
        )

    for line in iter(proc.stdout.readline, ''):
        if not line.strip():
            continue
        data = get_brightness()
        if data != last_data:
            print(json.dumps(data), flush=True)
            last_data = data

if __name__ == "__main__":
    main()
