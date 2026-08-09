#!/bin/bash
# Get disk usage for all physical mounts, skipping tempfs and loop devices
df -h --output=target,pcent,avail | grep -vE 'tmpfs|loop|udev|efivar' | tail -n +2 | jq -R -s '
  split("\n") | map(select(length > 0) | split(" ") | map(select(length > 0))) | 
  map({target: .[0], percentage: .[1] | sub("%";"") | tonumber, free: .[2]})'
