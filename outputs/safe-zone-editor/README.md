# SafeZone dashboard prototype

An editable, dependency-free web prototype based on the PS-191 brief: dynamic hazard zonation, carrying-capacity assessment, and immediate relocation prioritization.

## Run

Open `index.html` in a modern web browser. No server, build step, or external package is required. For local development with a server, run `npx serve .` from this folder if Node.js is available.

## Included interactions

- **Run assessment** refreshes the mock rainfall, soil saturation, risk area, and relocation values.
- **Carrying capacity** sliders calculate the CCI from the brief's formula and update the recommendation.
- Navigation shows the command centre, capacity, and relocation views.

The values, zones, and households are illustrative and should be replaced with validated GIS, weather, sensor, and demographic sources before operational use.
