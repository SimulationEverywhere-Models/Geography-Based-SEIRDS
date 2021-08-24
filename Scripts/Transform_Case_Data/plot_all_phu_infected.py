#!/usr/bin/env python
# coding: utf-8
# Original author: Glenn - 27/04/2021

# In[1]:

import pandas as pd
from copy import deepcopy
import matplotlib
import pathlib
import matplotlib.pyplot as plt
import local_module.regions as regions

#%%
case_fpath = 'output/timeseries/'
PLOT_DIR = 'cases_plotted/'
pathlib.Path(PLOT_DIR).mkdir(parents=True, exist_ok=True)
file_mappings = pd.read_csv('output/sim_file_mappings.csv')

data = {}
for row in file_mappings.iterrows():
    casefile = case_fpath + row[1]['casefile']
    cdf = pd.read_csv(casefile)
    region_abbr = row[1]['casefile'].rsplit('_')[0]
    data[region_abbr] = [region_abbr, cdf]

#%%

# extract beginning and end dates of the case reports
dates = data[region_abbr][1]['Date']
start_day = dates[0]
end_day = dates[len(dates)-1]
start_day = str(start_day)
end_day = str(end_day)
date_range = start_day + ' to ' + end_day

# make a df of IntergerDay, InfectedRegion1...InfectedRegion2
# plot sim_infected, active_cases, x_axis

phu_df = pd.DataFrame(deepcopy(data[region_abbr][1]['IntegerDay']))

#%%
# create a dataframe of NewInfected of each region under the key of it region name
for key in data:
    region_name = data[key][0]
    region_df = data[key][1]
    phu_df[region_name] = region_df['NewInfected']

#%% - Define the indivudal plots to draw

fig, ax = plt.subplots(figsize=(15,6))
linewidth = 3
font = matplotlib.font_manager.FontProperties()
font.set_size('small')
x = deepcopy(phu_df['IntegerDay'])
phu_df.drop(columns='IntegerDay', inplace=True)

#%%

# iterate over all phus and plot all that appear in regions.sw_regions
for phu_series in phu_df.iteritems():
    
    try: 
        i = regions.sw_regions.index(phu_series[0])
        inList = True
    except ValueError: 
        inList = False
    
    if inList:
        ax.plot(x, phu_series[1], label=phu_series[0], linewidth=linewidth)

plt.legend(loc='upper left', prop=font)
plt.title('Daily New Infections for SouthWest PHU Regions ' + date_range)
plt.xlabel("Time (days)")
plt.ylabel('New Infections')
plt.savefig("cases_plotted/southwest_phu_active_cases.png")
plt.close(fig)

fig, ax = plt.subplots(figsize=(15,6))

for phu_series in phu_df.iteritems():
    
    try: 
        i = regions.cw_regions.index(phu_series[0])
        inList = True
    except ValueError: 
        inList = False
    
    if inList:
        ax.plot(x, phu_series[1], label=phu_series[0], linewidth=linewidth)

plt.legend(loc='upper left', prop=font)
plt.title('Daily New Infections for CentralWest PHU Regions ' + date_range)
plt.xlabel("Time (days)")
plt.ylabel('New Infections')
plt.savefig("cases_plotted/centralwest_phu_active_cases.png")
plt.close(fig)

fig, ax = plt.subplots(figsize=(15,6))

for phu_series in phu_df.iteritems():
    
    try: 
        i = regions.ce_regions.index(phu_series[0])
        inList = True
    except ValueError: 
        inList = False
    
    if inList:
        ax.plot(x, phu_series[1], label=phu_series[0], linewidth=linewidth)
        
plt.legend(loc='upper left', prop=font)
plt.title('Daily New Infections for CentralEast + Toronto PHU Regions ' + date_range)
plt.xlabel("Time (days)")
plt.ylabel('New Infections')
plt.savefig("cases_plotted/centraleast_toronto_phu_active_cases.png")
plt.close(fig)

fig, ax = plt.subplots(figsize=(15,6))

for phu_series in phu_df.iteritems():   
    
    try: 
        i = regions.e_regions.index(phu_series[0])
        inList = True
    except ValueError: 
        inList = False
    
    if inList:
        ax.plot(x, phu_series[1], label=phu_series[0], linewidth=linewidth)

plt.legend(loc='upper left', prop=font)
plt.title('Daily New Infections for East PHU Regions ' + date_range)
plt.xlabel("Time (days)")
plt.ylabel('New Infections')
plt.savefig("cases_plotted/east_phu_active_cases.png")
plt.close(fig)
        
fig, ax = plt.subplots(figsize=(15,6))

for phu_series in phu_df.iteritems():   
    
    try: 
        i = regions.n_regions.index(phu_series[0])
        inList = True
    except ValueError: 
        inList = False
    
    if inList:
        ax.plot(x, phu_series[1], label=phu_series[0], linewidth=linewidth)

plt.legend(loc='upper left', prop=font)
plt.title('Daily New Infections for North PHU Regions ' + date_range)
plt.xlabel("Time (days)")
plt.ylabel('New Infections')
plt.savefig("cases_plotted/north_phu_active_cases.png")
plt.close(fig)
