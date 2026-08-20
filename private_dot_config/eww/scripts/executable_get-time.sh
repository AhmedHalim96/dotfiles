#!/usr/bin/env bash

while true; do
  # Print time and date as JSON
  date '+{"time": "%H:%M", "day": "%a", "date": "%b %d"}'

  # Calculate seconds until the top of the next minute
  SEC=$(date +%S)
  SLEEP_TIME=$((60 - 10#$SEC))

  # Sleep until the exact :00 mark
  sleep "$SLEEP_TIME"
done
