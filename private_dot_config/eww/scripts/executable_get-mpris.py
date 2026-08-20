#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import urllib.request

CACHE_PATH = "/tmp/eww_cover.jpg"

def process_art_url(url):
    if not url:
        return ""
    if url.startswith("file://"):
        return url.replace("file://", "")
    if url.startswith("http://") or url.startswith("https://"):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=2) as response:
                with open(CACHE_PATH, 'wb') as f:
                    f.write(response.read())
            return CACHE_PATH
        except Exception:
            return ""
    return url

def get_mpris_state():
    try:
        # Fetch metadata for all players
        res = subprocess.run(
            ["playerctl", "-a", "metadata", "--format",
             "{{status}}\t{{title}}\t{{artist}}\t{{album}}\t{{mpris:artUrl}}\t{{playerName}}"],
            capture_output=True, text=True, timeout=2
        )
        lines = [line for line in res.stdout.strip().split("\n") if line]
        if not lines:
            return {"status": "Stopped", "title": "Nothing Playing", "artist": "", "album": "", "artUrl": "", "player": ""}

        players = []
        for line in lines:
            parts = line.split("\t")
            if len(parts) >= 6:
                players.append({
                    "status": parts[0],
                    "title": parts[1],
                    "artist": parts[2],
                    "album": parts[3],
                    "artUrl": parts[4],
                    "player": parts[5]
                })

        # Prioritize active 'Playing' stream
        playing = [p for p in players if p["status"] == "Playing"]
        target = playing[0] if playing else players[0]

        target["artUrl"] = process_art_url(target.get("artUrl", ""))
        return target
    except Exception:
        return {"status": "Stopped", "title": "Nothing Playing", "artist": "", "album": "", "artUrl": "", "player": ""}

def main():
    last_state = None

    # Emit initial state
    initial = get_mpris_state()
    print(json.dumps(initial), flush=True)
    last_state = initial

    # Monitor events cleanly via playerctl stream
    proc = subprocess.Popen(
        ["playerctl", "-a", "metadata", "--follow", "--format", "{{status}}\t{{title}}"],
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True
    )

    while True:
        line = proc.stdout.readline()
        if not line and proc.poll() is not None:
            break

        state = get_mpris_state()
        if state != last_state:
            print(json.dumps(state), flush=True)
            last_state = state

if __name__ == "__main__":
    main()
EOF
