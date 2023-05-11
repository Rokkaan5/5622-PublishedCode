# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 14:58:18 2023

@author: rokka
"""

# %%
import pandas as pd
import numpy as np
import pickle
import datetime

# %%
noaa_df = pickle.load(open('API-NOAA/noaa_1990-2018.pkl','rb'))

def type_df_dict(noaa_df):
    dfs = {i:noaa_df[['date','value']][noaa_df['datatype']==i] for i in noaa_df['datatype'].unique()}
    return dfs


# noaa_df['station'].value_counts()
type_dict = type_df_dict(noaa_df[noaa_df['station']=='GHCND:AG000060390'])

for i in type_dict:
    type_dict[i].rename(columns={'value':i},inplace=True)
    
dfs = [i.set_index('date') for i in type_dict.values()]
df = dfs[0].join(dfs[1:],how='outer')
final_noaa = df.fillna(0)
final_noaa = final_noaa.reset_index()

# %%
owid_df = pd.read_csv('ourworldindata/1990-2018_ghg_data.csv')  # I must've manually selected the data and created a csv

# %%
noaa_dt = pd.to_datetime(final_noaa['date'])
final_noaa['year'] = noaa_dt.dt.year

# %%
combined_df = pd.merge(final_noaa,owid_df,on='year')
# %%
final_combined_df = combined_df.drop(columns = ['date'])
label_col = final_noaa.columns[1:-1].tolist()
data_col = owid_df.columns[1:].tolist()
final_combined_df = final_combined_df[['year']+data_col+label_col]
final_combined_df = final_combined_df.drop(columns =['DT00','DX32'])

# %%
conditions = [
    (final_combined_df['EMXP'] > 60), 
    (final_combined_df['EMXP'] >= 40) & (final_combined_df['EMXP'] <= 60),
    (final_combined_df['EMXP'] < 40),
    ]

values = ['Above', 'Within', 'Below']

final_combined_df['EMXP_class'] = np.select(conditions, values)

# %%
final_combined_df.to_csv('final_combined_df.csv',index=False)