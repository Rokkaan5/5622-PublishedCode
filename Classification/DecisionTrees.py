# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 15:49:54 2023

@author: rokka
"""
# %%
import numpy as np
from sklearn import preprocessing
import pandas as pd
import graphviz 
import string
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, plot_tree,export_graphviz
from sklearn.svm import LinearSVC
from sklearn.decomposition import PCA
from sklearn.tree import export_graphviz

from IPython.display import Image  

import pydotplus
# %%
df = pd.read_csv('temp-classification-test2.csv')

# suggested label columns (regression)
#label_cols = ['TAVG','TMAX','TMIN']    #not included in currently read-in data, but interesting to try eventually
# classification label
class_label_col = ['TAVG_label','TMAX_label','TMIN_label']
# data columns
data_cols = ['co2','co2_per_capita','co2_growth_abs','coal_co2','coal_co2_per_capita']


# %%
def train_test_dataframes(df,features,targets,split_type='random',test_size=0.2):
    
    X_col = features
    y_col = targets
    #--------------------------------------------------------------------------------------------------------------- 
    
    X = df[X_col]
    y = df[y_col]
    
    # Training-Test Split=====================================================
    #(Random) Train-Test Split-----------------------------------------------
    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size= test_size,random_state=123)
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
    
    return X_train,X_test,y_train,y_test

# %% Classification training and testing set=====================================================================================
X_train,X_test,y_train,y_test = train_test_dataframes(df,data_cols,class_label_col[0],test_size=0.3)

# %%
classDT = DecisionTreeClassifier(splitter='best')  # default is 'best', (only way I know to change is using 'random')

classDT.fit(X_train,y_train)

plot_tree(classDT)
print(X_train.columns)

# run in console to get copy a higher resolution version
graphviz.Source(export_graphviz(classDT,feature_names=X_train.columns))
# %% Features and feature importances
dict(zip(X_train.columns,classDT.feature_importances_))

# %%
DT_pred = classDT.predict(X_test)

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

cm = confusion_matrix(y_test, DT_pred, labels=classDT.classes_)
disp = ConfusionMatrixDisplay(confusion_matrix=cm,display_labels=classDT.classes_)                         
disp.plot()
plt.show()

# %% Regressions training and testing set========================================================================================
# X_train,X_test,y_train,y_test = train_test_dataframes(df,data_cols,label_cols,test_size=0.5)

# # %%
# regDT = DecisionTreeRegressor()

# regDT.fit(X_train,y_train)

# plot_tree(regDT)
# print(X_train.columns)

# # run in console to get copy a higher resolution version
# graphviz.Source(export_graphviz(regDT,feature_names=X_train.columns))
# # %% Features and feature importances
# dict(zip(X_train.columns,regDT.feature_importances_))

# # %%
# DT_pred = regDT.predict(X_test)
# DT_pred = pd.DataFrame(DT_pred,columns = y_test.columns)
# from sklearn.metrics import r2_score
# from sklearn.metrics import mean_squared_error as mse
# for i in y_test.columns:
#     print('MSE:{}'.format(mse(DT_pred[i],y_test[i])))
#     print('R2-score:{}'.format(r2_score(DT_pred[i],y_test[i])))