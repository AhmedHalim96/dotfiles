#!/usr/bin/env bash

get_audio() {
  DEF=$(pactl get-default-sink)
  pactl -f json list sinks | jq -c --arg def "$DEF" '
    ([.[] | select(.name == $def)] | first) as $active |
    {
      volume: ($active.volume["front-left"].value_percent // "0%" | rtrimstr("%") | tonumber),
      is_muted: ($active.mute // false),
      active_sink: ($active.properties["node.nick"] // $active.description // "Unknown"),
      sinks: [.[] | select(.name | contains("snd_aloop") | not) | {
        id: .name,
        description: (.properties["node.nick"] // .description),
        is_default: (.name == $def)
      }]
    }'
}

# Output initial state immediately
get_audio

# Listen for volume, mute, and default sink changes
pactl subscribe | stdbuf -oL grep --line-buffered -E "sink|server" | while read -r _; do
  get_audio
done
