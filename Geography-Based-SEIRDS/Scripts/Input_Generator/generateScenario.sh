echo
echo "Compiling json post processor:"
make
echo
echo "Generating neighborhoods:"
echo "NOTE - 'Invalid dauid found' indicates a cell with zero population, not an error"
echo
python generate_cadmium_json.py
echo
echo "Running json post processor:"
./convertScenario input/pre_processing.json
echo "done - result is in output folder"
