#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
23/08/2021

@author: glenn
"""
#%% - import libraries

import pandas
import datetime
import pickle
from pathlib import Path
from copy import deepcopy
import numpy as np
from local_module.fcts import cases2csv as cases2csv
from local_module.regions import phu_codes

#%% - input / output
DEBUG = True
OUTPUT_DIR = 'output'
TIMESERIES_DIR = 'output/timeseries'
DEBUG_DIR1 = 'output/debug/stage1/'
DEBUG_DIR2 = 'output/debug/stage2/'
DEBUG_DIR3 = 'output/debug/stage3/'
DEBUG_DIR4 = 'output/debug/stage4/'

Path(TIMESERIES_DIR).mkdir(parents=True, exist_ok=True)
Path(DEBUG_DIR1).mkdir(parents=True, exist_ok=True)
Path(DEBUG_DIR2).mkdir(parents=True, exist_ok=True)
Path(DEBUG_DIR3).mkdir(parents=True, exist_ok=True)
Path(DEBUG_DIR4).mkdir(parents=True, exist_ok=True)

#%% - load the sorted case data from pickled file, load region labels, set num regions

# set data
with open('pickled_cases/sorted_data_per_region.obj', 'rb') as f:
    data = pickle.load(f)

# set region labels
with open('pickled_cases/region_labels.obj', 'rb') as f:
    region_labels = pickle.load(f)

# set num_regions
num_regions = len(region_labels)

#%% - find earliest case date and latest case date amoung all regions

# initialize start day and end day to an arbitrary date
s = data[list(data.keys())[0]]

startday = s[0]['Date']
endday = s[0]['Date']
for region in data:
    
    case_series = data[region]
    
    # extract start and end dates of the case series
    d1=case_series[0]['Date']
    d2=case_series[-1]['Date']
    
    # save the earliest start day and lastest end day if a greater span is found
    if(d1 < startday):
        startday = d1
    if(d2 > endday):
        endday = d2

time_delta = endday - startday
sim_len = time_delta.days + 1
#%%
if DEBUG:
    cases2csv(data, DEBUG_DIR1, 'sorted_cases')

#%% - create a list of all days in the simulation
sim_date = list()
for i in range(sim_len):
    sim_date.append(startday + datetime.timedelta(days=i))
last_date = sim_date[-1]
   
#%% - for each region create a new list of series, items of which are date, num cases, num fatal cases
reduced_data = dict()
for region in region_labels:
    reduced_data[region] = list()

#%% - Sum all case reports occuring on the same day, place in 'reduced_data'
for region in reduced_data:
    
    # take the case series of the next region and set the date cursor to be one day before the first date in the list
    case_series = data[region]
    date_cursor = case_series[0]['Date']
    date_cursor -= datetime.timedelta(days=1)
    
    # find the next unique day, scan forward and grab all entries of the same date, accumulate them
    for case_report in case_series:
        
        # the date of the next case report concides with the date of a case report already entered in 'reduced_data'
        if(case_report['Date'] == date_cursor):
            # increment the case count of the last entry in reduced data
            r = reduced_data[region]
            # add 1 to the infection count of the day at the end of the list
            r[-1]['NewInfected'] += 1
            if (case_report['Outcome1'] == 'Fatal'):
                r[-1]['Fatal'] += 1
        # create a new day to enter cases under and insert the first case report    
        else:
            s = pandas.Series(object())
            s['Reporting_PHU_ID'] = case_report['Reporting_PHU_ID']
            s['Date'] = case_report['Date']
            s['NewInfected'] = 1
    
            if (case_report['Outcome1'] == 'Fatal'):
                s['Fatal'] = 1
            else:
                s['Fatal'] = 0
                
            date_cursor = s['Date']    
            reduced_data[region].append(s)
#%%
if DEBUG:
    cases2csv(reduced_data, DEBUG_DIR2, 'reduced_cases')

#%%
x1 = data[list(data.keys())[0]]
x2 = reduced_data[list(reduced_data.keys())[0]]

#%% - Insert zero infection/fatality case days into data inbetween days with cases   
for region in reduced_data:
    
    case_series = reduced_data[region]
    first_step = case_series[0]
    last_date_in_series = case_series[-1]['Date']
    next_date = first_step['Date']
    index = 0
    
    for date in sim_date:
        
        # if the simdate does exist in the reduced case data, then leave reduced data as is
        if(date == next_date):
            #print('Date: ', str(date), 'Next Date: ', print(str(next_date)))
            if(date != last_date_in_series): 
                next_date = case_series[index+1]['Date']
        # otherwise insert no cases under the sim_date
        else:
            #print('Inserting at: ', str(date))
            s = pandas.Series(object())
            s['Reporting_PHU_ID'] = region
            s['Date'] = date
            s['NewInfected'] = 0
            s['Fatal'] = 0
            s['IntegerDay'] = deepcopy(index)
            case_series.insert(index, s)
        
        case_series[index]['IntegerDay'] = deepcopy(index) 
        index += 1   
    
#%% - Add an Active Infected Column inferring the active cases from new infections
#   - mean infection length of 10 is used
for region in reduced_data:
    case_series = reduced_data[region]
    infected_series = np.zeros(sim_len,dtype=int)
    
    for i in range(len(case_series)):
        day = case_series[i]
        # add the number of new infected to the next 10 days
        if(day['NewInfected'] > 0):
            num_new_infected = day['NewInfected']
            max_index = min((i+10), sim_len - 1)
            num_additions = max_index - i
            
            for j in range(num_additions):
                infected_series[i+j] += num_new_infected
                
    # Copy the infected_series to reduced_data['ActiveInfected']
    for i in range(len(case_series)):
        case_series[i]['ActiveInfected'] = infected_series[i]

#%% - Shift all deaths by 10 days so that deaths occur at the end of mean
#   - infection length and not on the day of new infection
for region in reduced_data:
    case_series = reduced_data[region]
    deaths_series = np.zeros(sim_len,dtype=int)
    for i in range(len(case_series)):
        deaths_series[i] = case_series[i]['Fatal']
    deaths_series = np.roll(deaths_series, 10)
    deaths_series[0:10] = 0
    for i in range(len(case_series)):
        case_series[i]['Fatal'] = deaths_series[i]
#%%
if DEBUG:
    cases2csv(reduced_data, DEBUG_DIR3, 'blank_days_inserted') 
#%% - Make fatalities a cumulative sum over all days

for region in reduced_data:
    
    case_series = reduced_data[region]
    cumulative_deaths = 0
    for day in case_series:
        cumulative_deaths += day['Fatal']
        day['TotalDeaths'] = deepcopy(cumulative_deaths)

#%%
if DEBUG:
    cases2csv(reduced_data, DEBUG_DIR4, 'cumulative_deaths')  
        
#%% - output case data and mapping to simulation log files

with open(OUTPUT_DIR +'/sim_file_mappings.csv', "w") as mapfile:
    
    mapfile.write('casefile,simfile\n')
    for region in reduced_data:
        
        # remove spaces and commas from region name (csv file)
        region_name = phu_codes[region].replace(' ', '').replace(',', '')
        
        # write the name of the case data time series file, and the expected logs simulation timeseries file
        mapfile.write(region_name + '_timeseries.csv,' + 'region_'+ str(region) + '_totals_timeseries.csv\n')
        str_beginning = TIMESERIES_DIR + '/'
        fname = str_beginning + region_name + '_timeseries.csv'
        
        with open(fname, "w") as outfile:
            case_series = reduced_data[region]
            outfile.write('IntegerDay,NewInfected,ActiveInfected,TotalDeaths,Date\n')
            for day in case_series:
                outfile.write(str(day['IntegerDay']) + ',' +
                              str(day['NewInfected']) + ',' +
                              str(day['ActiveInfected']) + ',' +
                              str(day['TotalDeaths']) + ',' +
                              str(day['Date']) + "\n")
        
        mapfile.write(region_name + '_timeseries.csv,' + 'region_'+ str(region) + '_totals_timeseries.csv' + '\n')