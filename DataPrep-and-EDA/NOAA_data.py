# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 17:39:36 2023
@author: rokka
"""
# %% Import Libraries
import requests
import pandas as pd
from datetime import datetime, timedelta
import os,sys

# %% code to import my own python files outside cwd
path = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
sys.path.append(path)

# the following is a specific python file I made to access my api keys and 
# tokens while still hiding them from the publicly available code) 
# this is a file is only on my local system
from JKeys import my_key
# %% Build data
def noaa_req(startdate,enddate,dsid='GSOY'):
    url = 'https://www.ncei.noaa.gov/cdo-web/api/v2/data'
    
    header = {'Token': my_key('NOAA')}                      # replace with your own api key here
    
    URLPost = {'datasetid':dsid,
               # 'stationid':'GHCND:US1NCBC0005',
                # 'datatypeid':'TMAX&TMIN',
               'startdate':startdate,
               'enddate':enddate
                    }
    response=requests.get(url,headers=header, params=URLPost)
    return pd.json_normalize(response.json()['results'])

def build_noaa_df(startdate,enddate,dsid='GSOY'):
    '''
    function to concat individual NOAA data request dfs to build a full df of NOAA API data 
    (especially since requests are limited to one year range (or 10 year range for annual and monthly data))
    '''
    form = '%Y-%m-%d'                                 # string format for time
    dfs = []
    start = datetime.strptime(startdate,form)         # initial (and iterative) start date
    final_end = datetime.strptime(enddate,form)       # specified end date
    
    end = start+pd.DateOffset(years=1)                      # iterative end date
    
    while end <= final_end:                                 # NOAA API request has specific 
        df = noaa_req(start.strftime(form),end.strftime(form),dsid=dsid)
        dfs.append(df)
    
        start = end
        end += pd.DateOffset(years=1)
    
    return pd.concat(dfs).reset_index(drop=True)



# %%
def type_df_dict(noaa_df):
    dfs = {i:noaa_df[noaa_df['datatype']==i] for i in noaa_df['datatype'].unique()}
    return dfs


# %% test functions
sample_df = build_noaa_df('1990-01-01','2018-01-01')
sample_dict = type_df_dict(sample_df)