# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 20:36:33 2023

@author: rokka
"""

# %% Libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import pickle

# %% Import sklearn libraries
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error as mse
from sklearn.metrics import r2_score

# %%
import ML_model as mlm 

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
features = ['co2','co2_per_capita','co2_growth_abs','coal_co2','coal_co2_per_capita']
targets = ['TAVG','TMAX','TMIN']

X_train,X_test,y_train,y_test = mlm.train_test_dataframes(final_df, features, targets,scale=False)

# %% LinearRegression Model
LR_pred,LR_model = mlm.vpt_ml_model(X_train, y_train, X_test, y_test,ml_model_type=LinearRegression())

# for t in targets:
#     mlm.ml_model_performance(target=y_test, prediction = LR_pred, target_name = t, 
#                              ml_model_name='LinearRegression model 1: {}'.format(t))

mlm.collective_performance_analysis(target=y_test, prediction=LR_pred, ml_model_name="Multi-Linear Regression")

# %% RandomForest Regression Model
RF_pred,RF_model = mlm.vpt_ml_model(X_train, y_train, X_test, y_test)

# for t in targets:
#     mlm.ml_model_performance(target=y_test, prediction = RF_pred, target_name = t, ml_model_name='RF model 1: {}'.format(t))
mlm.collective_performance_analysis(target=y_test, prediction=RF_pred, ml_model_name='RandomForest Regression Model')