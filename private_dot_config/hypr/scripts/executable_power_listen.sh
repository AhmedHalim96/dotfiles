#!/bin/bash

CRITICAL_LEVEL=5
BATTERY_PATH="/org/freedesktop/UPower/devices/battery_BAT0"
STATE_FILE="/tmp/hypr_power_state"

send_notif() {
  # Get current status and capacity
  # We use 'tr' to make sure the case is consistent
  status=$(upower -i $BATTERY_PATH | grep state | awk '{print $2}' | tr '[:upper:]' '[:lower:]')
  capacity=$(upower -i $BATTERY_PATH | grep percentage | tr -dc '0-9')

  # Read the last saved state
  [ -f "$STATE_FILE" ] && last_state=$(cat "$STATE_FILE") || last_state="unknown"

  # Only notify if the state has actually CHANGED
  if [ "$status" != "$last_state" ]; then
    echo "$status" >"$STATE_FILE"

    if [ "$status" = "charging" ]; then
      notify-send -u low -i battery-charging -h string:x-canonical-private-synchronous:power_notif "Power Plugged" "Battery: ${capacity}%"
    elif [ "$status" = "discharging" ]; then
      notify-send -u normal -i battery-caution -h string:x-canonical-private-synchronous:power_notif "Power Unplugged" "Battery: ${capacity}%"
    fi
  fi

  # Check for Critical Level regardless of state change (safety first)
  if [ "$status" = "discharging" ] && [ "$capacity" -le "$CRITICAL_LEVEL" ]; then
    notify-send -u critical -i battery-empty "BATTERY CRITICAL" "Level: ${capacity}%. Suspending in 10s..."
    sleep 10
    if [ "$(upower -i $BATTERY_PATH | grep state | awk '{print $2}')" = "discharging" ]; then
      systemctl suspend
    fi
  fi
}

# Real-time listener
gdbus monitor --system --dest org.freedesktop.UPower --object-path "$BATTERY_PATH" | while read -r line; do
  # When ANY property changes, wait 0.5s for UPower to finish updating all values
  # then run the check once.
  sleep 0.5
  send_notif
done
