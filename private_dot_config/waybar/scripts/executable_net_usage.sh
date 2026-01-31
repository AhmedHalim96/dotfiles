#!/bin/bash
INTERFACE="wlo1"

# Filter out warnings and grab JSON
DATA=$(vnstat -i "$INTERFACE" --json 2>/dev/null | grep '^{')

# Parse Today's Usage (Now correctly identifying these as BYTES)
TODAY_RX=$(echo "$DATA" | jq '.interfaces[0].traffic.day[0].rx')
TODAY_TX=$(echo "$DATA" | jq '.interfaces[0].traffic.day[0].tx')
TODAY_TOTAL=$((TODAY_RX + TODAY_TX))

# Parse Monthly Usage
MONTH_RX=$(echo "$DATA" | jq '.interfaces[0].traffic.month[0].rx')
MONTH_TX=$(echo "$DATA" | jq '.interfaces[0].traffic.month[0].tx')
MONTH_TOTAL=$((MONTH_RX + MONTH_TX))

# Conversion function (Bytes -> MiB/GiB)
convert() {
  local bytes=$1
  if [ "$bytes" -gt 1073741824 ]; then
    # More than 1 GiB
    echo "$(awk "BEGIN {printf \"%.2f\", $bytes/1073741824}") GiB"
  else
    # Show in MiB
    echo "$(awk "BEGIN {printf \"%.2f\", $bytes/1048576}") MiB"
  fi
}

TEXT=" $(convert $TODAY_TOTAL)"
TOOLTIP="<b><u>Network Stats ($INTERFACE)</u></b>\n\n<b>Today:</b>\n  Down: $(convert $TODAY_RX)\n  Up: $(convert $TODAY_TX)\n  Total: $(convert $TODAY_TOTAL)\n\n<b>This Month:</b>\n  Total: $(convert $MONTH_TOTAL)"

printf '{"text": "%s", "tooltip": "%s"}\n' "$TEXT" "$TOOLTIP"
