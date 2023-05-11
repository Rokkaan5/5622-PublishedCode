# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 02:54:57 2023

@author: rokka
"""
# %% libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score

# %% data
clust_df = pd.read_csv('../data/API-NOAA/1990-2018_df.csv')


# %% different k values
ks = [10,15,20,24,27]
predictions = []
sil_scores = []

for k in ks:
    clust = KMeans(n_clusters=k)
    clust.fit(clust_df)
    pred = clust.predict(clust_df)
    predictions.append(pred)
    sil_scores.append(silhouette_score(clust_df, pred))

# preview some results
for i in range(len(ks)):
    print('k = {} silhouette score: {}'.format(ks[i],sil_scores[i]))
    
for i in range(len(ks)):
    print("cluster result preview for k = {}: {}".format(ks[i],predictions[i]))