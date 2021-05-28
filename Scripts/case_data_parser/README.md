Case Data Parser
===
The case data parser tool transforms the Ontario PHU case data to a format the the model can be compared against. The case data contains the the dates of confirmed cases per public health unit. The tool transforms each case into an active infection lasting 10 days, and generates a time series of all active infections per region.

The input is located in data/PHU, the output is generated in output/ontario_phu.

Note that the model is capable of generating the new reported cases as an output seperately from the number of active infections, and a comparison can be drawn in this way too.