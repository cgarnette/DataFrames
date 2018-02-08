# DataFrames
Practice assignments using Pandas in Python (Coursera, Intro to Data Science)

Recession Housing
  - Use Pandas to clean and analyze data related to GDP and Housing
  - Find whether University towns or non-University towns were more heavily effected by the 2008 Recession in the United States. In terms of the housing market.
  - Break down is as follows:
  ``` 
  * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), "City_Zhvi_AllHomes.csv", has median home sale prices at a fine grained level.
 * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_townsCollege_towns_in_the_United_States) which has been copy and pasted into the file "university_towns.txt".
 * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htmgdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file "gdplev.xls". For this assignment, only look at GDP data from the first quarter of 2000 onward.
 
 
get_list_of_university_towns :
    Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning has been done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'.
	

 get_recession_start :
    Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3
    
 get_recession_end :
    Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3
    
 get_recession_bottom :
    Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3
    
 convert_housing_data_to_quarters :
    Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].

 run_ttest :
    First creates new data showing the decline or growth of housing prices
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
    reduced market loss).
  ```
  

GDP and Energy
  - Use Pandas to clean and analyze data related to GDP and Global Energy consumption
  - Assignment breaks down as follows:
  ```
  - Question 1 
 Load the energy data from the file `Energy Indicators.xls`, which is a list of indicators of [energy supply and renewable electricity production](Energy%20Indicators.xls) from the [United Nations](http://unstats.un.org/unsd/environment/excel_file_tables/2013/Energy%20Indicators.xls) for the year 2013, and should be put into a DataFrame with the variable name of **energy**.
 
 Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer and header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and you should change the column labels so that the columns are:
 
 `['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']`
 
 Convert `Energy Supply` to gigajoules (there are 1,000,000 gigajoules in a petajoule). For all countries which have missing data (e.g. data with "...") make sure this is reflected as `np.NaN` values.
 
 Rename the following list of countries (for use in later questions):
 
 "Republic of Korea": "South Korea",
 "United States of America": "United States",
 "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
 "China, Hong Kong Special Administrative Region": "Hong Kong"
 
 There are also several countries with numbers and/or parenthesis in their name. Be sure to remove these, 
 
 e.g. 
 
 `'Bolivia (Plurinational State of)'` should be `'Bolivia'`, 
 
 `'Switzerland17'` should be `'Switzerland'`.

 
 Next, load the GDP data from the file `world_bank.csv`, which is a csv containing countries' GDP from 1960 to 2015 from [World Bank](http://data.worldbank.org/indicator/NY.GDP.MKTP.CD). Call this DataFrame **GDP**. 
 
 Make sure to skip the header, and rename the following list of countries:
 
 ```"Korea, Rep.": "South Korea", 
 "Iran, Islamic Rep.": "Iran",
 "Hong Kong SAR, China": "Hong Kong"

 
 Finally, load the [Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology](http://www.scimagojr.com/countryrank.php?category=2102) from the file `scimagojr-3.xlsx`, which ranks countries based on their journal contributions in the aforementioned area. Call this DataFrame **ScimEn**.
 
 Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15). 
 
 The index of this DataFrame should be the name of the country, and the columns should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
        'Citations per document', 'H index', 'Energy Supply',
        'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008',
        '2009', '2010', '2011', '2012', '2013', '2014', '2015'].
   
  -  Question 2
 The previous question joined three datasets then reduced this to just the top 15 entries. When you joined the datasets, but before you reduced this to the top 15 items, how many entries did you lose?
 
  - Question 3
 What is the average GDP over the last 10 years for each country? (exclude missing values from this calculation.)
 
  - Question 4
 By how much had the GDP changed over the 10 year span for the country with the 6th largest average GDP?
 
  - Question 5
 What is the mean `Energy Supply per Capita`?
 
  - Question 6
 What country has the maximum % Renewable and what is the percentage?
 
  - Question 7
 Create a new column that is the ratio of Self-Citations to Total Citations. 
 What is the maximum value for this new column, and what country has the highest ratio?
 
  - Question 8
 Create a column that estimates the population using Energy Supply and Energy Supply per capita. 
 What is the third most populous country according to this estimate?
 
  - Question 9
 Create a column that estimates the number of citable documents per person. 
 What is the correlation between the number of citable documents per capita and the energy supply per capita? Use the `.corr()` method, (Pearson's correlation).
 
  - Question 10
 Create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the top 15, and a 0 if the country's % Renewable value is below the median.
 
  - Question 11
 Use the following dictionary to group the Countries by Continent, then create a dateframe that displays the sample size (the number of countries in each continent bin), and the sum, mean, and std deviation for the estimated population of each country.
 
  - Question 13
 Convert the Population Estimate series to a string with thousands separator (using commas). Do not round the results.
 
 ```
 
 
