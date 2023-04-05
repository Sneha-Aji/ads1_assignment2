# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


import os
files = ['Arable land (% of land area).csv',
         'Average precipitation in depth (mm per year).csv',
         'CO2 emissions from gaseous fuel consumption (kt) .csv',
         'CO2 intensity (kg per kg of oil equivalent energy use).csv',
         'Foreign direct investment, net inflows (% of GDP).csv',
         'Forest area (sq. km).csv',
         'Land area where elevation is below 5 meters (% of total land area).csv',
         'Urban land area where elevation is below 5 meters (sq. km).csv']



# A function to read in world bank regional data
def read_world_bank_region(f_name):
    df = pd.read_csv(f_name, index_col = 'date') # Read in the data, regions are columns
    regions = [
         'South Asia',
         'East Asia & Pacific',
         'Middle East & North Africa',
         'Sub-Saharan Africa',
         'North America',
         'Latin America & Caribbean',
         'Europe & Central Asia'
    ]
    df = df.loc[:,regions] # Subset for those regions
    
    if all(df.isnull().all()): # filter regions with no data
        return("Region has no data")
    
    rows_to_drop = [] # Clean rows whose observations are missing from the beginning till the end
    for row in df.index:
        if all(df.loc[row, :].isna()):
            rows_to_drop.append(row)
            
    df = df.drop(rows_to_drop) # Drop the rows with missing data        
    years = df.T # Transpose and set years to columns
    return years, df

# Check for files topics to keep
for f_name in files:
    if type(read_world_bank_region(f_name)) == tuple:
        pass
    else:
        files.remove(f_name)



# Remaining worthy files
files



def barplot(df, topic):
    '''
    a function to plot barplots from dataframe
    '''
    df.plot(kind = 'bar', figsize = (7,5))
    plt.xlabel('Country Name') # label x axis
    plt.title(f"{topic}")
    plt.legend(bbox_to_anchor = [1, 1])
    plt.show()



def lineplot(df, topic):
    '''
    A function to plot line plots from dataframe
    '''
    df.plot(kind ='line', linestyle = '--')
    plt.xlabel('Year')
    plt.title(f'{topic}')
    plt.legend(bbox_to_anchor = [1,0.8])
    plt.show()

def r_heatmap(dfr, cmap, region):
    '''
    A function to produce heatmap
    '''
    plt.figure(figsize = (8,8))
    plt.imshow(dfr, cmap = cmap)
    plt.colorbar() # Colorbar
    plt.title(region)
    plt.xticks(range(len(dfr)), dfr.columns, rotation = 90) # Set x ticks
    plt.yticks(range(len(dfr)), dfr.columns)
    for i in range(len(dfr)):
        for j in range(len(dfr)):
            plt.annotate(f"{dfr.iloc[i,j]:.2f}", (i, j)) # Annotation of the heatmap
    plt.show()
    
def stats_desc(df):
    '''
    a function to compute descriptive stats
    '''
    return df.describe()



# Descriptive Statistics
topic = 'CO2 emissions from gaseous fuel consumption (kt) .csv'
carbon_y, carbon_c = read_world_bank_region(topic)
stats_desc(carbon_c).T.rename_axis("Region", axis = 0)



# Plotting bar plots
# CO2
topic = 'CO2 emissions from gaseous fuel consumption (kt) .csv'
carbon_y, carbon_c = read_world_bank_region(topic)
barplot(carbon_y, topic[:-4])

# forest area
topic2 = 'Forest area (sq. km).csv'
forest_y, forest_c = read_world_bank_region(topic2)
barplot(forest_y, topic2[:-4])



# Correlations
# North America
check = 0
topics = []
for f_name in files:
    topic = f_name[:-4] # Subset topic name
    region = 'North America' # Set the region
    dfy, dfc = read_world_bank_region(f_name)
    
    if len(dfc) > 3: # Check if most data are present.
        region_data = dfc[region]
        topics.append(topic) # Save the topic name
        if check == 0:
            region_df = region_data
            check += 1
        else:
            region_df = pd.concat([region_df, region_data], axis = 1)
dfr = region_df.corr()
dfr.columns = topics
r_heatmap(dfr, cmap = 'cividis', region = region)

# Latin America & Caribbean
check = 0
topics = []
for f_name in files:
    topic = f_name[:-4] # Subset topic name
    region = 'Latin America & Caribbean' # Set the region
    dfy, dfc = read_world_bank_region(f_name)
    
    if len(dfc) > 3: # Check if most data are present.
        region_data = dfc[region]
        topics.append(topic) # Save the topic name
        if check == 0:
            region_df = region_data
            check += 1
        else:
            region_df = pd.concat([region_df, region_data], axis = 1)
dfr = region_df.corr()
dfr.columns = topics
r_heatmap(dfr, cmap = 'cool', region = region)




# Line Plots
# CO2
topic = 'Foreign direct investment, net inflows (% of GDP).csv'
gdp_y, gdp_c = read_world_bank_region(topic)
lineplot(gdp_c, topic[:-4])

# forest area
topic2 = 'CO2 emissions from gaseous fuel consumption (kt) .csv'
carbon_y, carbon_c = read_world_bank_region(topic2)
lineplot(carbon_c, topic2[:-4])
