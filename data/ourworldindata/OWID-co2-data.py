# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 13:08:55 2023

@author: rokka
"""
# %%
import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import os,sys

# %%
df = pd.read_csv('owid-co2-data.csv')

# %%
world_df = df[df['country']=='World']
world_df.info()

# # %%
# world_df.drop(columns=['iso_code'],inplace = True)
# world_df.info()

# %%
with_methane_df = world_df[~world_df['methane'].isna()]
with_methane_df.info()

# # %%
# world_df = world_df[~world_df['CO2 concentrations'].isna()]
# world_df.info()

# # %%
# dropped_df = world_df.dropna()

# %% Selecting columns (categorized)
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
all_df = world_df[['year']+ghg_cols+ghg_percap+ghg2+other+co2_type_cols+co2_types_cols_percap]

# %%
all_df.to_csv('owid_JK_all_selected_ghg_data.csv',index=False)