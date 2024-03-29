# Written by Glenn
# This script assumes that cmake has been run, and that the terminal environment includes java, python and python geopandas

# defining commands used
SIMULATE="./pandemic-geographical_model ../config/scenario_ontario_phu.json 500"
PARSE_MSG_LOGS="java -jar sim.converter.glenn.jar "input" "output""

# defining directories used
VISUALIZATION_DIR="GIS_Viewer/ontario/simulation_runs/run1"

# make directories if they don't exist
mkdir -p Scripts/Input_Generator/output
mkdir -p Scripts/Msg_Log_Parser/input
mkdir -p Scripts/Msg_Log_Parser/output
mkdir -p ${VISUALIZATION_DIR}

# generate a scenario json file for model input, save it in the config folder
echo "Generating Scenario:"
cd Scripts/Input_Generator
python generate_ontario_phu_json2.py
cp output/scenario_ontario_phu.json ../../config

# run the model
cd ../../bin
echo
echo "Executing model:"
echo ${SIMULATE}
${SIMULATE}

# generate SIRDS graphs
echo
echo "Generating graphs and stats (will be found in logs folder):"
cd ../Scripts/Graph_Generator/
python graph_per_regions.py
python graph_aggregates.py
cd ../..

# Copy the message log + scenario to message log parser's input
# Note this deletes the contents of input/output folders of the message log parser before executing
echo
echo "Copying simulation results to message log parser:"

rm -f Scripts/Msg_Log_Parser/input/*
rm -rf "Scripts/Msg_Log_Parser/output\pandemic_messages"
rm -f Scripts/Msg_Log_Parser/*.zip
rm -f Scripts/Msg_Log_Parser/output/*
cp config/scenario_ontario_phu.json Scripts/Msg_Log_Parser/input
cp logs/pandemic_messages.txt Scripts/Msg_Log_Parser/input

# Run the message log parser
echo
echo "Running message log parser:"
cd Scripts/Msg_Log_Parser
echo ${PARSE_MSG_LOGS}
${PARSE_MSG_LOGS}
echo
unzip "output\pandemic_messages.zip" -d output

# Copy the converted message logs to GIS Web Viewer Folder
echo
echo "Copying converted files to: ${VISUALIZATION_DIR}"
cd ../..
cp Scripts/Msg_Log_Parser/output/messages.log ${VISUALIZATION_DIR}
cp Scripts/Msg_Log_Parser/output/structure.json ${VISUALIZATION_DIR}

# Copy stats folders to from logs/stats/ case_data_comparison/provinces/sim_timeseries
echo
echo "Generating comparison to PHU case data"
rm -rf Scripts/Compare_Sim_Cases/sim_timeseries
cp -r logs/stats Scripts/Compare_Sim_Cases/sim_timeseries
cd Scripts/Compare_Sim_Cases
python compare_phus.py
cd ../..
rm -rf logs/output
rm -rf logs/case_data_comparison
mv Scripts/Compare_Sim_Cases/output logs/case_data_comparison
