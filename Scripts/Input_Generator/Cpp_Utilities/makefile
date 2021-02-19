CC=g++
CFLAGS=-std=c++17

INCLUDEJSON=-I/home/eldrazi/CADMIUM/Cadmium-Simulation-Environment/cadmium/json/include

all: convertScenario.cpp jsonChecker.cpp
	$(CC) -g $(CFLAGS) $(INCLUDEJSON) convertScenario.cpp -o convertScenario
	$(CC) -g $(CFLAGS) $(INCLUDEJSON) jsonChecker.cpp -o jsonChecker

convertScenario: convertScenario.cpp
	$(CC) -g $(CFLAGS) $(INCLUDEJSON) convertScenario.cpp -o convertScenario

jsonChecker: jsonChecker.cpp
	$(CC) -g $(CFLAGS) $(INCLUDEJSON) jsonChecker.cpp -o jsonChecker	
