#!/usr/bin/env python3
import sys
import json
import subprocess
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Read monitor name from argument, default to HDMI-A-1
monitor = sys.argv[1] if len(sys.argv) > 1 else "HDMI-A-1"
icon_theme = Gtk.IconTheme.get_default()

# Spawn mmsg stream
process = subprocess.Popen(
    ["mmsg", "watch", "monitor", monitor],
    stdout=subprocess.PIPE,
    text=True
)

for line in iter(process.stdout.readline, ''):
    line = line.strip()
    if not line:
        continue
    try:
        data = json.loads(line)
        active_client = data.get("active_client")

        # Resolve icon path if active_client exists
        if active_client and isinstance(active_client, dict):
            appid = active_client.get("appid", "")
            # Try exact appid match, then lowercase fallback
            icon = icon_theme.lookup_icon(appid, 24, 0) or icon_theme.lookup_icon(appid.lower(), 24, 0)
            active_client["icon_path"] = icon.get_filename() if icon else ""

        print(json.dumps(data), flush=True)
    except Exception:
        print(line, flush=True)
