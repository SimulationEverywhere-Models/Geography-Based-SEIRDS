# Original author: Glenn - 24/03/2021

#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import shutil

#%%

sim_fpath = 'sim_timeseries/'
case_fpath = '../../case_data_parser/output/ontario_phu/'
output_path = 'output/'
    
COLOR_SUSCEPTIBLE = 'xkcd:blue'
COLOR_INFECTED = 'xkcd:red'
COLOR_EXPOSED = 'xkcd:sienna'
COLOR_RECOVERED = 'xkcd:green'
COLOR_DEAD = 'xkcd:black'

font = {'family' : 'DejaVu Sans',
        'weight' : 'normal',
        'size'   : 16}

matplotlib.rc('font', **font)
columns = ["time", "susceptible", "exposed", "infected", "recovered", "new_exposed", "new_infected", "new_recovered", "deaths"]

#%%

# make empty output folder
shutil.rmtree(output_path, ignore_errors=True)
try: 
    os.mkdir(output_path) 
except OSError as error: 
    print(error)
    
file_mappings = pd.read_csv('../../case_data_parser/output/ontario_phu/sim_file_mappings.csv')

for row in file_mappings.iterrows():
    
    # open casefile data
    casefile = case_fpath + row[1]['casefile']
    cdf = pd.read_csv(casefile)
    region_abbr = row[1]['casefile'].rsplit('_')[0]
    
    # open simfile data
    simfile = row[1]['simfile']
    
    # in the simfilename is the region number which needs to be extracted
    # it is located between the first two underscores
    region_id = simfile.rsplit('_')[1]
    simfile = sim_fpath + 'region_' + region_id + '/' + row[1]['simfile']
    sdf = pd.read_csv(simfile)
    
    # need to plot cdf ['TotalActive'] and ['TotalFatal'] vs sdf['I'] and ['D']
    active_cases = cdf['TotalActive']
    total_deaths = cdf['TotalDeaths']
    case_time = cdf['IntegerDay']
    sim_infected = sdf[' I']
    sim_deaths = sdf[' D']
    sim_time = sdf['sim_time']
    x_axis = sim_time
    
    # truncate the longer series so they are the same length
    num_points = min(len(sim_time), len(case_time))
    
    if(len(sim_time) > num_points):
        d = len(sim_time) - num_points
        x_axis = case_time
        
        # remove d entries from the end of sim_infected, sim_deaths
        for i in range(d):
            tail = len(sim_infected)-1
            sim_infected.drop(index=tail, inplace=True)
            sim_deaths.drop(index=tail, inplace=True)
    elif(len(case_time) > num_points):
        d = len(case_time) - num_points
        
        # remove d entries from the end of active_cases, total_deaths
        for i in range(d):
            tail = len(active_cases)-1
            active_cases.drop(index=tail, inplace=True)
            total_deaths.drop(index=tail, inplace=True)
            
    # determine filenames for infected and fatal plots
    infection_file = "intected_"+region_abbr + ".png"
    deaths_file = "deaths_"+region_abbr + ".png"
    
    # plot sim_infected, active_cases, x_axis
    fig, ax = plt.subplots(figsize=(15,6))
    linewidth = 2

    x = x_axis
    ax.plot(x, sim_infected, label="sim_infected", color=COLOR_INFECTED, linewidth=linewidth)
    ax.plot(x, active_cases, label="active_cases", color=COLOR_EXPOSED, linewidth=linewidth)
    plt.legend(loc='upper right')
    plt.margins(0,0)
    plt.title('Active Cases for ' + region_abbr)
    plt.xlabel("Time (days)")
    plt.ylabel("Number Active Infections")
    plt.savefig(output_path+infection_file)
    plt.close(fig)
    
    # plot sim_deaths, total_deaths, x_axis
    fig, ax = plt.subplots(figsize=(15,6))
    linewidth = 2

    x = x_axis
    ax.plot(x, sim_deaths, label="sim_deaths", color=COLOR_DEAD, linewidth=linewidth)
    ax.plot(x, total_deaths, label="total_deaths", color=COLOR_SUSCEPTIBLE, linewidth=linewidth)
    plt.legend(loc='upper right')
    plt.margins(0,0)
    plt.title('Total Fatalities for ' + region_abbr)
    plt.xlabel("Time (days)")
    plt.ylabel("Total Deaths")
    plt.savefig(output_path+deaths_file)
    plt.close(fig)
