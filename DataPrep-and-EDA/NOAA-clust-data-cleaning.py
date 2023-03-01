# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 17:39:36 2023
@author: rokka
"""
# %% Import Libraries
import requests
import pandas as pd
from datetime import datetime, timedelta
from NOAA_data import build_noaa_df, type_df_dict


# %%
noaa_df = build_noaa_df('1990-01-01','2018-01-01')

df_dict = type_df_dict(noaa_df)

# rename 'value' column in each df as attribute name
for i in df_dict:
    df_dict[i].rename(columns={'value':i},inplace=True)

print(df_dict)

# %%
dfs = [i.set_index('date') for i in df_dict.values()]
single_df = dfs[0].join(dfs[1:],how='outer')

single_df = single_df.fillna(0)
single_df = single_df.reset_index()

clust_df = single_df.drop('date',axis=1)

clust_df.head()

# %% save df for clustering to csv
clust_df.to_csv('1990-2018_df.csv',index=False)
