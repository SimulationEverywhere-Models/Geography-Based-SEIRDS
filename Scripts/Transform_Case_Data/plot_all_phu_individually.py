#!/usr/bin/env python
# coding: utf-8
# Original author: Glenn - 27/04/2021

# In[1]:

import pandas as pd
from copy import deepcopy
import matplotlib
import pathlib
import matplotlib.pyplot as plt

#%%
case_fpath = 'output/timeseries/'
PLOT_DIR1 = 'cases_plotted_per_region/full/'
PLOT_DIR2 = 'cases_plotted_per_region/first50/'
pathlib.Path(PLOT_DIR1).mkdir(parents=True, exist_ok=True)
pathlib.Path(PLOT_DIR2).mkdir(parents=True, exist_ok=True)
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

linewidth = 3
font = matplotlib.font_manager.FontProperties()
font.set_size('small')
x = deepcopy(phu_df['IntegerDay'])
phu_df.drop(columns='IntegerDay', inplace=True)

#%%

# iterate over all phus and plot the full span of cases
for phu_series in phu_df.iteritems():
    
    fig, ax = plt.subplots(figsize=(15,6))
    title = 'Daily New Infections for ' + phu_series[0] + ' ' + date_range
    ax.plot(x, phu_series[1], label=phu_series[0], linewidth=linewidth)
    plt.legend(loc='upper left', prop=font)
    plt.title(title)
    plt.xlabel("Time (days)")
    plt.ylabel('New Infections')
    plt.savefig(PLOT_DIR1 + phu_series[0] + '.png')
    plt.close(fig)

#%%

x2 = x[0:50]

#%%

# iterate over all phus and plot only the first 50 days of cases
for phu_series in phu_df.iteritems():
    
    fig, ax = plt.subplots(figsize=(15,6))
    y = phu_series[1][0:50]
    title = 'Daily New Infections for ' + phu_series[0] + ' ' + date_range
    ax.plot(x2, y, label=phu_series[0], linewidth=linewidth)
    plt.legend(loc='upper left', prop=font)
    plt.title(title)
    plt.xlabel("Time (days)")
    plt.ylabel('New Infections')
    plt.savefig(PLOT_DIR2 + phu_series[0] + '.png')
    plt.close(fig)
    
#%%