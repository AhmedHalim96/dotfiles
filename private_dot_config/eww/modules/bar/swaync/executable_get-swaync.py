#!/usr/bin/env python3
import json
import shutil
import subprocess
import sys

ICON_MAP = {
    "notification": "",
    "none": "",
    "dnd-notification": "",
    "dnd-none": "",
    "inhibited-notification": "",
    "inhibited-none": "",
    "dnd-inhibited-notification": "",
    "dnd-inhibited-none": "",
}

def main():
    if not shutil.which("swaync-client"):
        print(json.dumps({"icon": "", "alt": "none", "count": 0, "dnd": False, "tooltip": "swaync-client missing"}), flush=True)
        sys.exit(0)

    proc = subprocess.Popen(
        ["swaync-client", "-swb"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True
    )

    for line in iter(proc.stdout.readline, ''):
        if not line.strip():
            continue
        try:
            data = json.loads(line)
            alt = data.get("alt", "none")
            icon = ICON_MAP.get(alt, "")
            count = data.get("count", 0)
            dnd = alt.startswith("dnd")
            tooltip = data.get("tooltip", f"{count} Notifications")

            payload = {
                "icon": icon,
                "alt": alt,
                "count": count,
                "dnd": dnd,
                "tooltip": tooltip
            }
            print(json.dumps(payload), flush=True)
        except Exception:
            pass

if __name__ == "__main__":
    main()
