# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 17:39:36 2023
@author: rokka
"""
# %% Import Libraries------------------------------------------------------------------------------------------------------------
import requests
import pandas as pd
from datetime import datetime, timedelta
import os,sys

# %% code to import my own python files outside cwd------------------------------------------------------------------------------
path = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
sys.path.append(path)

# the following is a specific python file I made to access my api keys and 
# tokens while still hiding them from the publicly available code) 
# this is a file is only on my local system
from JKeys import my_key
# %% Request data from API and create dataframe if possible======================================================================
def noaa_req(startdate,enddate,dsid='GSOY'):
    url = 'https://www.ncei.noaa.gov/cdo-web/api/v2/data'
    
    header = {'Token': my_key('NOAA')}   
    
    URLPost = {'datasetid':dsid,
               # 'stationid':'GHCND:US1NCBC0005',
                # 'datatypeid':'TMAX&TMIN',
               'startdate':startdate,
               'enddate':enddate
                    }
    response=requests.get(url,headers=header, params=URLPost)
    if response.status_code == 200:
        try:
            return pd.json_normalize(response.json()['results'])
        except:
            return pd.DataFrame()

# %% Build a dataframe for a range of dates using function above=================================================================
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



# %% Create a dictionary of dataframes by 'datatype'=============================================================================
def type_df_dict(noaa_df):
    dfs = {i:noaa_df[['date','value']][noaa_df['datatype']==i] for i in noaa_df['datatype'].unique()}
    return dfs

# %% create a "final" dataframe with all datatypes as columns and retain information like 'date' and 'station'===================
def type_by_station(noaa_df):
    
    # initialize empty list of station dataframes
    all_dfs = []
    
    # organize by station
    for j in noaa_df['station'].unique():
        station_df = noaa_df[noaa_df['station'] == j]
        
        # create a dictionary of dataframes by 'datatype'
        type_dict = type_df_dict(station_df)
        
        # for all dataframes in the dictionary rename the 'value' column as the 'datatype' label
        for i in type_dict:
            type_dict[i].rename(columns={'value':i},inplace=True)
        
        # set the date as the index to align date with proper information
        type_dfs = [i.set_index('date') for i in type_dict.values()]
        
        # join the dataframes in the dictionary to create a single dataframe 
        df = type_dfs[0].join(type_dfs[1:],how='outer')
        
        # add station column again, and fill with current station in loop
        df['station'] = j
        
        # reset index and append to list of station dataframes
        all_dfs.append(df.reset_index())
        
    # combine all dataframes made in for-loop above into a single dataframe
    final_df = pd.concat(all_dfs)
    final_df = final_df.reset_index(drop=True)
    
    return final_df


# %% test functions==============================================================================================================
# sample_df = build_noaa_df('1763-01-01','1990-01-01')
# sample_dict = type_df_dict(sample_df)

# %% The final time-range of data I want=========================================================================================
full_request_df = build_noaa_df('1763-01-01','2022-01-01')
final_df = type_by_station(full_request_df.drop_duplicates())

# %% (optional) move "station" column to be second column (after 'date')
df_col = final_df.pop('station')
final_df.insert(1,'station',df_col)

# %% (optional) change 'date' column to simply indicate year
noaa_dt = pd.to_datetime(final_df['date'])
final_df['date'] = noaa_dt.dt.year
final_df.rename(columns={'date':'year'},inplace=True)

# %% save final_df as csv
final_df.to_csv('NOAA-Final-DF.csv',index=False)
