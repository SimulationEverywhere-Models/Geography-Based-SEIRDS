# Run while setting up the model, only needs to be run once
#cmake "CMakeLists.txt"
#make
cd Scripts/Transform_Case_Data
python transform_case_data.py
python plot_all_phu_individually.py
python plot_all_phu_infected.py