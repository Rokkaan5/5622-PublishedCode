# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 10:19:15 2023

@author: rokka
"""

# %% Libraries
import numpy as np
import pandas as pd

# %%
data = pd.read_csv('owid_JK_all_selected_ghg_data.csv')
temp = pd.read_csv('NOAA-temp-classification-label.csv')

# %%

df = pd.merge(data,temp[['year','TAVG_label','TMAX_label','TMIN_label']],on='year')

# %% potentially useful (categorized) columns of ghg data
# main ghg types of interest (and per capita info)
ghg_cols = ['co2','methane','nitrous_oxide']
ghg_percap = [i+'_per_capita' for i in ghg_cols]

# total ghg info
ghg2 = ['total_ghg','ghg_per_capita']

# other interesting information
other = ['co2_growth_abs','consumption_co2','consumption_co2_per_capita','energy_per_capita','primary_energy_consumption']

# different sources of production-based co2 emissions
co2_types = ['cement','coal','flaring','gas','oil','land_use_change']  # these are not valid column names

co2_type_cols = [i+'_co2' for i in co2_types]                      # use this for total data
co2_types_cols_percap = [i+'_per_capita' for i in co2_type_cols]   # use this to include per-capita data


# %%

# different sources of production-based co2 emissions (except flaring)
co2_types = ['cement','coal','gas','oil','land_use_change']  # these are not valid column names

co2_type_cols = [i+'_co2' for i in co2_types]                      # use this for total data
co2_types_cols_percap = [i+'_per_capita' for i in co2_type_cols]   # use this to include per-capita data

classification_test1 = df[['year','co2','co2_per_capita','co2_growth_abs']+['TAVG_label','TMAX_label','TMIN_label']]
class_test1 = classification_test1.dropna()


classification_test2 = df[['year','co2','co2_per_capita','co2_growth_abs','coal_co2','coal_co2_per_capita','TAVG_label','TMAX_label','TMIN_label']]
class_test2 = classification_test2.dropna()

# %%
class_test1.to_csv('temp-classification-test1.csv',index=False)
class_test2.to_csv('temp-classification-test2.csv',index=False)
