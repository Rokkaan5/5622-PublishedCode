# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 17:24:39 2023

@author: rokka
"""

# %% Import Libraries
import pandas as pd
import requests  


# %% Endpoint URL
End = 'https://www.airnowapi.org/aq/forecast/zipCode/'


# %% Parameters
URLPost = {'API_KEY':'Insert YOUR API Key here',
           'format': 'application/json', 
           'zipCode': '80303',
           'date' : '2019-02-03',
           'distance': '25'
            }

# %% request response code
response1=requests.get(End, URLPost)
print(response1)

# %% Read the JSON text
jsontxt = response1.json()
print(jsontxt)

# %% Convert JSON text to Pandas DF
airnow_df = pd.json_normalize(jsontxt)


