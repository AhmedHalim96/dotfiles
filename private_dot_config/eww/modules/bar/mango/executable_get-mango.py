#!/usr/bin/env python3
import json
import subprocess
import threading
import os
import glob

state = {
    "tags": {},          # { "eDP-1": [...], "HDMI-A-1": [...] }
    "active_layout": {}, # { "eDP-1": "T", "HDMI-A-1": "S" }
    "clients": {}
}
lock = threading.Lock()

# ---------------------------------------------------------------------------
# Icon resolution
# ---------------------------------------------------------------------------

DESKTOP_DIRS = [
    os.path.expanduser("~/.local/share/applications"),
    "/usr/local/share/applications",
    "/usr/share/applications",
    "/var/lib/flatpak/exports/share/applications",
    os.path.expanduser("~/.local/share/flatpak/exports/share/applications"),
    "/run/host/usr/share/applications",
]

ICON_DIRS = [
    os.path.expanduser("~/.local/share/icons"),
    "/usr/local/share/icons",
    "/usr/share/icons",
    "/usr/share/pixmaps",
    "/var/lib/flatpak/exports/share/icons",
    os.path.expanduser("~/.local/share/flatpak/exports/share/icons"),
]

ICON_THEMES = ["hicolor", "Papirus", "Papirus-Dark", "breeze", "breeze-dark",
               "Adwaita", "gnome", "elementary", ""]
ICON_SIZES  = ["scalable", "256x256", "128x128", "96x96", "64x64", "48x48",
               "32x32", "22x22", "16x16"]
ICON_EXTS   = [".svg", ".png", ".xpm"]

# Hard overrides for known bad/weird appids  (lowercase keys)
ICON_OVERRIDES = {
    # Browsers
    "navigator":                "firefox",
    "org.mozilla.firefox":      "firefox",
    "floorp":                   "floorp",
    "ablaze-floorp":            "floorp",
    "librewolf":                "librewolf",
    "google-chrome":            "google-chrome",
    "chromium":                 "chromium",
    "chromium-browser":         "chromium",
    "microsoft-edge":           "microsoft-edge",
    "brave-browser":            "brave-browser",
    "vivaldi":                  "vivaldi",
    "org.gnome.epiphany":       "org.gnome.Epiphany",
    # Terminals
    "kitty":                    "kitty",
    "alacritty":                "Alacritty",
    "foot":                     "foot",
    "wezterm":                  "org.wezfurlong.wezterm",
    "org.wezfurlong.wezterm":   "org.wezfurlong.wezterm",
    "konsole":                  "utilities-terminal",
    "gnome-terminal":           "utilities-terminal",
    "xterm":                    "utilities-terminal",
    "urxvt":                    "utilities-terminal",
    "st":                       "utilities-terminal",
    # Editors / IDEs
    "dev.zed.zed":              "zed",
    "zed":                      "zed",
    "code":                     "visual-studio-code",
    "code - oss":               "code-oss",
    "codium":                   "vscodium",
    "vscodium":                 "vscodium",
    "neovim":                   "nvim",
    "nvim":                     "nvim",
    "vim":                      "vim",
    "gvim":                     "gvim",
    "emacs":                    "emacs",
    "org.gnu.emacs":            "emacs",
    "jetbrains-idea":           "intellij-idea",
    "jetbrains-pycharm":        "pycharm",
    "jetbrains-webstorm":       "webstorm",
    "jetbrains-clion":          "clion",
    # File managers
    "org.gnome.nautilus":       "system-file-manager",
    "org.gnome.files":          "system-file-manager",
    "thunar":                   "org.xfce.thunar",
    "pcmanfm":                  "system-file-manager",
    "pcmanfm-qt":               "system-file-manager",
    "dolphin":                  "system-file-manager",
    "nemo":                     "system-file-manager",
    "ranger":                   "utilities-terminal",
    "yazi":                     "utilities-terminal",
    "lf":                       "utilities-terminal",
    # Chat / Social
    "discord":                  "discord",
    "webcord":                  "webcord",
    "vesktop":                  "discord",
    "legcord":                  "discord",
    "slack":                    "slack",
    "telegram":                 "telegram",
    "org.telegram.desktop":     "telegram",
    "signal":                   "signal-desktop",
    "org.signal.signal":        "signal-desktop",
    "element":                  "element",
    # Media
    "spotify":                  "spotify",
    "vlc":                      "vlc",
    "mpv":                      "mpv",
    "celluloid":                "io.github.celluloid_player.Celluloid",
    "io.github.celluloid_player.celluloid": "io.github.celluloid_player.Celluloid",
    "rhythmbox":                "rhythmbox",
    "audacious":                "audacious",
    "clementine":               "clementine",
    # Graphics
    "gimp":                     "gimp",
    "gimp-2.10":                "gimp",
    "gimp-3.0":                 "gimp",
    "inkscape":                 "inkscape",
    "org.inkscape.inkscape":    "inkscape",
    "krita":                    "krita",
    "org.kde.krita":            "krita",
    "blender":                  "blender",
    # OBS
    "obs":                      "com.obsproject.Studio",
    "com.obsproject.studio":    "com.obsproject.Studio",
    # Gaming
    "steam":                    "steam",
    "heroic":                   "heroic",
    "lutris":                   "lutris",
    # System
    "org.gnome.settings":       "preferences-system",
    "gnome-control-center":     "preferences-system",
    "pavucontrol":              "multimedia-volume-control",
    "org.pulseaudio.pavucontrol": "multimedia-volume-control",
    "nm-connection-editor":     "network-wired",
    "org.gnome.baobab":         "baobab",
    # Office / docs
    "org.gnome.evince":         "evince",
    "evince":                   "evince",
    "zathura":                  "zathura",
    "libreoffice":              "libreoffice-startcenter",
    "libreoffice-writer":       "libreoffice-writer",
    "libreoffice-calc":         "libreoffice-calc",
    "libreoffice-impress":      "libreoffice-impress",
    # Password managers
    "bitwarden":                "bitwarden",
    "1password":                "1password",
}

