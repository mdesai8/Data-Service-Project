#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 21:26:36 2019

@author: bhumikasinghal
"""

import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from sklearn import preprocessing
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
np.set_printoptions(suppress=True)
pd.set_option('display.float_format', lambda x: '%.3f' % x)
from sklearn.linear_model import LinearRegression


def predictCO2(country, year):
    df_fr = pd.read_csv('Backend/Datasets/CO2.csv', error_bad_lines=False, skiprows=4)
    df_fr = df_fr.drop(['Country Code','Indicator Name','Indicator Code','Unnamed: 64'], axis=1)
    df_fr = df_fr.set_index('Country Name')
    df_fr = df_fr.dropna(how = 'all', axis=0)
    df_fr = df_fr.dropna(how = 'all', axis=1)
    df_fr = df_fr[df_fr.isnull().sum(axis=1) <= 20]
    df_fr = df_fr.ffill(axis=1)
    df_fr = df_fr.bfill(axis=1)
    #print(df_fr.shape)
    df_fr = df_fr.reset_index()
    FR_Stacked_df = pd.melt(df_fr,id_vars=['Country Name'])
    FR_Stacked_df = FR_Stacked_df.set_index("Country Name")
    FR_Stacked_df['variable'] = FR_Stacked_df['variable'].astype(float)
    #sns.regplot(x="variable", y="value", data=FR_Stacked_df);
    #plt.show()

    le = preprocessing.LabelEncoder()
    FR_Stacked_df = FR_Stacked_df.reset_index()
    FR_Stacked_df['encoded'] = le.fit_transform(FR_Stacked_df["Country Name"].values)
    X = FR_Stacked_df[['encoded','variable']]
    X = np.array(X)
    y = FR_Stacked_df['value']
    y = np.array(y)

    model = KNeighborsRegressor(n_neighbors=3)
    model.fit(X , y)

    if (len(FR_Stacked_df.encoded[FR_Stacked_df["Country Name"]==country].unique()) == 0):
        return False

    enc = FR_Stacked_df.encoded[FR_Stacked_df["Country Name"]==country].unique()[0]
    predicted = model.predict([[enc, year]]).astype(float)
    new_df=FR_Stacked_df[FR_Stacked_df["Country Name"]==country]
    sns.lineplot(x="variable" , y="value",data=new_df)
    plt.xlabel("Years")
    plt.ylabel("COS Emission")
    plt.title("COS Emissions for " + country)
    plt.savefig("predicted_images/CO2Emission.png")
    plt.close()

    return predicted[0]
