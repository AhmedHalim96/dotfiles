#!/usr/bin/env python3
import json
import subprocess
import threading
import sys

# Centralized state structure grouped by monitor name
state = {
    "tags": {},     # { "eDP-1": [...], "HDMI-A-1": [...] }
    "clients": {}   # { "eDP-1": [...], "HDMI-A-1": [...] }
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
            for entry in data.get("all_tags", []):
                mon = entry.get("monitor", "")
                tags_by_mon[mon] = entry.get("tags", [])
            with lock:
                state["tags"] = tags_by_mon
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
                # Pre-filter visible clients
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