DISK_CACHE_PATH = os.path.expanduser("~/.cache/mmsg-icons.json")

def _load_disk_cache() -> dict[str, str]:
    try:
        with open(DISK_CACHE_PATH, encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                return data
    except (OSError, json.JSONDecodeError):
        pass
    return {}

def _save_disk_cache(cache: dict[str, str]) -> None:
    try:
        os.makedirs(os.path.dirname(DISK_CACHE_PATH), exist_ok=True)
        with open(DISK_CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump(cache, f)
    except OSError:
        pass

_icon_cache: dict[str, str] = _load_disk_cache()


def _appid_candidates(appid: str) -> list[str]:
    """Return ordered list of icon-name candidates to try for an appid."""
    key = appid.lower()
    out = []

    # 1. hard override
    if key in ICON_OVERRIDES:
        out.append(ICON_OVERRIDES[key])

    # 2. exact as given (covers "Spotify", "dev.zed.Zed", etc.)
    out.append(appid)

    # 3. lowercase
    out.append(key)

    # 4. last segment of reverse-DNS  (dev.zed.Zed -> Zed, zed)
    parts = appid.split(".")
    if len(parts) > 1:
        out.append(parts[-1])
        out.append(parts[-1].lower())
        # second-to-last too  (com.spotify.Client -> spotify)
        out.append(parts[-2])
        out.append(parts[-2].lower())

    # 5. strip common suffixes/prefixes
    for strip in ("-stable", "-bin", "-git", "-nightly", "-release"):
        if key.endswith(strip):
            out.append(key[: -len(strip)])

    # 6. separator variants
    for src, dst in [("-", "_"), ("_", "-"), (".", "-")]:
        out.append(key.replace(src, dst))

    # de-dup, preserve order
    seen: set[str] = set()
    result = []
    for c in out:
        if c and c not in seen:
            seen.add(c)
            result.append(c)
    return result


def _find_desktop_icon(appid: str) -> str | None:
    """
    Look up the Icon= field in a matching .desktop file.
    This is the most reliable mapping because it's what the app itself declares.
    """
    candidates = _appid_candidates(appid)

    for d in DESKTOP_DIRS:
        if not os.path.isdir(d):
            continue
        for name in candidates:
            for filename in [name + ".desktop", name.lower() + ".desktop"]:
                path = os.path.join(d, filename)
                if os.path.isfile(path):
                    icon = _read_desktop_icon(path)
                    if icon:
                        return icon

    # glob fallback: any .desktop whose filename contains the appid
    key = appid.lower().split(".")[-1]   # just the last segment to avoid too-broad matches
    for d in DESKTOP_DIRS:
        if not os.path.isdir(d):
            continue
        for path in glob.glob(os.path.join(d, f"*{key}*.desktop")):
            icon = _read_desktop_icon(path)
            if icon:
                return icon

    return None


def _read_desktop_icon(path: str) -> str | None:
    try:
        in_entry = False
        with open(path, encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if line == "[Desktop Entry]":
                    in_entry = True
                elif line.startswith("[") and in_entry:
                    break   # left the [Desktop Entry] section
                elif in_entry and line.startswith("Icon="):
                    return line.split("=", 1)[1].strip()
    except OSError:
        pass
    return None


def _find_icon_file(icon_name: str) -> str | None:
    """Find the actual file for icon_name, searching theme dirs."""
    if not icon_name:
        return None

    # Already an absolute path
    if os.path.isabs(icon_name) and os.path.isfile(icon_name):
        return icon_name

    for base in ICON_DIRS:
        if not os.path.isdir(base):
            continue
        for theme in ICON_THEMES:
            for size in ICON_SIZES:
                for cat in ("apps", ""):
                    parts = [base]
                    if theme: parts.append(theme)
                    parts.append(size)
                    if cat:   parts.append(cat)
                    folder = os.path.join(*parts)
                    for ext in ICON_EXTS:
                        p = os.path.join(folder, icon_name + ext)
                        if os.path.isfile(p):
                            return p
        # flat pixmaps / root of base
        for ext in ICON_EXTS:
            p = os.path.join(base, icon_name + ext)
            if os.path.isfile(p):
                return p

    # Last resort: recursive glob (slow, only runs if nothing found above)
    for base in ICON_DIRS:
        matches = glob.glob(os.path.join(base, "**", icon_name + ".svg"), recursive=True)
        if not matches:
            matches = glob.glob(os.path.join(base, "**", icon_name + ".png"), recursive=True)
        if matches:
            # prefer scalable then largest size
            matches.sort(key=lambda p: ("scalable" in p, "256" in p, "128" in p), reverse=True)
            return matches[0]

    return None


def resolve_icon(appid: str) -> str:
    """
    Return the best icon path for appid.
    Strategy:
      1. .desktop file lookup  -> gives us the canonical icon name
      2. Search that name in icon theme dirs
      3. If step 1 failed, try appid candidates directly in icon dirs
    Falls back to 'application-x-executable'.
    """
    if not appid:
        return "application-x-executable"

    cache_key = appid.lower()
    if cache_key in _icon_cache:
        return _icon_cache[cache_key]

    result = "application-x-executable"

    # Step 1 + 2: .desktop -> icon name -> path
    icon_name = _find_desktop_icon(appid)
    if icon_name:
        path = _find_icon_file(icon_name)
        if path:
            result = path
        else:
            # icon name is valid but file wasn't found — return the name anyway
            # so eww can try its own theme lookup
            result = icon_name

    # Step 3: try candidates directly as icon names/paths
    if result == "application-x-executable":
        for candidate in _appid_candidates(appid):
            path = _find_icon_file(candidate)
            if path:
                result = path
                break

    _icon_cache[cache_key] = result
    _save_disk_cache(_icon_cache)
    return result


# ---------------------------------------------------------------------------
# Watch logic
# ---------------------------------------------------------------------------

def emit():
    with lock:
        print(json.dumps(state), flush=True)


def watch_tags():
    proc = subprocess.Popen(["mmsg", "watch", "all-tags"], stdout=subprocess.PIPE, text=True)
    for line in iter(proc.stdout.readline, ''):
        if not line.strip():
            continue
        try:
            data = json.loads(line)
            tags_by_mon = {}
            layout_by_mon = {}
            for entry in data.get("all_tags", []):
                mon = entry.get("monitor", "")
                tags = entry.get("tags", [])
                tags_by_mon[mon] = tags
                active_sym = "T"
                for tag in tags:
                    if tag.get("is_active", False):
                        active_sym = tag.get("layout", "T")
                        break
                layout_by_mon[mon] = active_sym
            with lock:
                state["tags"] = tags_by_mon
                state["active_layout"] = layout_by_mon
            emit()
        except Exception:
            pass


def watch_clients():
    proc = subprocess.Popen(["mmsg", "watch", "all-clients"], stdout=subprocess.PIPE, text=True)
    for line in iter(proc.stdout.readline, ''):
        if not line.strip():
            continue
        try:
            data = json.loads(line)
            clients_by_mon = {}
            for client in data.get("clients", []):
                if not client.get("is_visible", False):
                    continue
                mon = client.get("monitor", "")
                if mon not in clients_by_mon:
                    clients_by_mon[mon] = []

                # NOTE: the field is "appid", not "app_id"
                appid = client.get("appid", "") or client.get("app_id", "") or ""
                client["icon"] = resolve_icon(appid)

                clients_by_mon[mon].append(client)
            with lock:
                state["clients"] = clients_by_mon
            emit()
        except Exception:
            pass


def main():
    t1 = threading.Thread(target=watch_tags, daemon=True)
    t2 = threading.Thread(target=watch_clients, daemon=True)
    t1.start()
    t2.start()
    t1.join()
    t2.join()


if __name__ == "__main__":
    main()
