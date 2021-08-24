#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  1 20:16:11 2021

@author: glenn
"""

def pd_series_date(s):
    return s['Date']

# writes a dictionary of lists of pandas Series objects to file
def dict_of_list_tocsv(d, fname):
    with open(fname, 'w') as f:
        
        firstkey = list(d.keys())[0]
        examplePandasSeries = d[firstkey][0]
        pandasSeriesKeys = examplePandasSeries.keys()
        
        for key in pandasSeriesKeys:
            f.write(str(key) + ',')
        f.write('\n')
        
        for key in d:
            series = d[key]
            
            f.write('Region: ' + str(key) + ',\n')
            for step in series:
                for item in step:
                    f.write(str(item) + ',')
                f.write('\n')
            f.write('\n')
    