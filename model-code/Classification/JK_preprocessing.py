# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 18:01:12 2023

@author: rokka
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import pickle

# %% Import sklearn libraries
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


# %% train-test df function
def train_test_dataframes(df,features,targets,split_type='random',test_size=0.2,random_state=123,scale=True):
    
    #Creating X and y df from Time History data th_df (if applicable)-----------------------------------------------
    
    X = df[features].astype('float32')
    y = df[targets]
    
    # Training-Test Split=====================================================
    #(Random) Train-Test Split-----------------------------------------------
    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size= test_size,random_state=random_state)
    split = 'Random split'
    
    # (Sequential) Train-Test Split------------------------------------------
    if split_type == 'sequential':
    
        train_size = 1-test_size
        
        X_train = X[:int(train_size*len(X))]   #values up to % indicated by train_size
        X_test = X[int(train_size*len(X)):]    #remaining sequential values from X
        y_train = y[:int(train_size*len(y))]
        y_test = y[int(train_size*len(y)):]
        
        split = 'Sequential split'
    # Print split type--------------------------------------------------------
    print('Train-Test split was:', split)
    
    #Scaling==================================================================
    if scale==True:
        scaler=StandardScaler()
        X_train = pd.DataFrame(scaler.fit_transform(X_train),index=X_train.index, columns=X_train.columns)
        X_test = pd.DataFrame(scaler.transform(X_test),index=X_test.index,columns=X_test.columns)
        print('X_train & X_test have been scaled')
    else:
        print('X_train & X_test are not scaled')
        
    print('Dataframes are complete')  
    
    return X_train,X_test,y_train,y_test