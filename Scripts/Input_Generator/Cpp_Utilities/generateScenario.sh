# make folder "output" if it doesn't exist already
cd ..
mkdir -p output
cd Cpp_Utilities

# print information for user
echo
echo "Compiling json post processor:"
make convertScenario
echo
echo "Generating neighborhoods:"
echo "NOTE - 'Invalid dauid found' indicates a cell with zero population, not an error"
echo
# create pre_preprocessing.json
python generate_cadmium_json_cpp.py
# create format pre_preprocessing.json
echo
echo "Running json post processor:"
./convertScenario ../input/pre_processing.json
echo "done - result is in output folder"
