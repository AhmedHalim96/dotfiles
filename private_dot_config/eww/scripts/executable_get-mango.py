#!/usr/bin/env python3
import json
import subprocess
import threading

state = {
    "tags": {},          # { "eDP-1": [...], "HDMI-A-1": [...] }
    "active_layout": {}, # { "eDP-1": "T", "HDMI-A-1": "S" }
    "clients": {}
}
lock = threading.Lock()

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

                # Extract active tag's layout symbol for this monitor
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
