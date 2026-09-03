#!/home/ahmed/venv/bin/python3
import asyncio
import json
import re
import sys
from dbus_next.aio import MessageBus
from dbus_next.constants import BusType
from dbus_next.message import Message, MessageType

BLUEZ_SERVICE = "org.bluez"
ICON_MAP = [
    (r"audio-headset|audio-headphones|headphone|headset", "󰋋"),
    (r"input-gamepad|controller|gamepad", "󰊴"),
    (r"phone", "󰄜"),
    (r"input-mouse|mouse", "󰍽"),
]

def log(msg):
    print(f"[DEBUG] {msg}", file=sys.stderr, flush=True)

class BluetoothMonitor:
    def __init__(self):
        self.bus = None
        self.managed_objects = {}
        self.last_output = None
        self._was_powered = False
        self._attempting_connect = set()

    def _unwrap(self, val):
        if hasattr(val, "value"):
            return self._unwrap(val.value)
        if isinstance(val, dict):
            return {self._unwrap(k): self._unwrap(v) for k, v in val.items()}
        if isinstance(val, list):
            return [self._unwrap(v) for v in val]
        return val

    async def start(self):
        log("Connecting to System DBus...")
        self.bus = await MessageBus(bus_type=BusType.SYSTEM).connect()

        match_rules = ["type='signal',sender='org.bluez'"]

        for rule in match_rules:
            await self.bus.call(
                Message(
                    destination="org.freedesktop.DBus",
                    path="/org/freedesktop/DBus",
                    interface="org.freedesktop.DBus",
                    member="AddMatch",
                    signature="s",
                    body=[rule]
                )
            )

        self.bus.add_message_handler(self._handle_message)

        await self._fetch_managed_objects()
        self._check_auto_connect()
        self._emit_state()

        await asyncio.Future()

    async def _fetch_managed_objects(self):
        try:
            reply = await self.bus.call(
                Message(
                    destination=BLUEZ_SERVICE,
                    path="/",
                    interface="org.freedesktop.DBus.ObjectManager",
                    member="GetManagedObjects"
                )
            )
            if reply and reply.message_type == MessageType.METHOD_RETURN and reply.body:
                self.managed_objects = self._unwrap(reply.body[0])
        except Exception as e:
            log(f"GetManagedObjects error: {e}")

    def _handle_message(self, msg):
        if msg.message_type != MessageType.SIGNAL:
            return

        try:
            member = msg.member
            path = msg.path
            body = self._unwrap(msg.body)

            if member == "InterfacesAdded" and len(body) >= 2:
                obj_path, interfaces = body[0], body[1]
                if obj_path not in self.managed_objects:
                    self.managed_objects[obj_path] = {}
                self.managed_objects[obj_path].update(interfaces)
                self._check_auto_connect()
                self._emit_state()

            elif member == "InterfacesRemoved" and len(body) >= 2:
                obj_path, interfaces = body[0], body[1]
                if obj_path in self.managed_objects:
                    for iface in interfaces:
                        self.managed_objects[obj_path].pop(iface, None)
                    if not self.managed_objects[obj_path]:
                        del self.managed_objects[obj_path]
                self._emit_state()

            elif member == "PropertiesChanged" and len(body) >= 2:
                interface_name, changed_props = body[0], body[1]

                if path in self.managed_objects:
                    if interface_name not in self.managed_objects[path]:
                        self.managed_objects[path][interface_name] = {}
                    self.managed_objects[path][interface_name].update(changed_props)
                else:
                    self.managed_objects[path] = {interface_name: changed_props}

                self._check_auto_connect()
                self._emit_state()

        except Exception as e:
            log(f"Signal handling error: {e}")

    def _is_adapter_powered(self):
        for path, interfaces in self.managed_objects.items():
            if "org.bluez.Adapter1" in interfaces:
                if interfaces["org.bluez.Adapter1"].get("Powered", False):
                    return True
        return False

    def _check_auto_connect(self):
        is_powered = self._is_adapter_powered()

        # Trigger auto-connect when adapter switches from off -> on, or on initial run
        if is_powered and not self._was_powered:
            log("Adapter powered on. Running auto-connect sequence...")
            asyncio.create_task(self._auto_connect_paired_devices())

        self._was_powered = is_powered

    async def _auto_connect_device(self, path):
        if path in self._attempting_connect:
            return
        self._attempting_connect.add(path)
        try:
            log(f"Attempting auto-connect to: {path}")
            await self.bus.call(
                Message(
                    destination=BLUEZ_SERVICE,
                    path=path,
                    interface="org.bluez.Device1",
                    member="Connect"
                )
            )
            log(f"Successfully connected to: {path}")
        except Exception as e:
            log(f"Auto-connect failed for {path}: {e}")
        finally:
            # Keep in set briefly to prevent continuous connect loops
            await asyncio.sleep(5)
            self._attempting_connect.discard(path)

    async def _auto_connect_paired_devices(self):
        for path, interfaces in self.managed_objects.items():
            if "org.bluez.Device1" in interfaces:
                dev = interfaces["org.bluez.Device1"]
                is_paired = dev.get("Paired", False) or dev.get("Trusted", False)
                is_connected = dev.get("Connected", False)

                if is_paired and not is_connected:
                    asyncio.create_task(self._auto_connect_device(path))

    def _emit_state(self):
        state = self._build_state_json()
        if state != self.last_output:
            print(json.dumps(state), flush=True)
            self.last_output = state

    def _build_state_json(self):
        adapter_powered = self._is_adapter_powered()

        if not adapter_powered:
            return {
                "enabled": False,
                "connected": False,
                "icon": "󰂲",
                "connected_name": "Disabled",
                "connected_battery": "",
                "devices": []
            }

        devices = []
        any_connected = False
        primary_name = "Disconnected"
        primary_battery = ""

        for path, interfaces in self.managed_objects.items():
            if "org.bluez.Device1" in interfaces:
                dev = interfaces["org.bluez.Device1"]
                name = dev.get("Alias") or dev.get("Name") or "Unknown"
                mac = dev.get("Address", "")
                is_connected = bool(dev.get("Connected", False))
                icon_str = dev.get("Icon", "")

                battery = ""
                if "org.bluez.Battery1" in interfaces:
                    bat_val = interfaces["org.bluez.Battery1"].get("Percentage")
                    if bat_val is not None:
                        battery = f"{bat_val}%"

                icon = "󰂱"
                comb_text = f"{name} {icon_str}"
                for pattern, ic in ICON_MAP:
                    if re.search(pattern, comb_text, re.IGNORECASE):
                        icon = ic
                        break

                if is_connected:
                    any_connected = True
                    if primary_name == "Disconnected":
                        primary_name = name
                        primary_battery = battery

                devices.append({
                    "name": name,
                    "mac": mac,
                    "connected": is_connected,
                    "icon": icon,
                    "battery": battery
                })

        devices.sort(key=lambda x: x["connected"], reverse=True)

        display_name = primary_name
        if primary_battery and primary_name != "Disconnected":
            display_name = f"{primary_name} ({primary_battery})"

        return {
            "enabled": True,
            "connected": any_connected,
            "icon": "󰂱" if any_connected else "󰂯",
            "connected_name": display_name,
            "connected_battery": primary_battery,
            "devices": devices
        }

if __name__ == "__main__":
    try:
        asyncio.run(BluetoothMonitor().start())
    except KeyboardInterrupt:
        pass
