def answer_one():
    import pandas as pd
############## Energy #######################################################################  
    energy = pd.read_excel('Energy Indicators.xls','Energy', skiprows=17, skipfooter= 38, na_values='...')
    energy = energy.drop(['Unnamed: 0', 'Unnamed: 1'], axis=1)
    
    energy.columns = ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
    
    energy['Energy Supply']= energy['Energy Supply'].convert_objects(convert_dates=False, convert_numeric=True,convert_timedeltas=False)
    energy['Energy Supply per Capita']= energy['Energy Supply per Capita'].convert_objects(convert_dates=False, convert_numeric=True,convert_timedeltas=False)
    energy['% Renewable']= energy['% Renewable'].convert_objects(convert_dates=False, convert_numeric=True,convert_timedeltas=False)
    
    #energy['Energy Supply'] = energy['Energy Supply'].apply(lambda x: (x*1000000)) This works too
    energy['Energy Supply'] = energy['Energy Supply'] * 1000000
    
    countryChange = {"Republic of Korea": "South Korea", "United States of America": "United States", "United Kingdom of Great Britain and Northern Ireland": "United Kingdom", "China, Hong Kong Special Administrative Region": "Hong Kong"}
    
    energy['Country'] = energy['Country'].str.split('\(').str[0]
    energy['Country'] = energy['Country'].str.split('\d').str[0]
    energy['Country'] = energy['Country'].str.strip()
    
    energy['Country'] = energy['Country'].replace(countryChange)
############################################################################################
############# GDP ##########################################################################
    GDP = pd.read_csv('world_bank.csv', skiprows=4)
    GDP['Country Name'] = GDP['Country Name'].replace(to_replace={"Korea, Rep.": "South Korea", 
            "Iran, Islamic Rep.": "Iran",
            "Hong Kong SAR, China": "Hong Kong"})
###########################################################################################
################ ScimEn ###################################################################
    ScimEn = pd.read_excel('scimagojr-3.xlsx')
###########################################################################################
################## Merging ################################################################

    energy = energy.set_index('Country')
    GDP = GDP.set_index('Country Name')
    ScimEn = ScimEn.set_index('Country')
    
    GDPcols = [str(i) for i in range(2006,2016)]
    GDP = GDP[GDPcols]
    
    result = pd.merge(ScimEn, GDP, how='inner', left_index=True, right_index=True)
    result = pd.merge(result, energy, how='inner', left_index=True, right_index=True)
    result = result[result['Rank']<16]
    return result


def answer_two():
    import pandas as pd
############## Energy #######################################################################  
    energy = pd.read_excel('Energy Indicators.xls','Energy', skiprows=17, skipfooter= 38, na_values='...')
    energy = energy.drop(['Unnamed: 0', 'Unnamed: 1'], axis=1)
    
    energy.columns = ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
    
    energy['Energy Supply']= energy['Energy Supply'].convert_objects(convert_dates=False, convert_numeric=True,convert_timedeltas=False)
    energy['Energy Supply per Capita']= energy['Energy Supply per Capita'].convert_objects(convert_dates=False, convert_numeric=True,convert_timedeltas=False)
    energy['% Renewable']= energy['% Renewable'].convert_objects(convert_dates=False, convert_numeric=True,convert_timedeltas=False)
    
    #energy['Energy Supply'] = energy['Energy Supply'].apply(lambda x: (x*1000000)) This works too
    energy['Energy Supply'] = energy['Energy Supply'] * 1000000
    
    countryChange = {"Republic of Korea": "South Korea", "United States of America": "United States", "United Kingdom of Great Britain and Northern Ireland": "United Kingdom", "China, Hong Kong Special Administrative Region": "Hong Kong"}
    
    energy['Country'] = energy['Country'].str.split('\(').str[0]
    energy['Country'] = energy['Country'].str.split('\d').str[0]
    energy['Country'] = energy['Country'].str.strip()
    
    energy['Country'] = energy['Country'].replace(countryChange)
############################################################################################
############# GDP ##########################################################################
    GDP = pd.read_csv('world_bank.csv', skiprows=4)
    GDP['Country Name'] = GDP['Country Name'].replace(to_replace={"Korea, Rep.": "South Korea", 
            "Iran, Islamic Rep.": "Iran",
            "Hong Kong SAR, China": "Hong Kong"})
###########################################################################################
################ ScimEn ###################################################################
    ScimEn = pd.read_excel('scimagojr-3.xlsx')
