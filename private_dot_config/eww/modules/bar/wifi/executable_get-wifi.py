#!/home/ahmed/venv/bin/python3
import asyncio
import json
import socket
import struct
from dbus_next.aio import MessageBus
from dbus_next.constants import BusType
from dbus_next.message import Message, MessageType

NM_SERVICE = "org.freedesktop.NetworkManager"
NM_PATH = "/org/freedesktop/NetworkManager"

class NetworkManagerMonitor:
    def __init__(self):
        self.bus = None
        self.last_output = None

    def _unwrap(self, val):
        """Recursively unwrap DBus variants into native Python data types."""
        if hasattr(val, "value"):
            return self._unwrap(val.value)
        if isinstance(val, dict):
            return {self._unwrap(k): self._unwrap(v) for k, v in val.items()}
        if isinstance(val, list):
            return [self._unwrap(v) for v in val]
        return val

    def _get_signal_icon(self, signal, enabled):
        if not enabled:
            return "󰤭"
        if signal is None or signal == 0:
            return "󰤯"
        if signal <= 25:
            return "󰤟"
        if signal <= 50:
            return "󰤢"
        if signal <= 75:
            return "󰤥"
        return "󰤨"

    async def _call(self, path, interface, member, signature="", body=None):
        reply = await self.bus.call(
            Message(
                destination=NM_SERVICE,
                path=path,
                interface=interface,
                member=member,
                signature=signature,
                body=body or []
            )
        )
        if reply and reply.message_type == MessageType.METHOD_RETURN and reply.body:
            return self._unwrap(reply.body)
        return None

    async def _get_property(self, path, interface, prop_name):
        res = await self._call(
            path,
            "org.freedesktop.DBus.Properties",
            "Get",
            "ss",
            [interface, prop_name]
        )
        return res[0] if res else None

    async def start(self):
        self.bus = await MessageBus(bus_type=BusType.SYSTEM).connect()

        # Subscribe to NetworkManager signals across devices and access points
        match_rules = [
            "type='signal',sender='org.freedesktop.NetworkManager'"
        ]

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

        # Emit initial state
        await self._emit_state()

        # Keep event loop running
        await asyncio.Future()

    def _handle_message(self, msg):
        if msg.message_type != MessageType.SIGNAL:
            return

        member = msg.member
        # React to key NM signals that affect state
        if member in ("PropertiesChanged", "AccessPointAdded", "AccessPointRemoved", "StateChanged"):
            asyncio.create_task(self._emit_state())

    async def _emit_state(self):
        state = await self._build_state_json()
        if state != self.last_output:
            print(json.dumps(state), flush=True)
            self.last_output = state

    async def _build_state_json(self):
        # 1. Check if Wi-Fi Hardware & Radio are enabled
        wireless_enabled = await self._get_property(NM_PATH, NM_SERVICE, "WirelessEnabled")

        if not wireless_enabled:
            return {
                "enabled": False,
                "connected": False,
                "ssid": "Disabled",
                "signal": 0,
                "icon": "󰤭",
                "ip": "N/A",
                "networks": []
            }

        # 2. Locate Wireless Device Path (DeviceType 2 == Wi-Fi)
        devices = await self._call(NM_PATH, NM_SERVICE, "GetDevices")
        wifi_device_path = None

        if devices:
            for dev_path in devices[0]:
                dev_type = await self._get_property(dev_path, f"{NM_SERVICE}.Device", "DeviceType")
                if dev_type == 2:  # NM_DEVICE_TYPE_WIFI
                    wifi_device_path = dev_path
                    break

        if not wifi_device_path:
            return {
                "enabled": True,
                "connected": False,
                "ssid": "No Wi-Fi Card",
                "signal": 0,
                "icon": "󰤭",
                "ip": "N/A",
                "networks": []
            }

        # 3. Get Active Access Point & Available Networks
        active_ap_path = await self._get_property(wifi_device_path, f"{NM_SERVICE}.Device.Wireless", "ActiveAccessPoint")
        ap_paths_res = await self._call(wifi_device_path, f"{NM_SERVICE}.Device.Wireless", "GetAllAccessPoints")

        ap_paths = ap_paths_res[0] if ap_paths_res else []

        connected = False
        active_ssid = "Disconnected"
        active_signal = 0
        networks = []
        seen_ssids = set()

        for ap_path in ap_paths:
            if ap_path == "/":
                continue

            ssid_bytes = await self._get_property(ap_path, f"{NM_SERVICE}.AccessPoint", "Ssid")
            signal = await self._get_property(ap_path, f"{NM_SERVICE}.AccessPoint", "Strength") or 0
            flags = await self._get_property(ap_path, f"{NM_SERVICE}.AccessPoint", "Flags") or 0
            wpa_flags = await self._get_property(ap_path, f"{NM_SERVICE}.AccessPoint", "WpaFlags") or 0
            rsn_flags = await self._get_property(ap_path, f"{NM_SERVICE}.AccessPoint", "RsnFlags") or 0

            ssid = ""
            if ssid_bytes:
                try:
                    ssid = bytes(ssid_bytes).decode("utf-8").strip()
                except Exception:
                    ssid = ""

            if not ssid or ssid in seen_ssids:
                continue
            seen_ssids.add(ssid)

            # Security Label
            security = "Open"
            if (wpa_flags > 0) or (rsn_flags > 0) or (flags & 1):
                security = "WPA/WPA2"

            is_active = (ap_path == active_ap_path)

            if is_active:
                connected = True
                active_ssid = ssid
                active_signal = signal

            networks.append({
                "ssid": ssid,
                "signal": signal,
                "active": is_active,
                "security": security,
                "icon": self._get_signal_icon(signal, True)
            })

        # 4. Get IPv4 Address directly from DBus IP4Config interface
        ip_addr = "N/A"
        if connected:
            ip4_config_path = await self._get_property(wifi_device_path, f"{NM_SERVICE}.Device", "Ip4Config")
            if ip4_config_path and ip4_config_path != "/":
                address_data = await self._get_property(ip4_config_path, f"{NM_SERVICE}.IP4Config", "AddressData")
                if address_data and len(address_data) > 0:
                    ip_addr = address_data[0].get("address", "N/A")

        networks.sort(key=lambda x: x["signal"], reverse=True)

        return {
            "enabled": True,
            "connected": connected,
            "ssid": active_ssid,
            "signal": active_signal,
            "icon": self._get_signal_icon(active_signal, connected),
            "ip": ip_addr,
            "networks": networks[:6]
        }

if __name__ == "__main__":
    try:
        asyncio.run(NetworkManagerMonitor().start())
    except KeyboardInterrupt:
        pass
