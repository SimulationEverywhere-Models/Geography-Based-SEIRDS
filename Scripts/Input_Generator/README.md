## Scenario Generation

The python scripts in this folder generate scenarios based on the geographical data in the cadmum_gis folder and in the inputs folder of this directory.

Requirements before running:
the python environment must have geopandas installed before running generateScenario.sh

Inputs:
- the default cell state can be set in `input_*/default.json`
- one or more infected cells can be set in `input_*/infectedCells.json`
- `input/fields.json` inserts information for message log parsing to be used with GIS Web viewer v2

Where the * wildcard is the region name.