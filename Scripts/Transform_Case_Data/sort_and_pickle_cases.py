#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 00:52:59 2021

@author: glenn
"""
#%% - import libraries

import pandas
import time
import pickle
from local_module import fcts

#%% input / output paths

RAW_CASE_DATA = 'raw_cases/conposcovidloc.csv'
SORTED_CASES = 'pickled_cases/sorted_data_per_region.obj'
REGION_LABELS = 'pickled_cases/region_labels.obj'

#%% - read the case data into pandas dataframe

phuDailys = pandas.read_csv(RAW_CASE_DATA)
phuDailys['Date'] = pandas.to_datetime(phuDailys['Accurate_Episode_Date']).dt.date
phu_df = phuDailys[['Reporting_PHU_ID', 'Outcome1', 'Date']]

#%% - find all distinct region labels

region_labels = list(set(phu_df['Reporting_PHU_ID']))
num_regions = len(region_labels)

#%% - insert case reports from raw case data into lists per region
#   - computationally expensive, this cell may take more than 10 minutes (1061 seconds)

t0 = time.perf_counter()
data = dict()
for region in region_labels:
    data[region] = list()

for region in region_labels:
    for row in phu_df.iterrows():
            if(row[1]['Reporting_PHU_ID']==region):
                data[region].append(row[1])
t1 = time.perf_counter()
print('cell took ', str(t1 - t0), ' seconds to complete') 
                 
#%% - sort all in the dict by case by date

for region in data:
    dataset = data[region]
    
    # dataset is a list of pandas series objects that need to be sorted by date
    dataset.sort(key=fcts.pd_series_date)
    
#%% - Save sorted data to pickled object

with open(SORTED_CASES, 'wb') as f:
    pickle.dump(data, f)

#%% - save region label to pickled object

with open(REGION_LABELS, 'wb') as f:
    pickle.dump(region_labels, f)
