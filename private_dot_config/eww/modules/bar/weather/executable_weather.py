#!/usr/bin/env python3
import json
import re
import sys
import urllib.request

def get_weather(location="Cairo"):
    url = f"https://wttr.in/{location}?format=%C+%t+%f"

    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'curl/7.68.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = response.read().decode('utf-8').strip()

        if not data:
            raise ValueError("Empty response")

        condition, temp, feels = data.split('+')
        condition_clean = condition.strip().lower()

        # Map weather condition to Nerd Font icons
        if any(w in condition_clean for w in ["cloud", "overcast"]):
            icon = ""  # nf-md-weather_cloudy
        elif any(w in condition_clean for w in ["clear", "sunny", "sun"]):
            icon = "󰖙"  # nf-md-weather_sunny
        elif any(w in condition_clean for w in ["rain", "drizzle", "shower"]):
            icon = "󰖗"  # nf-md-weather_rainy
        elif "snow" in condition_clean:
            icon = "󰖘"  # nf-md-weather_snowy
        elif any(w in condition_clean for w in ["thunder", "storm"]):
            icon = ""  # nf-md-weather_lightning
        elif any(w in condition_clean for w in ["fog", "mist", "haze"]):
            icon = "󰖑"  # nf-md-weather_fog
        else:
            icon = "󰖕"  # nf-md-weather_partly_cloudy (fallback)

        # Parse numeric temperature value (handles - / + signs)
        temp_match = re.search(r'[-+]?\d+', temp)
        if temp_match:
            temp_val = int(temp_match.group())
            if temp_val < 10:
                temp_class = "temp-cold"
            elif temp_val < 25:
                temp_class = "temp-warm"
            else:
                temp_class = "temp-hot"
        else:
            temp_class = "temp-unknown"

        output = {
            "icon": icon,
            "temp": temp.strip(),
            "feels": feels.strip(),
            "desc": condition.strip(),
            "temp_class": temp_class
        }

    except Exception:
        output = {
            "icon": "󰅚",  # nf-md-alert_circle_outline
            "temp": "?",
            "feels": "?",
            "desc": "Error",
            "temp_class": "temp-unknown"
        }

    print(json.dumps(output))

if __name__ == "__main__":
    get_weather()
