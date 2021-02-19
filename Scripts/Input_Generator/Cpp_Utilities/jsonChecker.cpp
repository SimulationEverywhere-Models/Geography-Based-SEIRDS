// Written by Glenn Davidson
// Converts scenario.json from celldevs-depreciated format to cadmium master format

// input: takes a json filename as an input argument
// output: writes result to output/scenario.json

// Ideally the functionality of this program would be implemented entirely by generate_cadmium_json.py,
// but I am more familiar with C++, will try to implement it fully in python going forward

#include <iostream>
#include <fstream>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

int main(int argc, char ** argv) {
    if (argc < 2) {
        std::cout << "Error : Program must be given a json as an argument";
        std::cout << argv[0] << std::endl;
        return -1;
    }

    std::ifstream file_existence_checker1{argv[1]};

    if(!file_existence_checker1.is_open()) {
        throw std::runtime_error{"Unable to open the file: " + std::string{argv[1]}};
    }
    

    // read all input files into json objects
    std::string scenario_config_file_path = argv[1];
    std::ifstream scenarioFile;
    scenarioFile.open(scenario_config_file_path);
    json jScenario;
    scenarioFile >> jScenario;
    scenarioFile.close();

    std::cout << "No error thrown, JSON is valid format" << std::endl;
    return 0;
}

