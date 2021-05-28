Case Data Comparison Tool
===

These scripts are useful in comparing the model results to the reported ontario PHU case data.

The script 'plot_all_phu_infected.py' will plot the infection time series data of all ontario PHUS. It is useful in intuitiing what the model initial conditions should be, and was also used for generating some of the figures in writing. Is uses the case_data_parser output as its input, and outputs the plots to the cases plotted folder.

The script 'compare_phus.py' is used to plot the model results and case data in the same plots for comparison. It takes the simulation time series and case time series, and for each region plots the infection and fatality time series comparison. The 'sim_file_mappings.csv' is used to match simulation time series files to case time series files. Integer IDs are used in the simulation time series files to identify regions because they are used consistently in Geographical Boundary files.