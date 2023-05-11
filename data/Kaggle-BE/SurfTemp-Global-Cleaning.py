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
global_df = pd.read_csv('GlobalTemperatures.csv')

# %% Data Cleaning EDA========================================================================================================

global_df.info()

g_desc = global_df.describe()

# %% Change 'dt' column to datetime datatype
global_df['dt'] = pd.to_datetime(global_df['dt'])

# %%
global_df[global_df['LandMaxTemperature'].isna()].info()

global_df[global_df['LandAverageTemperature'].isna()].info()  

# %%
sns.pairplot(data=global_df)

# %% Missing parameter correlation with available parameters (LandAverageTemp)
temp = ['LandMaxTemperature','LandMinTemperature','LandAndOceanAverageTemperature']

for t in temp:
    proxy = 'LandAverageTemperature'
    plt.figure()
    plt.scatter(x=global_df[proxy],y=global_df[t])
    plt.xlabel(proxy)
    plt.ylabel(t)
    plt.title('{} (R = {})'.format(t,pearsonr(global_df[t].dropna(),global_df[proxy][global_df[t].notnull()])[0]))
    
# %% Deal with Missing - 1: Drop all missing==================================================================================
clean_global1 = global_df.dropna()

clean_global1.to_csv('global_droppedNA.csv')

# %% Deal with Missing - 2: Impute with Linear Regression=====================================================================
from sklearn.linear_model import LinearRegression

lrm = LinearRegression()
X = ['LandAverageTemperature']
y = temp
train = global_df['LandMaxTemperature'].notnull()
train_X = global_df[X][train]
train_y = global_df[y][train]
pred_X = global_df[X][global_df['LandMaxTemperature'].isna()].dropna()

lrm.fit(train_X,train_y)

pred = lrm.predict(pred_X)

pred_df = pd.DataFrame(pred,columns=y,index=pred_X.index)

# %% Rebuild the final clean imputed df---------------------------------------------------------------------------------------
top_half = pd.concat([pred_X,pred_df],axis=1)

bottom_half = pd.concat([train_X,train_y],axis=1)

data_whole = pd.concat([top_half,bottom_half])

final_clean = pd.concat([global_df['dt'],data_whole],axis=1)

final_clean.info()

# %% Final 2nd clean df-------------------------------------------------------------------------------------------------------
final_clean[final_clean['LandAverageTemperature'].isna()].index == global_df[global_df['LandAverageTemperature'].isna()].index

final_clean.dropna(inplace=True)

clean_global2 = final_clean.copy()

clean_global2.to_csv('global_ImputedMissing.csv')
