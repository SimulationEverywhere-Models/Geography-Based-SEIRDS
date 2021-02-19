the script generate_cadmium_json_g1.py will create a scenario.json for the Geography-Based-Model, the C++ utilities are no longer used
the inputs to the process are found in the input folder, the outputs from this process will be located in the output folder

Requirements before running:
the python environment must have geopandas installed before running generateScenario.sh

Inputs/Outputs:
the default cell state can be set in input/default.json
the infected cell can be set in input/infectedCell.json
input/fields.json inserts information for message log parsing to be used with GIS Web viewer v2
generate_cadmium_json_g1.py will create scenario.json in output folder

Notes:
- The current inputs are for SEIRDS model, the Geography-Based-Model (SIRDS) can be accomodated by changing the files in the input folder.
- The updated generation of scenario.json was previously done in part in C++, this program is no longer required, but it is included in Cpp_Utilities