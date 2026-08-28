#!/usr/bin/env python3
import json
import subprocess
import sys

# Icon and label mappings for non-default keymodes
KEYMODE_MAP = {
    "media": {"label": "MEDIA", "icon": "󰎈"},
    "apps":  {"label": "APPS",  "icon": "󰀻"},
    "passthrough": {"label": "PASS", "icon": "󰌌"},
}

def main():
    proc = subprocess.Popen(
        ["mmsg", "watch", "keymode"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True
    )

    # Initial emission (hidden by default)
    print(json.dumps({"name": "default", "label": "", "icon": "", "visible": False}), flush=True)

    for line in iter(proc.stdout.readline, ''):
        if not line.strip():
            continue
        try:
            data = json.loads(line)
            mode = data.get("keymode", "default").lower()

            if mode == "default":
                payload = {
                    "name": "default",
                    "label": "",
                    "icon": "",
                    "visible": False
                }
            else:
                meta = KEYMODE_MAP.get(mode, {"label": mode.upper(), "icon": "󰌌"})
                payload = {
                    "name": mode,
                    "label": meta["label"],
                    "icon": meta["icon"],
                    "visible": True
                }

            print(json.dumps(payload), flush=True)
        except Exception:
            pass

if __name__ == "__main__":
    main()
