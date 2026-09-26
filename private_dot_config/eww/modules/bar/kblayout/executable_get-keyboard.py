#!/usr/bin/env python3
import json
import subprocess
import sys

# Map full layout strings to clean 2-letter bar badges
LAYOUT_MAP = {
    "English (US)": "US",
    "English (US, intl., with dead keys)": "US",
    "Arabic": "AR",
    "Arabic (qwerty)": "AR",
    "French": "FR",
    "German": "DE",
    "Spanish": "ES",
    "Russian": "RU",
    "Japanese": "JP",
}

def get_short_name(full_name):
    if full_name in LAYOUT_MAP:
        return LAYOUT_MAP[full_name]
    # Fallback: take first 2 letters uppercase
    clean = full_name.split("(")[0].strip()
    return clean[:2].upper() if len(clean) >= 2 else clean.upper()

def main():
    proc = subprocess.Popen(
        ["mmsg", "watch", "keyboardlayout"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True
    )

    for line in iter(proc.stdout.readline, ''):
        if not line.strip():
            continue
        try:
            data = json.loads(line)
            full_layout = data.get("layout", "US")
            short_layout = get_short_name(full_layout)

            payload = {
                "full": full_layout,
                "short": short_layout,
            }
            print(json.dumps(payload), flush=True)
        except Exception:
            pass

if __name__ == "__main__":
    main()
