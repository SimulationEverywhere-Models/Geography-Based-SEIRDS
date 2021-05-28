# Original author: Glenn - 27/04/2021

#!/usr/bin/env python
# coding: utf-8

# In[1]:

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from copy import deepcopy
from pathlib import Path

#%%

phu_dict = {
    'GreyBruceHealthUnit' : 'GreyBruce',
    'HuronPerthHealthUnit' : 'HuronPerth',
    'Middlesex-LondonHealthUnit' : 'Middlesex',
    'SouthwesternPublicHealth' : 'Southwestern',
    'LambtonPublicHealth' : 'Lambton',
    'Chatham-KentHealthUnit' : 'Chatham',
    'Windsor-EssexCountyHealthUnit' : 'Windsor',
    'Wellington-Dufferin-GuelphHealthUnit' : 'Wellington',
    'HaltonRegionHealthDepartment' : 'Halton',
    'RegionofWaterlooPublicHealth' : 'Waterloo',
    'HamiltonPublicHealthServices' : 'Hamilton',
    'NiagaraRegionPublicHealthDepartment' : 'Niagara',
    'BrantCountyHealthUnit' : 'Brant',
    'Haldimand-NorfolkHealthUnit' : 'Haldimand',
    'PeelPublicHealth' : 'Peel',
    'YorkRegionPublicHealth' : 'York',
    'TorontoPublicHealth' : 'Toronto',
    'SimcoeMuskokaDistrictHealthUnit' : 'Simcoe',
    'DurhamRegionHealthDepartment' : 'Durham',
    'HaliburtonKawarthaPineRidgeDistrictHealthUnit' : 'Haliburton',
    'PeterboroughPublicHealth' : 'Peterborough',
    'RenfrewCountyandDistrictHealthUnit' : 'Renfrew',
    'HastingsandPrinceEdwardCountiesHealthUnit' : 'Hastings',
    'KingstonFrontenacandLennoxandAddingtonHealthUnit' : 'KFLA',
    'LeedsGrenvilleandLanarkDistrictHealthUnit' : 'Leeds',
    'OttawaPublicHealth' : 'Ottawa',
    'EasternOntarioHealthUnit' : 'Eastern',
    'NorthBayParrySoundDistrictHealthUnit' : 'NorthBay',
    'TimiskamingHealthUnit' : 'Timiskaming',
    'SudburyandDistrictHealthUnit' : 'Sudbury',
    'AlgomaPublicHealthUnit' : 'Algoma',
    'PorcupineHealthUnit' : 'Porcupine',
    'ThunderBayDistrictHealthUnit' : 'ThunderBay',
    'NorthwesternHealthUnit' : 'Northwestern'
}

sw_regions = [
    'GreyBruceHealthUnit',
    'HuronPerthHealthUnit',
    'Middlesex-LondonHealthUnit',
    'SouthwesternPublicHealth',
    'LambtonPublicHealth',
    'Chatham-KentHealthUnit',
    'Windsor-EssexCountyHealthUnit']
cw_regions = [
    'Wellington-Dufferin-GuelphHealthUnit',
    'HaltonRegionHealthDepartment',
    'RegionofWaterlooPublicHealth',
    'HamiltonPublicHealthServices',
    'NiagaraRegionPublicHealthDepartment',
    'BrantCountyHealthUnit',
    'Haldimand-NorfolkHealthUnit']
ce_regions = [
    'PeelPublicHealth',
    'YorkRegionPublicHealth',
    'TorontoPublicHealth',
    'SimcoeMuskokaDistrictHealthUnit',
    'DurhamRegionHealthDepartment',
    'HaliburtonKawarthaPineRidgeDistrictHealthUnit',
    'PeterboroughPublicHealth']
e_regions = [
    'RenfrewCountyandDistrictHealthUnit',
    'HastingsandPrinceEdwardCountiesHealthUnit',
    'KingstonFrontenacandLennoxandAddingtonHealthUnit',
    'LeedsGrenvilleandLanarkDistrictHealthUnit',
    'OttawaPublicHealth',
    'EasternOntarioHealthUnit']
n_regions = [
    'NorthBayParrySoundDistrictHealthUnit',
    'TimiskamingHealthUnit',
    'SudburyandDistrictHealthUnit',
    'AlgomaPublicHealthUnit',
    'PorcupineHealthUnit',
    'ThunderBayDistrictHealthUnit',
    'NorthwesternHealthUnit']

#%%
# create output folder
Path('cases_plotted').mkdir(parents=True, exist_ok=True)

