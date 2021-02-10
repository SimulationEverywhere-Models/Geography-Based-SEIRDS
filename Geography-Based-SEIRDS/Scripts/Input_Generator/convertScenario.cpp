// Written by Glenn Davidson
// Converts scenario.json from celldevs-depreciated format to cadmium master format

// input: takes a json filename as an input argument
// output: writes result to output/scenario.json

// Ideally the functionality of this program would be implemented entirely by generate_cadmium_json.py,
// but I am more familiar with C++, will try to implement it fully in python going forward

#include <iostream>
#include <fstream>
#include <nlohmann/json.hpp>

#define OUPUT_FILENAME "output/scenario.json"
#define FIELDS_FILE "input/fields.json"
#define INFECTED_CELL_FILE "input/infectedCell.json"

using json = nlohmann::json;

int main(int argc, char ** argv) {
    if (argc < 2) {
        std::cout << "Error : Program must be given a json as an argument";
        std::cout << argv[0] << std::endl;
        return -1;
    }

    std::ifstream file_existence_checker1{argv[1]};
    std::ifstream file_existence_checker2{FIELDS_FILE};
    std::ifstream file_existence_checker3{INFECTED_CELL_FILE};

    if(!file_existence_checker1.is_open()) {
        throw std::runtime_error{"Unable to open the file: " + std::string{argv[1]}};
    }
    if(!file_existence_checker2.is_open()) {
        throw std::runtime_error{"Unable to open the file: " + std::string{FIELDS_FILE}};
    }
    if(!file_existence_checker3.is_open()) {
        throw std::runtime_error{"Unable to open the file: " + std::string{INFECTED_CELL_FILE}};
    }

    // read all input files into json objects
    std::string scenario_config_file_path = argv[1];
    std::ifstream scenarioFile;
    scenarioFile.open(scenario_config_file_path);
    json jScenario;
    scenarioFile >> jScenario;
    scenarioFile.close();

    std::ifstream fieldsFile;
    fieldsFile.open(FIELDS_FILE);
    json jFields;
    fieldsFile >> jFields;
    fieldsFile.close();

    std::ifstream infectedFile;
    infectedFile.open(INFECTED_CELL_FILE);
    json jInfection;
    infectedFile >> jInfection;
    infectedFile.close();

    std::ofstream outputFile;
    outputFile.open(OUPUT_FILENAME);
    json outputJson;

    // read the name of the infected cell
    std::string infectedCell = jInfection.value("cell_id", "non-existent");

    // iterate over all cells in input file, format them, and then write them to output scenario.json
    for(int i = 0; i < jScenario["cells"].size(); i++){

        // read the next cell in iteration
        json nextCell = jScenario["cells"].at(i);
        std::string cellName = nextCell["cell_id"];

        // erase the cell_id object, no longer used
        nextCell.erase(nextCell.find("cell_id"));

        // read the old format neighborhood into object
        json nextNH = nextCell["neighborhood"];

        // create another object to hold the formatted neighborhood result
        json neighborhood;

        // iterate over all members of the cell's neighborhood
        for (int j = 0; j < nextNH.size(); j++){

            // read nextneighbor in neighborhood
            json neighbor = nextNH.at(j);
            // reformat cell_id and vicinity
            std::string cellName = neighbor["cell_id"];
            json vicinity = neighbor["vicinity"];
            double correlation;
            vicinity.at("correlation").get_to(correlation);
            json inf_k_factor = vicinity.at("infection_correction_factors");
            neighbor.erase(neighbor.find("cell_id"));
            neighbor.erase(neighbor.find("vicinity"));
            neighbor["correlation"] = correlation;
            neighbor["infection_correction_factors"] = inf_k_factor;
            // insert the resulting neighbor entry in neighborhood
            neighborhood[cellName] = neighbor;
        }
        
        // overwrite the neighborhood with properly formatted neighborhood
        nextCell["neighborhood"] = neighborhood;
        
        // if this is an infected cell, overwrite the state object
        if(cellName == infectedCell){
            // overwrite susceptible, infected, recovered, fatalities, but leave the rest of the state object as is
            nextCell["state"]["susceptible"] = jInfection["state"]["susceptible"];
            nextCell["state"]["infected"] = jInfection["state"]["infected"];
            nextCell["state"]["exposed"] = jInfection["state"]["exposed"];
            nextCell["state"]["recovered"] = jInfection["state"]["recovered"];
            nextCell["state"]["fatalities"] = jInfection["state"]["fatalities"];
        }
        outputJson["cells"][cellName] = nextCell;
    }

    // format and insert default scenario at the top of "cells"
    json jDefault = jScenario["default"];
    json neighborhood = jDefault["neighborhood"];
    std::string defaultID = neighborhood["cell_id"];
    json vicinity = neighborhood["vicinity"];
    
    // extract correlation and infection correction factor
    double correlation;
    vicinity.at("correlation").get_to(correlation);
    json inf_k_factor = vicinity.at("infection_correction_factors");

    // erase old objects
    neighborhood.erase(neighborhood.find("cell_id"));
    neighborhood.erase(neighborhood.find("vicinity"));

    // place vicinity items into object under default id index, without a vicinity label
    neighborhood[defaultID]["correlation"] = correlation;
    neighborhood[defaultID]["infection_correction_factors"] = inf_k_factor;
    jDefault["neighborhood"] = neighborhood;

    // write the default cell state to output json
    outputJson["cells"]["default"] = jDefault;

    // insert "fields" object for message log parser
    outputJson["fields"] = jFields["fields"];

    // write the scenario json file
    // this output file is in the format to be input to the model
    outputFile << outputJson.dump(4);
    outputFile.close();
    return 0;
}

