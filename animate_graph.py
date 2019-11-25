
# coding: utf-8

# In[98]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import ImageMagickFileWriter
from IPython.display import Image, display
#get_ipython().magic('matplotlib notebook')
animation.convert_path: 'magick.exe'


# In[128]:

#file_x = input("Enter file name for x-axis: ")
#file_y = input("Enter file name for y-axis: ")


# In[129]:

# In[130]:

#df_y


# In[131]:

def preprocess_df(df, value_name):
    """ remove missing values and put years in one column
    
    Parameters
    ----------
    df: dataframe
        the data that needs to be preprocessed

    value_name: string
        the name of the column that will contain the year's data

    Return
    ------
    preprocessed dataframe
    """
    #print(df)
    years = [str(y) for y in range(1960, 2017)]
    
    # remove useless columns
    df.drop(['Indicator Name', 'Indicator Code'], axis=1, inplace=True)

    # remove countries with missing value
    #df.dropna(axis=0, inplace=True)
    #print(df.head())
    # melt the dataframe to have years in one columns
    df = pd.melt(df,
                     id_vars='Country Code',
                     value_vars=years,
                     var_name='Year',
                     value_name=value_name)
    #print(df.head())
    
    df.loc[df[value_name].isnull(), value_name] = df['Country Code'].map(df.groupby('Country Code')[value_name].mean())
    df = df.dropna(axis=0)
    return df
    #df=pd.DataFrame()



def animate_data(file_x,file_y):

	country = pd.read_csv('Backend/Datasets/Metadata_Country_API_IT.CEL.SETS.P2_DS2_en_csv_v2.csv')
	population = pd.read_csv('Backend/Datasets/country_population.csv')
	df_x = pd.read_csv('Backend/Datasets/'+file_x,skiprows=3)
	df_y = pd.read_csv('Backend/Datasets/'+file_y,skiprows=3)



	country = country[['Country Code', 'Region']]
	population = preprocess_df(population, 'Population')
	df_x = preprocess_df(df_x, file_x)
	#print(df.head())
	df_y = preprocess_df(df_y, file_y)


	# In[ ]:




	# In[132]:

	# Merge the data into one dataframe
	df = pd.merge(country, population, how='left', on='Country Code')
	df = pd.merge(df, df_y, how='left', on=['Country Code', 'Year'])
	df = pd.merge(df, df_x, how='left', on=['Country Code', 'Year'])

	# Remove remaining lines with missing values
	# They will appear if a country is in one dataset but not in another one
	df.dropna(axis=0, inplace=True)


	# In[133]:

	#df.head()
	return df,file_x,file_y


	# In[ ]:




	# In[134]:

	# get a list of the years. I will create one frame per year.
	

# In[ ]:
def generate_animation(file1, file2):
    df,file_x,file_y=animate_data(file1,file2)

    years = df['Year'].unique().tolist()

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(df[file_x].min() - .3,
                df[file_x].max() + .3)
    ax.set_ylim(df[file_y].min() - 2,
                df[file_y].max() + 2)

    # set the regions' colors
    colors = {
        'Latin America & Caribbean': '#2CA02C',
        'South Asia': '#8C564B',
        'Sub-Saharan Africa': '#E377C2',
        'Europe & Central Asia': '#FF7F0E',
        'Middle East & North Africa': '#D62728',
        'East Asia & Pacific': '#1F77B4',
        'North America': '#9467BD'
    }

    # create one scatterplot per region
    # I need to do like this to have all the regions 
    # showing up in the legend
    scats = []
    groups = df.groupby('Region')
    for name, grp in groups:
        scat = ax.scatter([], [],
                        marker='o',
                        color=colors[name],
                        label=name,
                        edgecolor='silver',
                        alpha=.6)
        scats.append(scat)

    # add the year in the middle of the scatter plot
    # for now, the text is empty (''). Il will be filled 
    # in each frame
    year_label = ax.text(4.5, 50, '', va='baseline', ha='right', alpha=.3,
                        size=12, fontdict={'weight': 'bold'})

    # decorate the visualization
    ax.spines['bottom'].set_color('silver')
    ax.spines['top'].set_color('silver')
    ax.spines['right'].set_color('silver')
    ax.spines['left'].set_color('silver')
    ax.tick_params(
        labelcolor='silver',
        color='silver'
    )
    ax.set_xlabel(file_x, color='silver')
    ax.set_ylabel(file_y, color='silver')
    ax.legend(loc=1, fontsize=7)

    # set the initial state
    def init():
        for scat in scats:
            scat.set_offsets([])
        return scats,

    # function that will update the figure with new data
    def update(year):
        # I need to update all scatterplots one by one
        # and return a list of updated plots
        for scat, (name, data) in zip(scats, groups):
            # get the data for the current year
            sample = data[data['Year'] == year]
            # set the x and y values 
            scat.set_offsets(sample[[file_x, file_y]])
            # update the size of the markers with the population
            # of the current year
            scat.set_sizes(np.sqrt(sample['Population'] / 10000) * 5)
            year_label.set_text(year)
        return scats,

    # generate the animation
    ani = animation.FuncAnimation(fig, update, init_func=init,
                                frames=years,
                                interval=50,
                                repeat=False)

    writer = ImageMagickFileWriter()
    ani.save('predicted_images/analysis.gif', writer=writer)
    #animate_data('CO2.csv','gdp.csv')
    plt.show()
