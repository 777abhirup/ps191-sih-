# SafeZone dashboard prototype

An editable web prototype based on the PS-191 brief: dynamic hazard zonation, carrying-capacity assessment, and immediate relocation prioritization.

## Run

Open `index.html` in a modern web browser. No build step is required. The interactive map, base tiles, and live weather request require an internet connection. For local development with a server, run `npx serve .` from this folder if Node.js is available.

## Interactions

- **Interactive map** uses Leaflet with OpenStreetMap base tiles. Click a zone or table row to smoothly fly to the selected habitation and inspect its current HSI / CCI / RPS.
- **Refresh live data** retrieves recent weather-model data from Open-Meteo for the selected location. It calculates preceding 24-hour rainfall and normalises the 0-7 cm soil-moisture value before updating HSI.
- **Carrying capacity** sliders calculate the CCI from the brief's formula and update the recommendation.
- Navigation switches between the command centre, capacity, and relocation views with transitions.

## Data and safety note

Live weather is suitable only as a prototype input. The habitation baselines, polygons, safe-zone capacity, carrying-capacity inputs, household data, and risk thresholds are illustrative. Replace them with agency-validated GIS, sensor, hydrology, geotechnical, shelter, and demographic datasets before operational use. Do not use this prototype to issue evacuation instructions.

### Sources

- Map tiles: OpenStreetMap contributors (shown in map attribution).
- Weather: Open-Meteo Forecast API; it returns hourly precipitation and soil-moisture model data for the selected coordinates.
