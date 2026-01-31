import json
import requests

try:
    weather = requests.get("https://wttr.in/Cairo?format=j1").json()
    
    current = weather['current_condition'][0]
    temp = int(current['FeelsLikeC'])
    code = current['weatherCode']
    
    # Define icons (Nerd Fonts)
    icons = {"113": "☀️", "116": "⛅", "119": "☁️", "122": "☁️", "143": "🌫", "200": "⛈"}
    icon = icons.get(code, "✨")

    # Determine CSS class based on temperature
    if temp <= 0:
        status = "freezing"
    elif 0 < temp <= 15:
        status = "cold"
    elif 15 < temp <= 25:
        status = "warm"
    elif 25 < temp <= 32:
        status = "hot"
    else:
        status = "critical"

    output = {
        "text": f"{icon} {temp}°C",
        "tooltip": f"Condition: {current['weatherDesc'][0]['value']}\nHumidity: {current['humidity']}%",
        "class": status
    }
    print(json.dumps(output))

except Exception as e:
    print(json.dumps({"text": "Weather Error", "class": "error"}))
