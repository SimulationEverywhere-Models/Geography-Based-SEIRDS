#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  1 20:16:11 2021

@author: glenn
"""

def pd_series_date(s):
    return s['Date']

# writes a dictionary of list of pandas Series objects to file
def cases2csv(data_dict, folder_name, series_name):
    
    for key in data_dict:
        series = data_dict[key]
        filename = str(key) + '_' + series_name + '.csv'
        filepath = folder_name + filename
        examplePandasSeries = series[0]
        seriesKeys = examplePandasSeries.keys()
        
        with open(filepath, 'w') as f:
    
            for column in seriesKeys:
                f.write(str(column) + ',')
            f.write('\n')
            
            for step in series:
                for item in step:
                    f.write(str(item) + ',')
                f.write('\n')
            f.write('\n')
    
    
    """
    with open('filex.csv', 'w') as f:
        
        firstkey = list(data_dict.keys())[0]
        examplePandasSeries = data_dict[firstkey][0]
        pandasSeriesKeys = examplePandasSeries.keys()
        
        for key in pandasSeriesKeys:
            f.write(str(key) + ',')
        f.write('\n')
        
        for key in data_dict:
            series = data_dict[key]
            
            f.write('Region: ' + str(key) + ',\n')
            for step in series:
                for item in step:
                    f.write(str(item) + ',')
                f.write('\n')
            f.write('\n')
    """
    