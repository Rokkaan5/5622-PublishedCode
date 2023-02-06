# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 17:39:36 2023

@author: rokka
"""
# %% Import Libraries
import requests
import pandas as pd

# %% NOAA API
url = 'https://www.ncei.noaa.gov/cdo-web/api/v2/data'

header = {'Token':'Insert YOUR API Key here'}

URLPost = {'datasetid':'GSOY',
           # 'stationid':'GHCND:US1NCBC0005',
            # 'datatypeid':'TMAX&TMIN',
           'startdate':'2010-01-01',
           'enddate':'2015-12-31'
                    }

response=requests.get(url,headers=header, params=URLPost)
print(response)

print(response.json())

# %% Convert JSON response text to pandas df
noaa_df = pd.json_normalize(response.json()['results'])

