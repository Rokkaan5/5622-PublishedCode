# -*- coding: utf-8 -*-
"""
Created on Tue May  2 10:36:25 2023

@author: rokka
"""

# %% Libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import pickle

# %%
noaa_df = pd.read_csv('NOAA-FINAL-DF.csv')
owid_df = pd.read_csv('owid_JK_all_selected_ghg_data.csv')

# %%
sort_df = noaa_df.sort_values(by='year')

# %%
temp_data = sort_df[['year','station','TAVG','TMAX','TMIN']]
temp_data.dropna(inplace=True)

# %%
df = pd.merge(owid_df,temp_data[['year','TAVG','TMAX','TMIN']],on='year')

# %%
final_df = df[['year','co2','co2_per_capita','co2_growth_abs','coal_co2','coal_co2_per_capita','TAVG','TMAX','TMIN']]
final_df.dropna(inplace=True)

# %%
final_df.to_csv('regression-temp-final-df.csv',index=False)