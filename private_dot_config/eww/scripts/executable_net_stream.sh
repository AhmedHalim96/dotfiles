#!/bin/bash
# Run once, loop forever, outputting JSON every time a cycle finishes
nethogs -t | stdbuf -oL awk '
BEGIN { printf "[" }
{
    # $1 is usually the process path (e.g., /usr/bin/firefox)
    # $2 is Sent (KB/s), $3 is Received (KB/s)
    
    # Get just the filename from the path
    split($1, path, "/")
    name = path[length(path)]
    
    # Format the numbers to 2 decimal places so they dont jump around
    up = sprintf("%.2f", $2)
    down = sprintf("%.2f", $3)

    if (NR > 1) printf ","
    printf "{\"name\":\"%s\", \"up\":\"%s\", \"down\":\"%s\"}", name, up, down
}
END { printf "]" }'
