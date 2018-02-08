
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# In[1]:

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# # Assignment 4 - Hypothesis Testing
# This assignment requires more individual learning than previous assignments - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.
# 
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
# 
# Each function in this assignment below is worth 10%, with the exception of ```run_ttest()```, which is worth 50%.

# In[2]:

# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


# In[3]:



def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    
    towns = pd.read_csv('university_towns.txt', sep='\n', header=None, names=['raw data'])
    schools = []
            
    for row in towns['raw data']:
        if '[ed' in row:
            curr = row.split('[')[0].strip() #replace(' ','')
        else:
            schools.append([curr, row.split('(')[0].strip()]) #replace(' ','')])
    
    towns = pd.DataFrame(schools, columns=['State','RegionName'])
    return towns
get_list_of_university_towns()


# In[4]:

def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    
    gdp = pd.read_excel('gdplev.xls', skiprows=9)
    a = [gdp.columns[4], gdp.columns[5], gdp.columns[6]]
    
    cols = {gdp.columns[4]:'Quarter', gdp.columns[5]:'GDP in Current Dollars',gdp.columns[6]:'GDP in Billions chained 09 dollars'}    
    gdp = gdp[a].rename(columns=cols)

    gdp = gdp.set_index('Quarter')
    gdp = gdp.loc['2000q1':]
    
    start = None
    
    for x in range(1, len(gdp['GDP in Current Dollars']), 1):
        if ((gdp['GDP in Current Dollars'][x] < gdp['GDP in Current Dollars'][x-1]) and (gdp['GDP in Current Dollars'][x] > gdp['GDP in Current Dollars'][x+1])):
            start = gdp.iloc[x-1].name#gdp['GDP in Current Dollars'][x-1]
            break
    
    return start
get_recession_start()


# In[5]:

def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    
    gdp = pd.read_excel('gdplev.xls', skiprows=9)
    a = [gdp.columns[4], gdp.columns[5], gdp.columns[6]]
    
    cols = {gdp.columns[4]:'Quarter', gdp.columns[5]:'GDP in Current Dollars',gdp.columns[6]:'GDP in Billions chained 09 dollars'}    
    gdp = gdp[a].rename(columns=cols)

    gdp = gdp.set_index('Quarter')
    gdp = gdp.loc[get_recession_start():]
    
    end = None
    
    for x in range(1, len(gdp['GDP in Current Dollars']), 1):
        if ((gdp['GDP in Current Dollars'][x] > gdp['GDP in Current Dollars'][x-1]) and (gdp['GDP in Current Dollars'][x] < gdp['GDP in Current Dollars'][x+1])):
            end = gdp.iloc[x+1].name#gdp['GDP in Current Dollars'][x-1]
            break
       
    return end
get_recession_end()


# In[6]:

def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    
    gdp = pd.read_excel('gdplev.xls', skiprows=9)
    a = [gdp.columns[4], gdp.columns[5], gdp.columns[6]]
    
    cols = {gdp.columns[4]:'Quarter', gdp.columns[5]:'GDP in Current Dollars',gdp.columns[6]:'GDP in Billions chained 09 dollars'}    
    gdp = gdp[a].rename(columns=cols)

    gdp = gdp.set_index('Quarter')
    gdp = gdp.loc[get_recession_start():get_recession_end()]
    
    
    bottom = gdp.where(gdp['GDP in Current Dollars']==min(gdp['GDP in Current Dollars'])).dropna().index[0]
    
    return bottom
get_recession_bottom()


# In[7]:

def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    
    #Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
    
    import numpy as np
    
    housing = pd.read_csv('City_Zhvi_AllHomes.csv')

    a = housing.columns[51:]
    
    housing['State'] = housing['State'].replace(states)
    
    housing = housing.set_index(['State','RegionName'])
    
    housing = housing[a]
    
    quarter = []
    for x in housing:
        if len(quarter) == 3:
            #Combine and find mean....not necessarily in that order....or maybe..idk yo
            yr, month = quarter[0].split('-')
            q = None
            if int(month) < 4:
                q = "q1"
            elif int(month) < 7:
                q = "q2"
            elif int(month) < 10:
                q = "q3"
            else:
                q = "q4"
                    
            housing[yr + q] = (housing[quarter[0]]+housing[quarter[1]]+ housing[quarter[2]])/3#housing.apply(lambda p: (p[quarter[0]] + p[quarter[1]] + p[quarter[2]])/3)
            
            
            housing = housing.drop(quarter, axis=1)
            quarter.clear()

        quarter.append(x)
    
    housing['2016q3'] = (housing['2016-07'] + housing['2016-08'])/2
    housing = housing.drop(['2016-07','2016-08'], axis=1)
    
    return housing
convert_housing_data_to_quarters()


# In[47]:

def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    
    university_towns= get_list_of_university_towns()
    housing = convert_housing_data_to_quarters()
    
    rec_bottom = get_recession_bottom()
    yr, quarter = rec_bottom.split('q')
    ### Finding the last quarter before the recession began ########################################
    if quarter == 1:
        yr = int(yr) - 1
        quarter = 4
    else:
        quarter = int(quarter) - 1
        
    lastGoodyr = str(yr) + 'q' + str(quarter)
    #################################################################################################
    #### Finding ratio of prices in good economic time to prices in bad economic time ################
    housing['pRatio'] = housing[lastGoodyr]/housing[rec_bottom]
    
    uniList = university_towns.to_records(index = False).tolist()
    
    uni_housing = housing.loc[uniList].dropna()
    other_housing = housing.loc[-housing.index.isin(uniList)].dropna()
    
    ####### Performing T-test on price ratios #####################
    
    uni_housing = uni_housing
    other_housing = other_housing
    
    results = ttest_ind(uni_housing['pRatio'], other_housing['pRatio'])
    
    best = 'university town' if uni_housing['pRatio'].mean() < other_housing['pRatio'].mean() else 'non-university town'
    
    results = (True if float(results[1]) < .01 else False, results[1], best)
    
    return results
run_ttest()


# In[ ]:



