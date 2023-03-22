# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 20:18:26 2023

@author: rokka
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import os,sys

# %% code to import my own python files outside cwd------------------------------------------------------------------------------
path = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
sys.path.append(path)
from NOAA_data import build_noaa_df
# %% The final time-range of data I want=========================================================================================
noaa_df = build_noaa_df('1763-01-01','2022-01-01')

# %%
noaa_dt = pd.to_datetime(noaa_df['date'])
noaa_df['year'] = noaa_dt.dt.year

single_data = noaa_df[['year','datatype']]

# %%
single_data.to_csv('single_data.csv',index=False)