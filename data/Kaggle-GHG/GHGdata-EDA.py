# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 17:21:03 2023

@author: rokka
"""

# %% import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# %%
ghg_df = pd.read_csv('climate_change.csv')

# %% EDA Datatype and Statistics================================================================================================
ghg_df.info()

df_descr = ghg_df[ghg_df.columns[2:]].describe()

# %% EDA visualizations=========================================================================================================
# Distribution plots -----------------------------------------------------------------------------------------------------------
for data_col in ghg_df.columns[2:]:
    plt.figure()
    sns.displot(data=ghg_df, x = data_col,kind='kde')
    plt.title('{} Value Distribution plot'.format(data_col))

# %% GHG correlation with temperature-------------------------------------------------------------------------------------------
from scipy.stats import pearsonr
for col in ghg_df.columns[2:-1]:
    t = 'Temp'
    plt.figure()
    plt.scatter(x=ghg_df[t],y=ghg_df[col])
    plt.xlabel(t)
    plt.ylabel(col)
    plt.title('{} correlation w/ temp (R = {})'.format(col,pearsonr(ghg_df[t],ghg_df[col])[0]))