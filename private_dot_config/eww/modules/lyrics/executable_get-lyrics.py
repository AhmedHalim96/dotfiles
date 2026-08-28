#!/usr/bin/env python3
import json
import subprocess
import sys

def main():
    # Initial emission (hidden)
    print(json.dumps({"text": "", "visible": False}), flush=True)

    try:
        proc = subprocess.Popen(
            ["lyricsmpris", "--pipe"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            bufsize=1
        )
    except FileNotFoundError:
        print(json.dumps({"text": "lyricsmpris not found", "visible": False}), flush=True)
        sys.exit(0)

    for line in iter(proc.stdout.readline, ''):
        clean_line = line.strip()
        
        # Hide when empty, instrumental, or explicitly no lyrics available
        if not clean_line or "no lyrics" in clean_line.lower() or clean_line.lower() == "instrumental":
            payload = {"text": "", "visible": False}
        else:
            payload = {"text": clean_line, "visible": True}

        print(json.dumps(payload), flush=True)

if __name__ == "__main__":
    main()
