#!/home/ahmed/venv/bin/python3
import asyncio
import json
import sys
import pulsectl_asyncio


async def format_audio_state(pulse: pulsectl_asyncio.PulseAsync) -> dict:
    """Queries current sink status and formats output matching original JSON structure."""
    server_info = await pulse.server_info()
    default_sink_name = server_info.default_sink_name
    sinks = await pulse.sink_list()

    active_sink = None
    sink_list = []

    for sink in sinks:
        # Ignore loopback devices matching 'snd_aloop'
        if "snd_aloop" in sink.name:
            continue

        description = (
            sink.proplist.get("node.nick")
            or sink.description
            or "Unknown"
        )
        is_default = sink.name == default_sink_name

        if is_default:
            active_sink = sink

        sink_list.append({
            "id": sink.name,
            "description": description,
            "is_default": is_default,
        })

    # Volume extraction (front-left channel preference, fallback to overall average)
    if active_sink:
        # volume.value_flat gives a float (0.0 to 1.0+)
        volume_pct = round(active_sink.volume.value_flat * 100)
        is_muted = bool(active_sink.mute)
        active_name = (
            active_sink.proplist.get("node.nick")
            or active_sink.description
            or "Unknown"
        )
    else:
        volume_pct = 0
        is_muted = False
        active_name = "Unknown"

    return {
        "volume": volume_pct,
        "is_muted": is_muted,
        "active_sink": active_name,
        "sinks": sink_list,
    }


def print_json(data: dict) -> None:
    """Emits JSON immediately with unbuffered stdout flush."""
    print(json.dumps(data), flush=True)


async def main():
    async with pulsectl_asyncio.PulseAsync("audio-monitor") as pulse:
        # Print initial state
        initial_state = await format_audio_state(pulse)
        print_json(initial_state)

        # Listen exclusively for server/sink events
        async for event in pulse.subscribe_events("sink", "server"):
            # Only trigger on change/new events
            if event.t in ("change", "new", "remove"):
                try:
                    state = await format_audio_state(pulse)
                    print_json(state)
                except Exception as err:
                    # Guard against brief state race conditions during device disconnects
                    sys.stderr.write(f"Error fetching state: {err}\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)
