#!/usr/bin/env python
# coding: utf-8
"""
23/08/2021

@author: glenn
"""

# In[1]:

import os
import pandas as pd
import shutil
import matplotlib.pyplot as plt
import local_module.plot_settings as p

#%%

SIM_FOLDER = 'sim_timeseries/'
CASE_FOLDER = '../Transform_Case_Data/output/timeseries/'
MAP_FILE = '../Transform_Case_Data/output/sim_file_mappings.csv'
OUTPUT_NEW_INFECTED = 'output/newinfected/'
OUTPUT_ACTIVE_INFECTED = 'output/activeinfected/'
OUTPUT_DEATHS = 'output/deaths/'
OUTPUT_FOLDER = 'output/'
    
#%%

# make empty output folders
shutil.rmtree(OUTPUT_FOLDER, ignore_errors=True)
try: 
    os.mkdir(OUTPUT_FOLDER) 
except OSError as error: 
    print(error)  
try: 
    os.mkdir(OUTPUT_NEW_INFECTED) 
except OSError as error: 
    print(error)  
try: 
    os.mkdir(OUTPUT_ACTIVE_INFECTED) 
except OSError as error: 
    print(error)
try: 
    os.mkdir(OUTPUT_DEATHS) 
except OSError as error: 
    print(error)
    
file_mappings = pd.read_csv(MAP_FILE)

#%%
for row in file_mappings.iterrows():
    
    # open casefile data
    casefile = CASE_FOLDER + row[1]['casefile']
    case_df = pd.read_csv(casefile)
    region_abbr = row[1]['casefile'].rsplit('_')[0]
    
    # open simfile data
    simfile = row[1]['simfile']
    
    # in the simfilename is the region number which needs to be extracted
    # it is located between the first two underscores
    region_id = simfile.rsplit('_')[1]
    simfile = SIM_FOLDER + 'region_' + region_id + '/' + row[1]['simfile']
    sim_df = pd.read_csv(simfile)
    
    # need to plot case_df ['NewInfected'] and ['TotalFatal'] vs sim_df['I'] and ['D']
    new_infected = case_df['NewInfected']
    active_infected = case_df['ActiveInfected']
    total_deaths = case_df['TotalDeaths']
    case_time = case_df['IntegerDay']
    sim_new_infected = sim_df['New_I']
    sim_active_infected = sim_df['I']
    sim_deaths = sim_df['D']
    sim_time = sim_df['sim_time']
    x_axis = sim_time
    
    # truncate the longer series so they are the same length
    num_points = min(len(sim_time), len(case_time))
    
    if(len(sim_time) > num_points):
        d = len(sim_time) - num_points
        x_axis = case_time
        
        # remove d entries from the end of sim_new_infected, sim_deaths
        for i in range(d):
            tail = len(sim_new_infected)-1
            sim_new_infected.drop(index=tail, inplace=True)
            sim_active_infected.drop(index=tail, inplace=True)
            sim_deaths.drop(index=tail, inplace=True)
    elif(len(case_time) > num_points):
        d = len(case_time) - num_points
        
        # remove d entries from the end of new_infected, total_deaths
        for i in range(d):
            tail = len(new_infected)-1
            new_infected.drop(index=tail, inplace=True)
            active_infected.drop(index=tail, inplace=True)
            total_deaths.drop(index=tail, inplace=True)
            
    # determine filenames for infected and fatal plots
    new_infection_file = "newinfected"+region_abbr + ".png"
    active_infection_file = "activeinfected"+region_abbr + ".png"
    deaths_file = "deaths_"+region_abbr + ".png"
    
    # plot sim_new_infected, new_infected, x_axis
    fig, ax = plt.subplots(figsize=(15,6))
    lw = 2

    x = x_axis
    ax.plot(x, sim_new_infected, label="simulation", color=p.COLOR_INFECTED, linewidth=lw)
    ax.plot(x, new_infected, label="new_infected", color=p.COLOR_EXPOSED, linewidth=lw)
    plt.legend(loc='upper right')
    plt.margins(0,0)
    plt.title('New Infected for ' + region_abbr)
    plt.xlabel("Time (days)")
    plt.ylabel("Number New Infections")
    plt.savefig(OUTPUT_NEW_INFECTED+new_infection_file)
    plt.close(fig)
    
    # plot sim_active_infected, active_infected, x_axis
    fig, ax = plt.subplots(figsize=(15,6))
    lw = 2

    x = x_axis
    ax.plot(x, sim_active_infected, label="simulation", color=p.COLOR_INFECTED, linewidth=lw)
    ax.plot(x, active_infected, label="active_infected", color=p.COLOR_EXPOSED, linewidth=lw)
    plt.legend(loc='upper right')
    plt.margins(0,0)
    plt.title('Active Infected for ' + region_abbr)
    plt.xlabel("Time (days)")
    plt.ylabel("Number Active Infections")
    plt.savefig(OUTPUT_ACTIVE_INFECTED+active_infection_file)
    plt.close(fig)
    
    # plot sim_deaths, total_deaths, x_axis
    fig, ax = plt.subplots(figsize=(15,6))
    lw = 2

    x = x_axis
    ax.plot(x, sim_deaths, label="simulation", color=p.COLOR_DEAD, linewidth=lw)
    ax.plot(x, total_deaths, label="total_deaths", color=p.COLOR_SUSCEPTIBLE, linewidth=lw)
    plt.legend(loc='upper right')
    plt.margins(0,0)
    plt.title('Total Fatalities for ' + region_abbr)
    plt.xlabel("Time (days)")
    plt.ylabel("Total Deaths")
    plt.savefig(OUTPUT_DEATHS+deaths_file)
    plt.close(fig)
