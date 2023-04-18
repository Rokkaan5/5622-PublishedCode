# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 11:26:34 2023

@author: rokka
"""

# %% libraries
import numpy as np
from sklearn.preprocessing import StandardScaler
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.svm import SVC

# my own code
from JK_preprocessing import train_test_dataframes

# %%
df = pd.read_csv('temp-classification-test2.csv')

# suggested label columns (regression)
#label_cols = ['TAVG','TMAX','TMIN']    #not included in currently read-in data, but interesting to try eventually
# classification label (y; targets)
class_label_col = ['TAVG_label','TMAX_label','TMIN_label']
# data columns (X; features)
data_cols = ['co2','co2_per_capita','co2_growth_abs','coal_co2','coal_co2_per_capita']


# %% Preprocessing: train-test split & scaling
X_train,X_test,y_train,y_test = train_test_dataframes(df, features = data_cols, targets = ['TAVG_label'],scale=True)

# X_train
# X_test
# y_train
# y_test

# %% evaluate models via confusion matrices
def create_cm(model,actual,prediction,plot_title):
    cm = confusion_matrix(actual, prediction, labels=model.classes_)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm,display_labels=model.classes_)                         
    disp.plot()
    plt.xticks(rotation=45)
    plt.title(plot_title)
    plt.show()

# %% Kernel 1
lin_svc = SVC(C=1.0, kernel='linear') # C (regularization parameter) = 1.0 is the default
lin_svc.fit(X_train, y_train)
lin_svc_pred = lin_svc.predict(X_test)

create_cm(lin_svc,y_test,lin_svc_pred,'Linear Kernel SVM')


# %% Kernel 2 (with different degree values)
deg =[2,3,4,5,6,7,8,9,10]

for d in deg:
    poly_svc = SVC(C=1.0, kernel='poly', degree = d)  # degree (for kernel = 'poly') = 3 is the default
    poly_svc.fit(X_train,y_train)
    poly_svc_pred = poly_svc.predict(X_test)
    
    create_cm(poly_svc,y_test,poly_svc_pred,'Polynomial Kernel (degree = {}) SVM'.format(d))
# %% Kernel 3
rbf_svc = SVC(C=1.0, kernel='rbf')   # technically this would be (all) the default parameters for sklearn's SVC
rbf_svc.fit(X_train,y_train)
rbf_svc_pred = rbf_svc.predict(X_test)

create_cm(rbf_svc,y_test,rbf_svc_pred,'rbf Kernel SVM')