###########################################################################################
################## Merging ################################################################

    energy = energy.set_index('Country')
    GDP = GDP.set_index('Country Name')
    ScimEn = ScimEn.set_index('Country')
    
    GDPcols = [str(i) for i in range(2006,2016)]
    GDP = GDP[GDPcols]

    
    test = pd.merge(ScimEn, GDP, how='outer', left_index=True, right_index=True)
    test = pd.merge(test, energy, how='outer', left_index=True, right_index=True)
    
    result = pd.merge(ScimEn, GDP, how='inner', left_index=True, right_index=True)
    result = pd.merge(result, energy, how='inner', left_index=True, right_index=True)
    
    before = len(result.index)
    result = result[result['Rank']<16]
    after = before - len(result.index)
    
    return len(test) - len(result)

def answer_three():
    import numpy as np
    Top15 = answer_one()
    
    yrs = [str(i) for i in range(2006,2016)]

    Top15['avgGDP'] = Top15[yrs].apply(lambda x: sum(x.dropna())/len(x.dropna()), axis=1)# Original
    
    #Top15['avgGDP'] = Top15[yrs].apply(lambda x: np.average(x))
    

    Top15 = Top15.sort_values(by='avgGDP', ascending=False)
    return Top15['avgGDP']

def answer_four():
    Top15 = answer_one()
    
    Top15['avgGDP'] = answer_three()
    
    Top15['change'] = Top15['2015'] - Top15['2006']
    
    Top15 = Top15.sort_values(by='avgGDP', ascending=False)
    
    return Top15['change'][5]


def answer_five():
    import numpy as np
    Top15 = answer_one()
    
    result = sum(Top15['Energy Supply per Capita'].dropna())/len(Top15['Energy Supply per Capita'].dropna())
    #result = np.average(Top15['Energy Supply per Capita'])
    
    return np.asscalar(result)


def answer_six():
    Top15 = answer_one()
    
    Top15 = Top15.sort_values(by='% Renewable')
    return (Top15.iloc[-1].name, Top15['% Renewable'][-1])


def answer_seven():
    Top15 = answer_one()
    
    Top15['Ratio of Self to Total Citations'] = Top15['Self-citations']/Top15['Citations']
    Top15 = Top15.sort_values(by='Ratio of Self to Total Citations')
    
    return (Top15.index[-1], Top15['Ratio of Self to Total Citations'][-1])

def answer_eight():
    Top15 = answer_one()
    
    Top15['Population Estimate'] = Top15['Energy Supply']/Top15['Energy Supply per Capita']
    Top15 = Top15.sort_values(by='Population Estimate', ascending=False)
    
    return Top15.index[2]


def answer_nine():
    Top15 = answer_one()

    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['Citable docs per Capita'] = Top15['Citable documents'] / Top15['PopEst']

    return Top15['PopEst'].corr(Top15['Citable docs per Capita'], method='pearson')


def answer_ten():
    import statistics
    Top15 = answer_one()
    
    Top15 = Top15.sort_values(by='% Renewable')
    
    Top15['Median'] = statistics.median(Top15['% Renewable'])
    
    Top15['HighRenew'] = Top15['% Renewable'].where(Top15['% Renewable'] < Top15['Median'], other = 1)
    
    Top15['HighRenew'] = Top15['HighRenew'].apply(lambda x: 1 if x == 1 else 0)
    
    Top15 = Top15.sort_values(by='Rank', ascending=True)
    return Top15['HighRenew']


def answer_eleven():
    import numpy as np
    import pandas as pd
    Top15 = answer_one()

    ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15 = Top15.groupby(by=ContinentDict)
    
    #for group,frame in Top15:
     #   print(str(group) + ' : ' + str(len(frame)))
    
    #Top15.get_group('Asia').describe()['PopEst']['std']#.apply(lambda x: print(str(x)))
    
    
    df = pd.DataFrame(columns=['size', 'sum', 'mean', 'std'], index=['Asia', 'Australia', 'Europe', 'North America', 'South America'])
    df['mean'] = Top15.agg({'PopEst': np.average})
    df['sum'] = Top15.agg({'PopEst': np.sum})
    df['std'] = Top15.agg({'PopEst': np.std})
    df['size'] = Top15.apply(lambda x: len(x))
    return df


def answer_thirteen():
    Top15 = answer_one()
    
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    
    Top15['PopEst'] = Top15['PopEst'].apply(lambda x: '{:,}'.format(x))
    
    return Top15['PopEst']

