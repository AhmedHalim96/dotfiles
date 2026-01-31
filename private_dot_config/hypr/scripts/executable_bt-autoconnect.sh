#!/bin/bash

# 1. Ensure Bluetooth is powered on
bluetoothctl power on

# 2. Give the controller a second to breathe
sleep 3

# 3. Get the MAC address of the first paired device
# (You can change 'head -n 1' to a specific MAC if you prefer)
DEVICE_MAC=$(bluetoothctl devices Paired | rg p2i | cut -d ' ' -f 2)

# 4. Attempt to connect
if [ -n "$DEVICE_MAC" ]; then
  echo "Found Device: $DEVICE_MAC. Connecting now....."
  bluetoothctl connect "$DEVICE_MAC"
fi
