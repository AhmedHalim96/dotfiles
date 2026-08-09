#!/bin/bash

# Get stats from vnstat for the current interface (e.g., wlan0 or eth0)
# Change 'wlan0' to your actual interface name
INTERFACE="wlo1"

get_vnstat() {
  # Grabs Today and Month totals in a human-readable format
  TODAY=$(vnstat -i $INTERFACE --oneline | cut -d';' -f6)
  MONTH=$(vnstat -i $INTERFACE --oneline | cut -d';' -f11)

  # Get top process using a non-interactive nethogs dump
  # We run it for 2 iterations and take the last one for accuracy
  #TOP_PROC=$(timeout 30s nethogs -t $INTERFACE | grep / | sort -rnk3 | head -n 1 | awk '{print $1 " | " $3 "KB/s"}')

  if [ -z "$TOP_PROC" ]; then TOP_PROC="Idle"; fi

  echo "{\"today\":\"$TODAY\", \"month\":\"$MONTH\"}"
}

get_vnstat