# set input folder
case_fpath = '../../case_data_parser/output/ontario_phu/'
    
# initialize plot settings
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
file_mappings = pd.read_csv('../../case_data_parser/output/ontario_phu/sim_file_mappings.csv')

data = {}
for row in file_mappings.iterrows():
    casefile = case_fpath + row[1]['casefile']
    cdf = pd.read_csv(casefile)
    region_abbr = row[1]['casefile'].rsplit('_')[0]
    data[region_abbr] = [region_abbr, cdf]

#%%

# extract beginning and end dates of the case reports to create the date range string
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
for key in data:
    # add all total actives under column of region_name
    region_name = data[key][0]
    region_df = data[key][1]
    phu_df[region_name] = region_df['TotalActive']



#%% - Define the indivudal plots to draw

fig, ax = plt.subplots(figsize=(15,6))
linewidth = 3
x = phu_df['IntegerDay']
font = matplotlib.font_manager.FontProperties()
font.set_size('small')

for phu_series in phu_df.iteritems():
    
    if(phu_series[0] == 'IntegerDay'):
        continue
    
    inList = True
    try: 
        i = sw_regions.index(phu_series[0])
        inList = True
    except ValueError: 
        inList = False
    
    if inList:
        ax.plot(x, phu_series[1], label=phu_series[0], linewidth=linewidth)
    else:
        inList = True
plt.legend(loc='upper left', prop=font)
plt.title('Active Cases for SouthWest PHU Regions ' + date_range)
plt.xlabel("Time (days)")
plt.ylabel('Number Active Infections')
plt.savefig("cases_plotted/southwest_phu_active_cases.png")
plt.close(fig)

fig, ax = plt.subplots(figsize=(15,6))

for phu_series in phu_df.iteritems():
    
    if(phu_series[0] == 'IntegerDay'):
        continue
    
    inList = True
    try: 
        i = cw_regions.index(phu_series[0])
        inList = True
    except ValueError: 
        inList = False
    
    if inList:
        ax.plot(x, phu_series[1], label=phu_series[0], linewidth=linewidth)
    else:
        inList = True
plt.legend(loc='upper left', prop=font)
plt.title('Active Cases for CentralWest PHU Regions ' + date_range)
plt.xlabel("Time (days)")
plt.ylabel('Number Active Infections')
plt.savefig("cases_plotted/centralwest_phu_active_cases.png")
plt.close(fig)

fig, ax = plt.subplots(figsize=(15,6))

for phu_series in phu_df.iteritems():
    
    if(phu_series[0] == 'IntegerDay'):
        continue
    
    inList = True
    try: 
        i = ce_regions.index(phu_series[0])
        inList = True
    except ValueError: 
        inList = False
    
    if inList:
        ax.plot(x, phu_series[1], label=phu_series[0], linewidth=linewidth)
    else:
        inList = True
plt.legend(loc='upper left', prop=font)
plt.title('Active Cases for CentralEast + Toronto PHU Regions ' + date_range)
plt.xlabel("Time (days)")
plt.ylabel('Number Active Infections')
plt.savefig("cases_plotted/centraleast_toronto_phu_active_cases.png")
plt.close(fig)

fig, ax = plt.subplots(figsize=(15,6))

for phu_series in phu_df.iteritems():
    
    if(phu_series[0] == 'IntegerDay'):
        continue
    
    inList = True
    try: 
        i = e_regions.index(phu_series[0])
        inList = True
    except ValueError: 
        inList = False
    
    if inList:
        ax.plot(x, phu_series[1], label=phu_series[0], linewidth=linewidth)
    else:
        inList = True
plt.legend(loc='upper left', prop=font)
plt.title('Active Cases for East PHU Regions ' + date_range)
plt.xlabel("Time (days)")
plt.ylabel('Number Active Infections')
plt.savefig("cases_plotted/east_phu_active_cases.png")
plt.close(fig)
        
fig, ax = plt.subplots(figsize=(15,6))

for phu_series in phu_df.iteritems():
    
    if(phu_series[0] == 'IntegerDay'):
        continue
    
    inList = True
    try: 
        i = n_regions.index(phu_series[0])
        inList = True
    except ValueError: 
        inList = False
    
    if inList:
        ax.plot(x, phu_series[1], label=phu_series[0], linewidth=linewidth)
    else:
        inList = True
plt.legend(loc='upper left', prop=font)
plt.title('Active Cases for North PHU Regions ' + date_range)
plt.xlabel("Time (days)")
plt.ylabel('Number Active Infections')
plt.savefig("cases_plotted/north_phu_active_cases.png")
plt.close(fig)
