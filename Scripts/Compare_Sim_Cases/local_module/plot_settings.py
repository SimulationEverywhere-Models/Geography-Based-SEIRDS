#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 14:57:04 2021

@author: eldrazi
"""

import matplotlib
    
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


