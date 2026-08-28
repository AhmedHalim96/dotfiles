#!/usr/bin/env python3
import json
import subprocess

ICON_MAP = {
    "T": "󰕰",  "S": "󰨞",  "G": "󰝘",  "M": "󰍉",
    "K": "󰓩",  "CT": "󰕯", "RT": "󰕮", "VS": "󰨟",
    "VT": "󰕲", "VG": "󰝙", "VK": "󰓪", "DW": "󰏇",
    "F": "󰓅",  "VF": "󰓄"
}

def main():
    try:
        res = subprocess.run(["mmsg", "get", "layouts"], capture_output=True, text=True, timeout=1)
        data = json.loads(res.stdout)
        layouts = data.get("layouts", [])
    except Exception:
        layouts = []

    for l in layouts:
        sym = l.get("symbol", "")
        l["icon"] = ICON_MAP.get(sym, "󰕰")

    print(json.dumps(layouts), flush=True)

if __name__ == "__main__":
    main()
