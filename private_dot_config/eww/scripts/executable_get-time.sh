#!/usr/bin/env bash

while true; do
  # Print time and date using pure Bash built-in strftime formatting
  printf '{"time": "%s", "day": "%s", "date": "%s %s"}\n' \
    "$(printf '%(%H:%M)T')" \
    "$(printf '%(%a)T')" \
    "$(printf '%(%b)T')" \
    "$(printf '%(%d)T')"

  # Read current second natively (prevents subshell fork)
  printf -v sec '%(%S)T'

  # Calculate remaining seconds until the next :00 mark
  # (Handles leading zero stripping automatically via 10#)
  sleep_time=$((60 - 10#$sec))

  # Fallback to 60 if executed exactly on the second mark
  ((sleep_time == 0)) && sleep_time=60

  sleep "$sleep_time"
done
