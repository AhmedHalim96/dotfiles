#!/bin/bash

# %C = Condition, %t = Actual Temp, %f = Feels Like
# We use '+' as a delimiter to make parsing easier
weather_data=$(curl -s "wttr.in/Cairo?format=%C+%t+%f")

# Check if curl failed
if [ $? -ne 0 ] || [ -z "$weather_data" ]; then
  echo "{\"icon\": \"\", \"temp\": \"?\", \"feels\": \"?\", \"desc\": \"Error\"}"
  exit 1
fi

# Split the data using '+' as the delimiter
# Using IFS (Internal Field Separator) is safer for conditions with spaces
IFS='+' read -r condition temp feels <<<"$weather_data"

# Clean up the strings (remove leading/trailing spaces and lowercase the condition)
condition_lower=$(echo "$condition" | tr '[:upper:]' '[:lower:]')

# Map conditions to Font Awesome 6 Icons
case $condition_lower in
*cloud*) icon="" ;;                 # fa-cloud
*clear* | *sun*) icon="" ;;         # fa-sun
*rain* | *drizzle*) icon="" ;;      # fa-cloud-showers-heavy
*snow*) icon="" ;;                  # fa-snowflake
*thunder*) icon="" ;;               # fa-bolt
*fog* | *mist* | *haze*) icon="" ;; # fa-smog
*) icon="" ;;                       # fa-cloud-sun (fallback)
esac

# Return JSON with the new 'feels' field
echo "{\"icon\": \"$icon\", \"temp\": \"$temp\", \"feels\": \"$feels\", \"desc\": \"$condition\"}"
