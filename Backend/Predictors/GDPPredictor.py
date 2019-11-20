import pandas as pd
from sklearn import preprocessing
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression

np.set_printoptions(suppress=True)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

DATASET_FILEPATH = "../Datasets/gdp.csv"

class GDPPredictor(Object):

    def __init__(self):
        self._self._df_gdp = pd.read_csv(DATASET_FILEPATH, skiprows=3)
        self._self._df_gdp.head()

        self._self._df_gdp = self._df_gdp.drop("Unnamed: 64",axis=1)
        self._df_gdp = self._df_gdp.drop("2019",axis=1)

        self._df_gdp.describe(include='all')

        self._df_gdp = self._df_gdp.drop(["Indicator Name","Indicator Code"],axis=1)

        self._GDP_stacked_df = pd.melt(self._df_gdp,id_vars=['Country Name','Country Code'])


        self._GDP_stacked_df.loc[self._GDP_stacked_df['value'].isnull(), 'value'] = self._GDP_stacked_df['Country Name'].map(self._GDP_stacked_df.groupby('Country Name')['value'].mean())

        self._GDP_stacked_df = self._GDP_stacked_df.dropna(axis=0)
        self._GDP_stacked_df=self._GDP_stacked_df.set_index("Country Name")

        self._GDP_stacked_df['variable'] = self._GDP_stacked_df['variable'].astype(float)


        self._le = preprocessing.LabelEncoder()

        self._GDP_stacked_df= self._GDP_stacked_df.reset_index()
        self._GDP_stacked_df.head()

        self._GDP_stacked_df['encoded'] = self._le.fit_transform(self._GDP_stacked_df["Country Name"].values)

        X = self._GDP_stacked_df[['encoded','variable']]
        X = np.array(X)

        y = self._GDP_stacked_df['value']
        y = np.array(y)

        self._model = LinearRegression()
        self._model.fit(X , y)

    def pointPredictGDP(self, country, year):
        self._enc = GDP_Stacked_df.encoded[GDP_Stacked_df["Country Name"]==country].unique()[0]
        return self._model.predict([[self._enc, year]]).astype(float)
