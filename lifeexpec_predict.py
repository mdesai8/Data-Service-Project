#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 20:44:22 2019

@author: bhumikasinghal
"""

import matplotlib
matplotlib.use('Agg') # Need to add this otherwise server closes unexpectedly
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
from sklearn.linear_model import LogisticRegression

def predicted_life_expec(cont, year):
    # print("--------------- Life Expectancy -------------")      
    df_le = pd.read_csv('Backend/Datasets/life_expectancy.csv', error_bad_lines=False, skiprows=4)
    df_le = df_le.drop(['Country Code','Indicator Name','Indicator Code','2018','2019','Unnamed: 64'], axis=1)
    df_le = df_le.set_index('Country Name')
    df_le = df_le.dropna(how = 'all', axis=0)
    df_le = df_le[df_le.isnull().sum(axis=1) <= 20]
    df_le = df_le.ffill(axis=1)
    df_le = df_le.bfill(axis=1)
    #print(df_fr.shape)
    df_le = df_le.reset_index()
    LE_Stacked_df = pd.melt(df_le,id_vars=['Country Name'])
    LE_Stacked_df = LE_Stacked_df.set_index("Country Name")
    LE_Stacked_df['variable'] = LE_Stacked_df['variable'].astype(float)
    #sns.regplot(x="variable", y="value", data=LE_Stacked_df);
    #plt.show()
    
    le = preprocessing.LabelEncoder()
    LE_Stacked_df = LE_Stacked_df.reset_index()
    LE_Stacked_df['encoded'] = le.fit_transform(LE_Stacked_df["Country Name"].values)
    X = LE_Stacked_df[['encoded','variable']]
    X = np.array(X)
    y = LE_Stacked_df['value']
    y = np.array(y)
    
    model = LinearRegression()
    model.fit(X , y)

    # cont = input("Enter Country Name :")
    # year = int(input("Enter year :"))
    if (len(LE_Stacked_df.encoded[LE_Stacked_df["Country Name"]==cont].unique()) == 0):
        return False

    enc = LE_Stacked_df.encoded[LE_Stacked_df["Country Name"]==cont].unique()[0]
    predicted = model.predict([[enc, year]]).astype(float)
    # print("Predicted Life Expectancy: ",predicted[0])


    year = int(year)

    new_df=LE_Stacked_df[LE_Stacked_df["Country Name"]==cont]

    predicted_df = pd.DataFrame({"Country Name": [cont],
                                 "variable": [year],
                                 "value": [predicted[0]],
                                 "encoded": 9})
    new_df = new_df.append(predicted_df, ignore_index=True)

    # print(new_df.to_string())
    sns.lineplot(x="variable" , y="value",data=new_df)
    plt.xlabel("Years")
    plt.ylabel("Life Expectancy")
    plt.title("Life Expectancy for " + cont)
    plt.savefig("predicted_images/life_expec.png")
    plt.close()
    return predicted[0]
    