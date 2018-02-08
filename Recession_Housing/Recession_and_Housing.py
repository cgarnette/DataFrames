

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}

def get_list_of_university_towns():
    
    towns = pd.read_csv('university_towns.txt', sep='\n', header=None, names=['raw data'])
    schools = []
            
    for row in towns['raw data']:
        if '[ed' in row:
            curr = row.split('[')[0].strip() #replace(' ','')
        else:
            schools.append([curr, row.split('(')[0].strip()]) #replace(' ','')])
    
    towns = pd.DataFrame(schools, columns=['State','RegionName'])
    return towns


def get_recession_start():
    
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


def get_recession_end():
    
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

def get_recession_bottom():
    
    gdp = pd.read_excel('gdplev.xls', skiprows=9)
    a = [gdp.columns[4], gdp.columns[5], gdp.columns[6]]
    
    cols = {gdp.columns[4]:'Quarter', gdp.columns[5]:'GDP in Current Dollars',gdp.columns[6]:'GDP in Billions chained 09 dollars'}    
    gdp = gdp[a].rename(columns=cols)

    gdp = gdp.set_index('Quarter')
    gdp = gdp.loc[get_recession_start():get_recession_end()]
    
    
    bottom = gdp.where(gdp['GDP in Current Dollars']==min(gdp['GDP in Current Dollars'])).dropna().index[0]
    
    return bottom

def convert_housing_data_to_quarters():
    
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

def run_ttest():
    
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



