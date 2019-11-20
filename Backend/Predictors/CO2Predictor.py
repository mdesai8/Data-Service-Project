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
from sklearn.linear_model import LinearRegression

np.set_printoptions(suppress=True)
pd.set_option('display.float_format', lambda x: '%.3f' % x)


class CO2Predictor(Object):

    CO2DATASET_FILEPATH = "../Datasets/C02.csv"

    def __init__(self):
        self._df_fr = pd.read_csv(self.CO2DATASET_FILEPATH, error_bad_lines=False, skiprows=4)
        self._self._df_fr = self._df_fr.drop(['Country Code','Indicator Name','Indicator Code','Unnamed: 64'], axis=1)
        self._df_fr = self._df_fr.set_index('Country Name')
        self._df_fr = self._df_fr.dropna(how = 'all', axis=0)
        self._df_fr = self._df_fr.dropna(how = 'all', axis=1)
        self._df_fr = self._df_fr[self._df_fr.isnull().sum(axis=1) <= 20]
        self._df_fr = self._df_fr.ffill(axis=1)
        self._df_fr = self._df_fr.bfill(axis=1)

        self._df_fr = self._df_fr.reset_index()
        self._FR_Stacked_df = pd.melt(self._df_fr,id_vars=['Country Name'])
        self._FR_Stacked_df = self._FR_Stacked_df.set_index("Country Name")
        self._FR_Stacked_df['variable'] = self._FR_Stacked_df['variable'].astype(float)

        self._le = preprocessing.LabelEncoder()
        self._FR_Stacked_df = self._FR_Stacked_df.reset_index()
        self._FR_Stacked_df['encoded'] = self._le.fit_transform(self._FR_Stacked_df["Country Name"].values)
        self._X = self._FR_Stacked_df[['encoded','variable']]
        self._X = np.array(X)
        self._y = self._FR_Stacked_df['value']
        self._y = np.array(y)

        self._model = KNeighborsRegressor(n_neighbors=3)
        self._model.fit(self._X , self._y)

    def pointPredictCO2(self, country, year):
        enc = FR_Stacked_df.encoded[FR_Stacked_df["Country Name"]==country].unique()[0]
        return model.predict([[enc, year]]).astype(float)
