import pandas as pd
import numpy as np
from sklearn.preprocessing import Imputer
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

df = pd.read_csv('rawData/Literacy_rate, adult_total(%_of people_ages_15_and_above).csv',skiprows=3)

df3 = df.iloc[:,4:]
# display(df3.shape)
yempty = df3.iloc[4:5,].to_numpy()
df3.dropna(axis=0, how='all', thresh=5, inplace=True)
# display(df3)
# display(df3.shape)

# from sklearn.preprocessing import Imputer
# from sklearn.linear_model import LinearRegression

def predictValueImputed(rowNo):
    startRow = rowNo
    endRow = rowNo + 1
    x1 = np.arange(1972, 2018 + 2)
    X = x1[:-1]
    X = X.reshape(-1,1)
    # display(X)
    # display(X.shape)
    y1 = df3.iloc[startRow:endRow,12:-2].to_numpy()
    y = y1.reshape(-1,1)
    # display(y.shape)

    imputer = Imputer()
    y_imputed = imputer.fit_transform(y)

    reg = LinearRegression().fit(X, y_imputed)
    # display(rowNo)
    # display(df.iloc[startRow:endRow,0])
    # display(reg.predict([[2019]])[0][0])
    # display(reg.predict([[2020]])[0][0])
    # display(reg.predict([[2021]])[0][0])
    # display(reg.predict([[2022]])[0][0])
    # display(reg.predict([[2023]])[0][0])
    # display(reg.predict([[2024]])[0][0])
    # display(reg.predict([[2025]])[0][0])
    # predictions = []
    predictions2019 = (reg.predict([[2019]])[0][0])
    predictions2020 =  (reg.predict([[2020]])[0][0])
    predictions2021 =  (reg.predict([[2021]])[0][0])
    predictions2022 =  (reg.predict([[2022]])[0][0])
    predictions2023 =  (reg.predict([[2023]])[0][0])
    predictions2024 =  (reg.predict([[2024]])[0][0])
    predictions2025 =  (reg.predict([[2025]])[0][0])

    return predictions2019,predictions2020,predictions2021,predictions2022,predictions2023,predictions2024,predictions2025

p2019 = []
p2020 = []
p2021 = []
p2022 = []
p2023 = []
p2024 = []
p2025 = []
# display(df3.shape[0])
for y in range(df3.shape[0]):
    # display(y)
    predictions2019,predictions2020,predictions2021,predictions2022,predictions2023,predictions2024,predictions2025 = predictValueImputed(y)
    p2019.append(predictions2019)
    p2020.append(predictions2020)
    p2021.append(predictions2021)
    p2022.append(predictions2022)
    p2023.append(predictions2023)
    p2024.append(predictions2024)
    p2025.append(predictions2025)


# display(df3.columns)
# display(len(p2019))
df3['2019'] = p2019
df3['2020'] = p2020
df3['2021'] = p2021
df3['2022'] = p2022
df3['2023'] = p2023
df3['2024'] = p2024
df3['2025'] = p2025
# display(df3.columns)

df3 = df3.drop(columns=['Unnamed: 64'])
# display(df3)

# Save To CSV
df3.to_csv('literacyPredicted.csv')

# import matplotlib.pyplot as plt

def plotRatePerCountryImputed(row):
    x = np.arange(1960, 2026)
    y = df3.iloc[row].to_numpy()
    y1 = y.reshape(-1,1)
    imputer = Imputer()
    y_imputed = imputer.fit_transform(y1)
    # display(x.shape)
    # display(y_imputed.shape)
    plt.plot(x,y_imputed)
    plt.title("Literacy Rate Over years")
    plt.xlabel("Years")
    plt.ylabel("Literacy Rate")
    plt.legend()
    #plt.savefig('RatePerCountry.png', dpi=fig.dpi, bbox_inches='tight', pad_inches=0.5)
    return x, y_imputed;
    

def plotRatePerCountryEmpty(row):
    x = np.arange(1960, 2026)
    y = df3.iloc[row].to_numpy()
    y1 = y.reshape(-1,1)
    # display(x.shape)
    # display(y1.shape)
    plt.plot(x,y1)
    plt.title("Literacy Rate Over years")
    plt.xlabel("Years")
    plt.ylabel("Literacy Rate")
    plt.legend()
    #plt.savefig('RatePerCountry.png', dpi=fig.dpi, bbox_inches='tight', pad_inches=0.5)
    plt.show()
    


# plotRatePerCountryEmpty(117)
# plotRatePerCountryImputed(117)

# plotRatePerCountryEmpty(17)
# plotRatePerCountryImputed(17)

df4 = df
# display(df4.shape)
df4.dropna(axis=0, how='all', thresh=9, inplace=True)
# display(df4)
# display(df4.shape)
# year = '2019'
fig_size = plt.rcParams["figure.figsize"]
fig_size[0] = 18
fig_size[1] = 13
plt.rcParams["figure.figsize"] = fig_size

def plotYearBar(year):
    x = df4['Country Name']
    # display(x)
    y = df3[str(year)]
    # display(y)
    plt.bar(x,y)
    plt.title("Literacy Rate for year" + str(year))
    plt.xlabel("Literacy Rate Per Country")
    plt.ylabel("Literacy Rate")
    plt.legend()
    plt.xticks(rotation=90)
    #plt.savefig('RatePerYear.png', dpi=fig.dpi, bbox_inches='tight', pad_inches=0.5)
    return x, y;

# plotYearBar(2019)

# plotYearBar(2020)

# plotYearBar(2000)

# plotYearBar(1996)
