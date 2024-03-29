#!/usr/bin/env python
# coding: utf-8

# In[102]:

# Original author: Kevin
# (Slightly) modified by: Binyamin
# modified further by: Glenn - Feb 18 2021

#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import geopandas as gpd
from collections import defaultdict, OrderedDict
from copy import deepcopy
import json

def shared_boundaries(gdf, id1, id2):
    g1 = gdf[gdf["PHU_ID"] == str(id1)].geometry.iloc[0]
    g2 = gdf[gdf["PHU_ID"] == str(id2)].geometry.iloc[0]
    return g1.length, g2.length, g1.boundary.intersection(g2.boundary).length

def get_boundary_length(gdf, id1):
    g1 = gdf[gdf["PHU_ID"] == str(id1)].geometry.iloc[0]
    return g1.boundary.length


# In[103]:


df = pd.read_csv("../../cadmium_gis/Ontario_PHUs/ontario_phu_clean.csv")  # General information (id, population, area...)
df_adj = pd.read_csv("../../cadmium_gis/Ontario_PHUs/ontario_phu_adjacency.csv")  # Pair of adjacent territories
gdf_ontario = gpd.read_file("../../cadmium_gis/Ontario_PHUs/ontario_phu.gpkg")  # GeoDataFrame with the territories poligons


# In[104]:


df.head()


# In[105]:


df_adj.head()


# In[106]:


gdf_ontario.head()


# In[107]:

# read default state from input json
default_cell = json.loads(open("input_ontario_phu/default.json", "r").read())
fields = json.loads(open("input_ontario_phu/fields.json", "r").read())
infectedCells = json.loads(open("input_ontario_phu/infectedCells.json", "r").read())


# In[108]:

default_state = default_cell["default"]["state"]
default_vicinity = default_cell["default"]["neighborhood"]["default_cell_id"]
default_correction_factors = default_vicinity["infection_correction_factors"]
default_correlation = default_vicinity["correlation"]
df_adj.head()


# In[109]:


nan_rows = df[df['population'].isnull()]
zero_pop_rows = df[df["population"] == 0]
invalid_region_ids = list(pd.concat([nan_rows, zero_pop_rows])["phu_id"])
len(invalid_region_ids), len(df)


# In[110]:


adj_full = OrderedDict()  # Dictionary with the structure of the json output format

for ind, row in df_adj.iterrows():  # Iterate the different pair of adjacent territories
    if row["region_id"] in invalid_region_ids:
        print("Invalid region_id found: ", row["region_id"])
        continue
    elif row["neighbor_id"] in invalid_region_ids:
        print("Invalid region_id found: ", row["neighbor_id"])
        continue
    elif str(row["region_id"]) not in adj_full:
        temp_cldf = df["phu_id"]
        temp_adjdf = row["region_id"]
        c = df["phu_id"] == row["region_id"]
        rel_row = df[df["phu_id"] == row["region_id"]].iloc[0, :]
        pop = int(rel_row["population"])
        area = rel_row["area_epsg4326"]

        boundary_len = get_boundary_length(gdf_ontario, row["region_id"])
        
        state = deepcopy(default_state)
        state["population"] = pop
        expr = dict()
        expr[str(row["region_id"])] = {"state": state, "neighborhood": {}}
        adj_full[str(row["region_id"])] = expr

    l1, l2, shared = shared_boundaries(gdf_ontario, row["region_id"], row["neighbor_id"])
    correlation = ((shared/l1 + shared/l2) / 2)  # equation extracted from zhong paper (boundaries only, we don't have roads info for now)
    # correlation = math.e ** (-1/correlation)
    if correlation == 0:
        continue
    
    expr = {"correlation": correlation,"infection_correction_factors": default_correction_factors}
    adj_full[str(row["region_id"])][str(row["region_id"])]["neighborhood"][str(row["neighbor_id"])]=expr
    
    if ind % 10 == 0:
        print(ind, "%.2f%%" % (100*ind/len(df_adj)))

for key, value in adj_full.items():
    # insert every cell into its own neighborhood, a cell is -> cell = adj_full[key][key]
    adj_full[key][key]["neighborhood"][key] = {"correlation": default_correlation, "infection_correction_factors": default_correction_factors}


# In[111]:

# insert cells from ordered dictionary into index "cells" of a new OrderedDict
template = OrderedDict()
template["cells"] = {}
template["cells"]["default"] = default_cell["default"]

# make a list of infected cell ids
infected_index = list()
for key in infectedCells:
    infected_index.append(key)

#%%

for key, value in adj_full.items():

    # write cells in cadmium master format 
    template["cells"][key] = value[key]

    # check if the key is in the list of infected cell keys
    # is key in the list infected_index
    
    if(key in infected_index):
        # overwrite the state variables of the infected cell
        template["cells"][key]["state"]["susceptible"] = infectedCells[key]["state"]["susceptible"]
        template["cells"][key]["state"]["exposed"] = infectedCells[key]["state"]["exposed"]
        template["cells"][key]["state"]["infected"] = infectedCells[key]["state"]["infected"]
        template["cells"][key]["state"]["recovered"] = infectedCells[key]["state"]["recovered"]
        template["cells"][key]["state"]["fatalities"] = infectedCells[key]["state"]["fatalities"]

# insert fields object at the end of the json for use with the GIS Webviewer V2
template["fields"] = fields["fields"]
adj_full_json = json.dumps(template, indent=4, sort_keys=False)  # Dictionary to string (with indentation=4 for better formatting)


# In[112]:

with open("output/scenario_ontario_phu.json", "w") as f:
    f.write(adj_full_json)
