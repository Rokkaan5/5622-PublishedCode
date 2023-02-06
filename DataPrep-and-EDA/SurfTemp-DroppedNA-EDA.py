# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 14:56:50 2023

@author: rokka
"""

# %% import libraries=========================================================================================================
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

# %% csv to df----------------------------------------------------------------------------------------------------------------
global_df = pd.read_csv('global_DroppedNA.csv')

# %% Data Cleaning EDA========================================================================================================

global_df.info()

g_desc = global_df.describe()

# %% Change 'dt' column to datetime datatype
global_df['dt'] = pd.to_datetime(global_df['dt'])


# EDA
# %% Distribution Plots
for col in global_df.columns[1:]:
    plt.figure()
    sns.displot(data = global_df,x = col, kind = 'kde')
    plt.title('{} (Celsius) Distribution Plot'.format(col))