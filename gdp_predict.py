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

if __name__ == "__main__":
    print("--------------- GDP-------------")
    df_gdp = pd.read_csv("../Datasets/gdp.csv",skiprows=3)
    df_gdp.head()

    df_gdp = df_gdp.drop("Unnamed: 64",axis=1)
    df_gdp = df_gdp.drop("2019",axis=1)

    df_gdp.describe(include='all')

    df_gdp = df_gdp.drop(["Indicator Name","Indicator Code"],axis=1)

    GDP_Stacked_df = pd.melt(df_gdp,id_vars=['Country Name','Country Code'])

    #print(GDP_Stacked_df.head())

    GDP_Stacked_df.loc[GDP_Stacked_df['value'].isnull(), 'value'] = GDP_Stacked_df['Country Name'].map(GDP_Stacked_df.groupby('Country Name')['value'].mean())

    GDP_Stacked_df = GDP_Stacked_df.dropna(axis=0)
    #print(GDP_Stacked_df.head())
    GDP_Stacked_df=GDP_Stacked_df.set_index("Country Name")

    GDP_Stacked_df['variable'] = GDP_Stacked_df['variable'].astype(float)

    #sns.regplot(x="variable", y="value", data=GDP_Stacked_df);
    #plt.show()

    le = preprocessing.LabelEncoder()

    GDP_Stacked_df= GDP_Stacked_df.reset_index()
    GDP_Stacked_df.head()

    GDP_Stacked_df['encoded'] = le.fit_transform(GDP_Stacked_df["Country Name"].values)

    X = GDP_Stacked_df[['encoded','variable']]
    X = np.array(X)

    y = GDP_Stacked_df['value']
    y = np.array(y)
    print(GDP_Stacked_df[GDP_Stacked_df["encoded"]==11])
    #X_train, X_val, Y_train, Y_val = train_test_split(X_train_val, Y_train_val, test_size=0.15/0.85, random_state=0)

    model = LinearRegression()
    model.fit(X , y)

    cont = input("Enter Country Name :")
    year = int(input("Enter year :"))
    enc = GDP_Stacked_df.encoded[GDP_Stacked_df["Country Name"]==cont].unique()[0]



    predicted = model.predict([[enc, year]]).astype(float)
    print("Predicted GDP: ",predicted[0],"US$")


    new_df=GDP_Stacked_df[GDP_Stacked_df["Country Name"]==cont]
    sns.lineplot(x="variable" , y="value",data=new_df)
    plt.show()
