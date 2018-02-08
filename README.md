# DataFrames
Practice assignments using Pandas in Python (Coursera, Intro to Data Science)


GDP and Energy
  - Use Pandas to clean and analyze data related to GDP and Global Energy consumption
  - Assignment breaks down as follows:
  
  - Question 1 
 Load the energy data from the file `Energy Indicators.xls`, which is a list of indicators of [energy supply and renewable electricity production](Energy%20Indicators.xls) from the [United Nations](http://unstats.un.org/unsd/environment/excel_file_tables/2013/Energy%20Indicators.xls) for the year 2013, and should be put into a DataFrame with the variable name of **energy**.
 
 Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer and header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and you should change the column labels so that the columns are:
 
 `['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']`
 
 Convert `Energy Supply` to gigajoules (there are 1,000,000 gigajoules in a petajoule). For all countries which have missing data (e.g. data with "...") make sure this is reflected as `np.NaN` values.
 
 Rename the following list of countries (for use in later questions):
 
 ```"Republic of Korea": "South Korea",
 "United States of America": "United States",
 "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
 "China, Hong Kong Special Administrative Region": "Hong Kong"```
 
 There are also several countries with numbers and/or parenthesis in their name. Be sure to remove these, 
 
 e.g. 
 
 `'Bolivia (Plurinational State of)'` should be `'Bolivia'`, 
 
 `'Switzerland17'` should be `'Switzerland'`.
 
 <br>
 
 Next, load the GDP data from the file `world_bank.csv`, which is a csv containing countries' GDP from 1960 to 2015 from [World Bank](http://data.worldbank.org/indicator/NY.GDP.MKTP.CD). Call this DataFrame **GDP**. 
 
 Make sure to skip the header, and rename the following list of countries:
 
 ```"Korea, Rep.": "South Korea", 
 "Iran, Islamic Rep.": "Iran",
 "Hong Kong SAR, China": "Hong Kong"```
 
 <br>
 
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
 
 
 
 
