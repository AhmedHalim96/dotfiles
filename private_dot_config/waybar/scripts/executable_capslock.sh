#!/bin/bash

# This path might vary slightly. Check /sys/class/leds/ for your keyboard name if this fails.
# We use '*' to match any input device that has a capslock LED.
CAPS_FILE=$(ls /sys/class/leds/*::capslock/brightness | head -n 1)

while true; do
  if [ -f "$CAPS_FILE" ]; then
    STATUS=$(cat "$CAPS_FILE")
    if [ "$STATUS" -eq 1 ]; then
      # Output for Waybar (Text and Class)
      echo '{"text": "CAPS LOCK ON", "class": "locked"}'
    else
      echo '{"text": "", "class": "unlocked"}'
    fi
  fi
  # Wait for a change or check every 0.1s for instant response
  sleep 0.1
done
