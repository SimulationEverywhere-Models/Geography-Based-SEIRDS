#!/usr/bin/env python
# coding: utf-8

# In[5]:


# Original author: Kevin
# (Slightly) modified by: Binyamin
# modified further by: Glenn

#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import geopandas as gpd
from collections import defaultdict, OrderedDict
from copy import deepcopy
import json

def shared_boundaries(gdf, id1, id2):
    g1 = gdf[gdf["dauid"] == str(id1)].geometry.iloc[0]
    g2 = gdf[gdf["dauid"] == str(id2)].geometry.iloc[0]
    return g1.length, g2.length, g1.boundary.intersection(g2.boundary).length

def get_boundary_length(gdf, id1):
    g1 = gdf[gdf["dauid"] == str(id1)].geometry.iloc[0]
    return g1.boundary.length


# In[6]:


df = pd.read_csv("../../../cadmium_gis/data/DA Ottawa Clean.csv")  # General information (id, population, area...)
df_adj = pd.read_csv("../../../cadmium_gis/data/DA Ottawa Adjacency.csv")  # Pair of adjacent territories
gdf_ontario = gpd.read_file("../../../cadmium_gis/data/DA Ottawa.gpkg")  # GeoDataFrame with the territories poligons


# In[7]:


df.head()


# In[8]:


df_adj.head()


# In[9]:


gdf_ontario.head()


# In[10]:


# read default state from input json
template = json.loads(open("default.json", "r").read())
default_state = template["default"]["state"]


# In[11]:


default_vicinity = template["default"]["neighborhood"]["vicinity"]
default_correction_factors = default_vicinity["infection_correction_factors"]
df_adj.head()


# In[12]:


nan_rows = df[df['DApop_2016'].isnull()]
zero_pop_rows = df[df["DApop_2016"] == 0]
invalid_dauids = list(pd.concat([nan_rows, zero_pop_rows])["DAuid"])
len(invalid_dauids), len(df)


# In[13]:


adj_full = OrderedDict()  # Dictionary with the structure of the json output format

for ind, row in df_adj.iterrows():  # Iterate the different pair of adjacent territories
    if row["dauid"] in invalid_dauids:
        print("Invalid dauid found: ", row["dauid"])
        continue
    elif row["Neighbor_dauid"] in invalid_dauids:
        print("Invalid dauid found: ", row["Neighbor_dauid"])
        continue
    elif str(row["dauid"]) not in adj_full:
        rel_row = df[df["DAuid"] == row["dauid"]].iloc[0, :]
        pop = rel_row["DApop_2016"]
        area = rel_row["DAarea"]

        boundary_len = get_boundary_length(gdf_ontario, row["dauid"])
        
        state = deepcopy(default_state)
        state["population"] = pop

        # added write of pop entry to demonstrate that the value does indicate a changing population value per cell
        adj_full[str(row["dauid"])] = {"cell_id": str(row["dauid"]), "state": state, "neighborhood": []}

    l1, l2, shared = shared_boundaries(gdf_ontario, row["dauid"], row["Neighbor_dauid"])
    correlation = (shared/l1 + shared/l2) / 2  # equation extracted from zhong paper (boundaries only, we don't have roads info for now)
    # correlation = math.e ** (-1/correlation)
    if correlation == 0:
        continue
    adj_full[str(row["dauid"])]["neighborhood"].append({"cell_id": str(row["Neighbor_dauid"]), "vicinity": {"correlation": correlation,
                                                                                                            "infection_correction_factors": default_correction_factors}})
    if ind % 1000 == 0:
        print(ind, "%.2f%%" % (100*ind/len(df_adj)))

for key, value in adj_full.items():
    adj_full[key]["neighborhood"].append({"cell_id": key, "vicinity": default_vicinity})


# In[14]:


adj_full


# In[15]:


template["cells"] = list(adj_full.values())


# In[16]:


adj_full_json = json.dumps(template, indent=4, sort_keys=False)  # Dictionary to string (with indentation=4 for better formatting)


# In[17]:


with open("../input/pre_processing.json", "w") as f:
    f.write(adj_full_json)

