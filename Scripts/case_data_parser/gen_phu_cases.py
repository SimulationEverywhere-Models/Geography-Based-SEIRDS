#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 00:52:59 2021

@author: glenn
"""
#%% - import libraries

import pandas
import numpy as np
import datetime
from pathlib import Path

def pd_series_date(s):
    return s['Date']

#%% - import ontario phu case data

Path('output/ontario_phu').mkdir(parents=True, exist_ok=True)

phuDailys = pandas.read_csv("data/PHU/PHU_Cases_Positives.csv")
phuDailys['Date'] = pandas.to_datetime(phuDailys['Accurate_Episode_Date']).dt.date
phu_df = phuDailys[['Reporting_PHU_ID', 'Outcome1', 'Date']]

#%% - count the number of unique regions before parsing the data, then create a dict to hold the data of each region
#   for each phu, create a dictionary element under its PHU_ID key to hold a list that will be the case data
#   this cell will take a few minutes to run

region_labels = list(set(phu_df['Reporting_PHU_ID']))
num_regions = len(region_labels)

data = dict()
for region in region_labels:
    data[region] = list()

for region in region_labels:
    for row in phu_df.iterrows():
            if(row[1]['Reporting_PHU_ID']==region):
                data[region].append(row[1])
                       
#%% - sort all cases by date

for region in data:
    dataset = data[region]
    
    # dataset is a list of pandas series objects that need to be sorted by date
    dataset.sort(key=pd_series_date)
    
#%% - find earliest case date and latest case date amoung all regions
# set an arbirary start and end date to begin the process, then iterate through
# the dataset to find the earliest case report and latest case report
s = data[2253]
startday = s[0]['Date']
endday = s[0]['Date']
for region in data:
    dataset = data[region]
    d1=dataset[0]['Date']
    d2=dataset[len(dataset)-1]['Date']
    
    if(d1 < startday):
        startday = d1
    if(d2 > endday):
        endday = d2

time_delta = endday - startday
sim_len = time_delta.days + 1

#%% - create a list of all days in the simulation
sim_date = list()
for i in range(sim_len):
    sim_date.append(startday + datetime.timedelta(days=i))
   
#%% - for each region create a new list of series, items of which are date, num cases, num fatal cases
reduced_data = dict()
for region in region_labels:
    reduced_data[region] = list()

last_date = startday - datetime.timedelta(days=-1)
for region in reduced_data:
    dataset = data[region]
    
    # find the next unique day, scan forward and grab all entries of the same date, accumulate them
    for entry in dataset:
        
        # if the entry index isn't zero, then check if there are other entries under that date
        if not(len(reduced_data[region]) == 0):
            
            # if the date is the same as the date at the end of the list then add it under that entry
            if(entry['Date'] == last_date):
                # increment the case count of the last entry in reduced data
                r = reduced_data[region]
                r[-1]['Infected'] += 1
                if (entry['Outcome1'] == 'Fatal'):
                    r[-1]['Fatal'] += 1
                
            else:
                s = pandas.Series(object())
                s['Date'] = entry['Date']
                s['Infected'] = 1
        
                if (entry['Outcome1'] == 'Fatal'):
                    s['Fatal'] = 1
                else:
                    s['Fatal'] = 0
                    
                last_date = s['Date']    
                reduced_data[region].append(s)
        else:
            # append the first entry to reduced_data[region]
            s = pandas.Series(object())
            s['Date'] = entry['Date']
            s['Infected'] = 1
        
            if (entry['Outcome1'] == 'Fatal'):
                s['Fatal'] = 1
            else:
                s['Fatal'] = 0
                    
            last_date = s['Date']    
            reduced_data[region].append(s)
      
#%% - now for each region create a data structure that holds the positive cases and fatalities per simulation day
#     the resulting data is equivalent to the reporting of new infected and new fatal per day
case_dailys = dict()
for region in region_labels:
    case_dailys[region] = list()
    
for region in case_dailys:
    dataset = reduced_data[region]
    
    r = dataset[0]
    next_date = r['Date']
    ri_max = len(dataset)
    ri = 0
    
    for date in sim_date:
        
        # if the simdate does exist in the reduced case data, then insert the reduced data entry for sim day
        if(next_date == date):
            case_dailys[region].append(dataset[ri])
            ri += 1
            if(ri < ri_max):
                r = dataset[ri]
                next_date = r['Date']
        # otherwise insert no cases under the sim_date
        else:
            s = pandas.Series(object())
            s['Date'] = date
            s['Infected'] = 0
            s['Fatal'] = 0
            case_dailys[region].append(s) 
       
#%% - extend new cases to active cases with mean infection length = 10 days
#   - the output will be IntegerDay, TotalActive, TotalDeaths, Date
active_cases = dict()
for region in region_labels:
    active_cases[region] = list()
    
for region in active_cases:
    dataset = case_dailys[region]
    # define a 2d array 2xsim_len - column 1 is TotalActive, column 2 is TotalDeaths
    
    c = np.zeros((2,sim_len),dtype=int)
    for i in range(len(dataset)):
        daily_report = dataset[i]
        
        # add the number of new infected to the next 10 days
        if(daily_report['Infected'] > 0):
            
            ni = daily_report['Infected']
            max_index = min((i+10), sim_len - 1)
            num_additions = max_index - i
            
            for j in range(num_additions):
                c[0,i+j] += ni
                
        # add the new fatal the the cumulative fatal count
        if (i>0): 
            c[1,i] = c[1,i-1] + daily_report['Fatal']
        elif (i==0):
            c[1,i] = daily_report['Fatal']
            
    active_cases[region].append(c)
            
#%% - make the final output series with columns IntegerDay, TotalActive, TotalDeaths, Date

output_series = dict()
for region in region_labels:
    output_series[region] = list()
    
for region in active_cases:
    r = active_cases[region]
    dataset = r[0]
    
    for i in range(dataset.shape[1]):
        s = pandas.Series(object())
        s['IntegerDay'] = i
        s['TotalActive'] = dataset[0,i]
        s['TotalDeaths'] = dataset[1,i]
        s['Date'] = sim_date[i]
        output_series[region].append(s) 
        
#%%

phu_codes = {2226 : 'Algoma Public Health Unit',
             2227 : 'Brant County Health Unit' ,
             2240 : 'Chatham-Kent Health Unit',
             2230 : 'Durham Region Health Department',
             2258 : 'Eastern Ontario Health Unit',
             2233 : 'Grey Bruce Health Unit',
             2234 : 'Haldimand-Norfolk Health Unit',
             2235 : 'Haliburton, Kawartha, Pine Ridge District Health Unit',
             2236 : 'Halton Region Health Department',
             2237 : 'Hamilton Public Health Services',
             2238 : 'Hastings and Prince Edward Counties Health Unit',
             5183 : 'Huron Perth Health Unit',
             2241 : 'Kingston, Frontenac and Lennox and Addington Health Unit',
             2242 : 'Lambton Public Health',
             2243 : 'Leeds, Grenville and Lanark District Health Unit',
             2244 : 'Middlesex-London Health Unit', 
             2246 : 'Niagara Region Public Health Department', 
             2247 : 'North Bay Parry Sound District Health Unit',
             2249 : 'Northwestern Health Unit',
             2251 : 'Ottawa Public Health',
             2253 : 'Peel Public Health',
             2255 : 'Peterborough Public Health',
             2256 : 'Porcupine Health Unit',
             2265 : 'Region of Waterloo, Public Health',
             2257 : 'Renfrew County and District Health Unit',
             2260 : 'Simcoe Muskoka District Health Unit',
             4913 : 'Southwestern Public Health',
             2261 : 'Sudbury and District Health Unit', 
             2262 : 'Thunder Bay District Health Unit', 
             2263 : 'Timiskaming Health Unit', 
             3895 : 'Toronto Public Health',
             2266 : 'Wellington-Dufferin-Guelph Health Unit',
             2268 : 'Windsor-Essex County Health Unit', 
             2270 : 'York Region Public Health'
             }

with open('output/ontario_phu/sim_file_mappings.csv', "w") as mapfile:
    
    mapfile.write('casefile,simfile\n')
    for region in output_series:
        
        s = phu_codes[region].replace(' ', '')
        region_name = s.replace(',', '')
        str_beginning = "output/ontario_phu/"
        f = str_beginning + region_name + '_timeseries.csv'
        
        with open(f, "w") as outfile:
            d = output_series[region]
            outfile.write('IntegerDay,TotalActive,TotalDeaths,Date' + '\n')
            for day in d:
                outfile.write(str(day['IntegerDay']) + "," +
                              str(day['TotalActive']) + "," +
                              str(day['TotalDeaths']) + "," +
                              str(day['Date']) + "\n")
        
        mapfile.write(region_name + '_timeseries.csv,' + 'region_'+ str(region) + '_totals_timeseries.csv' + '\n')
