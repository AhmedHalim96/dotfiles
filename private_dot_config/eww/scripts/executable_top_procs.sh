#!/bin/bash

# Get top 5 processes by CPU usage
# Format: name, cpu_usage
processes=$(ps -eo comm,%cpu --sort=-%cpu | head -n 10 | tail -n 9)

# Convert to JSON array
echo "$processes" | awk '
BEGIN { printf "[" }
{
    if (NR > 1) printf ","
    printf "{\"name\":\"%s\", \"cpu\":\"%s%%\"}", $1, $2
}
END { printf "]" }'
