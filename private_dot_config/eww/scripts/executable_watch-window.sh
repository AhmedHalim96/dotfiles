#!/usr/bin/env bash
# ~/.config/eww/scripts/watch-window.sh

WINDOW_NAME="$1"

# Initial check
eww active-windows | grep -q "$WINDOW_NAME" && echo "true" || echo "false"

# Listen for eww commands or window updates
# Note: You can tailor this stream to monitor compositor window events (e.g., hyprctl / swaymsg)
