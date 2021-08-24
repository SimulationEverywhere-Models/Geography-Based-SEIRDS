sort_and_pickle_cases.py
---
Reads and sorts raw case data from:
https://data.ontario.ca/en/dataset/confirmed-positive-cases-of-covid-19-in-ontario
 and saves the sorted data as pickled objects in the pickled_cases folder. This is a computationally expensive script, so the results of this process are not included in the repo with the raw case data. The case data can be downloaded from the link mentioned, and this script can be used to generate the pickled case objects. The pickled case data is included in the repo instead.

transform_case_data.py
---
Reads the pickled case data and generates the case time series per region, including the columns IntegerDay, NewInfected, ActiveInfected, TotalDeaths, Date.

plot_all_phu_infected.py
---
Plots all case data new infections, grouping the 33 PHUs into 5 graphs

plot_all_phu_individually.py
---
Plots all case data new infections, generating a graph for each PHU individually