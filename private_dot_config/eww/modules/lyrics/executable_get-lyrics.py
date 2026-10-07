#!/usr/bin/env python3
import json
import os
import shutil
import subprocess
import sys

# Maximum characters allowed before truncating for status bar layout
MAX_LENGTH = 65


def truncate(text: str, max_len: int = MAX_LENGTH) -> str:
    """Truncates long lyric lines to avoid breaking status bar widgets."""
    if len(text) > max_len:
        return text[: max_len - 1].strip() + "…"
    return text


def main():
    # Initial emission (hidden)
    print(json.dumps({"text": "", "visible": False}), flush=True)

    # Resolve executable path (checks PATH or fallback to ~/.local/bin/mpris-lyrics)
    cmd_path = shutil.which("mpris-lyrics")
    if not cmd_path:
        user_bin = os.path.expanduser("~/.local/bin/mpris-lyrics")
        if os.path.isfile(user_bin) and os.access(user_bin, os.X_OK):
            cmd_path = user_bin

    if not cmd_path:
        print(
            json.dumps({"text": "mpris-lyrics not found", "visible": False}),
            flush=True,
        )
        sys.exit(0)

    proc = None
    try:
        proc = subprocess.Popen(
            [cmd_path, "--pipe"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            bufsize=1,
        )

        for line in iter(proc.stdout.readline, ""):
            clean_line = line.strip()

            # Hide when line is empty, instrumental, or indicates no lyrics
            if (
                not clean_line
                or "no lyrics" in clean_line.lower()
                or clean_line.lower() == "instrumental"
            ):
                payload = {"text": "", "visible": False}
            else:
                payload = {
                    "text": truncate(clean_line),
                    "visible": True,
                }

            print(json.dumps(payload), flush=True)

    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        if proc and proc.poll() is None:
            proc.terminate()


if __name__ == "__main__":
    main()
