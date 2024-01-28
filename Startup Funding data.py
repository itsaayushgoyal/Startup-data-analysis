#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
dataset = pd.read_csv('startup_funding.csv')


# In[2]:


dataset.sample(5)


# In[3]:


dataset.shape


# In[5]:


dataset.info()


# ### CHANGING COLUMN NAMES SO THAT IT WILL BE EASY TO ACCESS

# In[6]:


dataset.columns = ['SNo', 'Date', 'StartupName', 'IndustryVertical', 'SubVertical', 'City', 'InvestorName', 'InvestorType', 'Amount', 'Remarks']
dataset.dtypes


# In[7]:


dataset.drop(['SNo'], axis = 1, inplace = True)


# In[8]:


dataset.info()


# ## 1. date column cleaning 

# In[9]:


import re

dates = dataset.Date.unique()
len(dates)
for date in dates :
    if not re.match(r'^[0-9]{2}/[0-9]{2}/[0-9]{4}$', date) :
        print(date)


# In[10]:


import datetime

def fixDates(date) :
    if re.match(r'^[0-9]{2}/[0-9]{6}$', date) :
        dateContents = date.split('/')
        date = (dateContents[0] + '/' + dateContents[1][:2] + '/' + dateContents[1][2:])
    
    if re.match(r'^[0-9]{2}/[0-9]{2}/[0-9]{3}$', date) :
        dateContents = date.split('/')
        date = (dateContents[0] + '/' + dateContents[1] + '/2' + dateContents[2])
    
    if re.match(r'^\\.*$', date) :
        dateContents = date.split('/')
        date = (dateContents[0][-2:] + r'/0' + dateContents[1] + '/' + dateContents[2])
    
    if re.match(r'^[0-9]{2}/[0-9]{2}\.[0-9]{4}$', date) :
        dateContents1 = date.split('/')
        dateContents2 = dateContents1[1].split('.')
        date = (dateContents1[0] + '/' + dateContents2[0] + '/' + dateContents2[1])
    
    if re.match(r'^[0-9]{2}/[0-9]{2}//[0-9]{4}$', date) :
        dateContents1 = date.split('//')
        dateContents2 = dateContents1[0].split('/')
        date = (dateContents2[0] + '/' + dateContents2[1] + '/' + dateContents1[1])
    
    return date


# In[11]:


dataset.Date= dataset.Date.apply(fixDates)


# In[12]:


dataset.Date = pd.to_datetime(dataset.Date)
dataset.Date.isna().sum()


# In[13]:


dataset.info()


# ### 2. Startup Names

# In[14]:


sNames = dataset.StartupName.unique()
for name in sNames :
    print(name)


# In[15]:


def fixStartupNames(name) :
    name = name.strip("\"").strip() # Rule 1
    name = name.replace('\u2019', '\'') # Rule 2
    name = name.replace(r'\\xe2\\x80\\x99', '\'') # Rule 3
    name = name.replace(r'\xe2\x80\x99', '\'') # Rule 4
    name = name.replace(r'\\xc2\\xa0', '') # Rule 5
    name = name.replace(r'\n', r' ') # Rule 6
    name = name.replace('\\', '') # Rule 7
    # Rule 8
    if name.startswith('https://') :
        name = name[8: ]
    if name.startswith('www.') :
        name = name[4: ]
    if name.endswith('/') :
        name = name[: len(name) - 1]
    
    # Rule 9 
    if name == "Ola Cabs" or name == "Ola Electric" or name == "Olacabs" :
        name = 'Ola'
    
    # Rule 10
    if name == "Flipkart.com" :
        name = "Flipkart"
    
    # Rule 11
    if name == "Oyorooms" or name == "OYOfit" or name == "Oyo Rooms" or name == "OYO Rooms" or name == "OyoRooms" :
        name = 'Oyo'
    
    # Rule 12
    if name == "Rapido Bike Taxi" :
        name = "Rapido"
    
    # Rule 13
    if name == "Paytm Marketplace" :
        name = 'Paytm'
    return " ".join([component.capitalize() for component in name.split()])


# In[16]:


dataset.StartupName = dataset.StartupName.apply(fixStartupNames)


# In[17]:


dataset.StartupName.isna().sum()


# ### 3. Industry Vertical 

# In[18]:


industryverticals = dataset.IndustryVertical.unique()
for industryVertical in sorted(industryverticals.astype(str)) :
    print(industryVertical)


# In[19]:


def fixIndustryVertical(name) :
    name = name.replace(r'\\xc2\\xa0', '') # Rule 1
    name = name.replace(r'\\xe2\\x80\\x99', '\'') # Rule 2
    name = name.replace(r'\xe2\x80\x99', '') # Rule 3
    name = name.replace(r'\xe2\x80\x93', '') # Rule 4
    name = name.replace(r'\\xc3\\xa9', 'e') # Rule 5
    name = name.replace(r'\n', r' ') # Rule 6
    name = name.replace('\\', '') # Rule 7
    # Rule 8
    name = "".join(name.strip().split('-'))
    return " ".join([component.capitalize() for component in name.split()])


# In[20]:


dataset.IndustryVertical.isna().sum()


# In[21]:


dataset.IndustryVertical.fillna("Unknown",inplace=True)


# In[22]:


dataset.IndustryVertical = dataset.IndustryVertical.apply(fixIndustryVertical)


# In[23]:


dataset.IndustryVertical.isna().sum()


# ### 4. Sub Verticals

# In[24]:


subVerticals = dataset.SubVertical.unique()
for subVertical in sorted(subVerticals.astype(str)) :
    print(subVertical)


# In[25]:


def fixSubVerticals(name) :
    name = name.strip("\"").strip() # Rule 1
    # Rule 2
    name = name.replace(r'\\xe2\\x80\\x99', '')
    name = name.replace(r'\xe2\x80\x99', '')
    name = name.replace(r'\\xc2\\xa0', ' ') # Rule 3
    name = name.replace(r'\\xc3\\xa9', 'e') # Rule 4
    name = name.replace(r'\n', r' ') # Rule 5
    name = name.replace('\\', '') # Rule 7
    # Rule 6
    googleAdIndex = name.find("(adsbygoogle")
    if googleAdIndex != -1 :
        name = name[: googleAdIndex]
    # Rule 8
    name = "".join(name.strip().split('-'))
    return " ".join([component.capitalize() for component in name.split()])


# In[26]:


dataset.SubVertical.isna().sum()


# In[27]:


dataset.SubVertical.fillna("Unknown",inplace=True)


# In[28]:


dataset.SubVertical = dataset.SubVertical.apply(fixSubVerticals)


# ### 5. City

# In[29]:


cities = dataset.City.unique()
for city in sorted(cities.astype(str)) :
    print(city)


# In[30]:


cityCorrections = {'Ahemadabad': 'Ahmedabad', 'Ahemdabad': 'Ahmedabad', 'Bengaluru': 'Bangalore', 'Bhubneswar': 'Bhubaneswar', 'Gurgaon': 'Gurugram', 'Kolkatta': 'Kolkata', 'Nw Delhi': 'New Delhi', 'USA': 'US'}
def fixCity(name) :
    name = name.replace(r'\\xc2\\xa0', '').strip().strip(',') # Rule 1
    # Rule 2
    nameList = re.split('/|,| & | and ', name)
    for index in range(len(nameList)) :
        cityName = nameList[index].strip().strip(',')
        if cityName in cityCorrections :
            cityName = cityCorrections[cityName]
        nameList[index] = cityName
    nameList.sort()
    
    return ", ".join(nameList)


# In[32]:


dataset.City.isna().sum()


# In[33]:


dataset.City.fillna("Unknown",inplace=True)
dataset.City = dataset.City.apply(fixCity)


# ### 6. Investor Name

# In[34]:


investorNames = dataset.InvestorName.unique()
for investorName in sorted(investorNames.astype(str)) :
    print (investorName)


# In[35]:


def fixInvestorName(name) :
    name = name.strip("\"").strip() # Rule 1
    # Rule 2
    name = name.replace(r'\\xe2\\x80\\x99', '\'')
    name = name.replace(r'\\xc2\\xa0', '') # Rule 3
    name = name.replace(r'\\xc3\\x98', 'o') # Rule 4
    name = name.replace(r'\\xc3\\xa9', 'e') # Rule 5
    name = name.replace(r'\\xc3\\xaf', 'i') # Rule 6
    name = name.replace(r'\n', r' ') # Rule 7
    name = name.replace('\\', '') # Rule 8
    # Rule 9
    name = "".join(name.strip().split('-'))
    name = " ".join([component.capitalize() for component in name.split()])
    
    # Rule 10
    names = []
    for _name in re.split(",| And ", re.sub("\(.*?\)", '', name)) :
        names.append(" ".join([component.capitalize() for component in _name.strip().rstrip('.').strip().split()]))
    return ",".join(names).strip(',').strip()


# In[36]:


dataset.InvestorName.isna().sum()


# In[37]:


dataset.InvestorName.fillna("Undisclosed",inplace=True)
dataset.InvestorName= dataset.InvestorName.apply(fixInvestorName)


# ### 7. Investor Type

# In[38]:


investorTypes = dataset.InvestorType.unique()
for investorType in sorted(investorTypes.astype(str)) :
    print(investorType)


# In[39]:


def fixInvestorTypes(name) :
    # Rule 1
    if name.startswith('Funding Round') :
        return 'Funding Round'
    if name.startswith('PrivateEquity') :
        return 'Private Equity'
    
    # Rule 2
    name = name.replace(r'\n', r' ')
    name = name.replace('\\', '')
    
    # Rule 3
    name = name.replace('-', ' ')
    
    # Rule 4
    name = name.replace('Angle', 'Angel')
    
    # Rule 5
    name = name.replace('Funding', '')
    name = name.replace('funding', '')
    name = name.replace('Based', '')
    
    # Rule 6
    cityList = name.split('/')
    for index in range(len(cityList)) :
        cityName = cityList[index].strip()
        cityList[index] = " ".join([component.capitalize() for component in cityName.split()])
    
    cityList.sort()
    return ", ".join(cityList)


# In[40]:


dataset.InvestorType.isna().sum()


# In[41]:


dataset.InvestorType.fillna('Undefined', inplace = True)
dataset.InvestorType = dataset.InvestorType.apply(fixInvestorTypes)


# ### 8. Amount

# In[42]:


amounts = dataset.Amount.unique()
for amount in sorted(amounts.astype('str')) :
    print(amount)


# In[43]:


def fixAmount(amount) :
    # Rule 1
    amount = amount.lower().strip('+').strip()
    
    # Rule 2
    amount = amount.replace(r'\\xc2\\xa0', '')
    
    # Rule 3
    amount = amount.replace('undisclosed', '0')
    amount = amount.replace('unknown', '0')
    amount = amount.replace('n/a', '0')
    amount = amount.replace('nan', '0')
    
    # Rule 4
    amount = amount.replace(',', '')
    
    # Rule 5
    return amount.strip()


# In[44]:


dataset.Amount.isna().sum()


# In[45]:


dataset.Amount.fillna("0", inplace = True)
dataset.Amount = dataset.Amount.apply(fixAmount).astype('float')


# In[46]:


numOfRowsWith0 = dataset[dataset.Amount == 0].shape[0]
numOfRowsWith0


# In[47]:


InvestorToMeanVals = {}
InvestorTypes = dataset.InvestorType.unique()
for investorType in InvestorTypes :
    InvestorToMeanVals[investorType] = dataset[(dataset.InvestorType == investorType) & (dataset.Amount != 0)].Amount.mean()


# In[48]:


for investorType in InvestorToMeanVals :
    dataset.loc[(dataset.InvestorType == investorType) & (dataset.Amount == 0), 'Amount'] = InvestorToMeanVals[investorType]


# In[49]:


dataset.Amount.isna().sum()


# In[50]:


dataset.Amount.fillna(0, inplace = True)


# ### 9. Remarks

# In[51]:


remarks = dataset.Remarks.unique()
for remark in sorted(remarks.astype(str)) :
    print(remark)


# In[52]:


dataset.Remarks.isna().sum()


# In[53]:


dataset.drop(['Remarks'], axis = 1, inplace = True)


# In[ ]:





# # Let's check the cleaned data

# In[54]:


dataset.sample(5)


# In[ ]:





# # visualization of cleaned Data

# In[55]:


import matplotlib.pyplot as plt
import numpy as np
import random


# In[56]:


colours = ['green', 'blue', 'orange', 'purple', 'magenta', 'red', 'yellow', 'cyan', 'chocolate', 'skyblue']


# In[ ]:





# ## 1. Trend of investments' frequency over the years 2015 - 2020, using line graph between year and number of fundings  :

# In[57]:


years = dataset.Date.dt.year
year = []
frequency = []
yearWithFrequency = years.value_counts()
for _year in sorted(yearWithFrequency.index) :
    year.append(_year)
    frequency.append(yearWithFrequency[_year])


# In[58]:


plt.figure(figsize = (10, 6))
plt.plot(year, frequency, 'b-->')
plt.title('Trend of total number of fundings over years from 2015 to 2020')
plt.xlabel('Year')
plt.ylabel('Number of fundings')
for _year, freq in zip(year, frequency) :
    plt.text(_year, freq, str(freq))
plt.grid()
plt.show()


# ## 2. Top 10 Indian Cities which has most no. of startups

# In[59]:


knownCitiesDataset = dataset[dataset.City != 'Unknown']
#knownCitiesDataset
cities = knownCitiesDataset.City
#cities
relevantData = cities.value_counts()[: 10]
city = relevantData.index
startupCounts = relevantData.values 


# In[60]:


currentColors = random.sample(colours, 10)

plt.figure(figsize = (20, 7))

plt.subplot(1, 2, 1)
plt.pie(startupCounts, labels = city, autopct = '%.2f%%', explode = [0.05 for _ in range(len(startupCounts))], colors = currentColors)
plt.title('Percentage of startup counts for top 10 cities in India')
plt.axis('equal')

plt.subplot(1, 2, 2)
plt.grid(alpha = 0.3)
for _city, _startupCount, colour in zip(city, startupCounts, currentColors) :
    plt.bar(_city, _startupCount, color = colour)
    plt.text(_city, _startupCount, str(_startupCount))
plt.title('Top 10 cities with the most startups')
plt.ylabel('Number of funding rounds')
plt.xlabel('City Name')
plt.xticks(rotation = 40)

plt.suptitle('Illustrations of top 10 cities with the highest count of startup')

plt.show()


# ## 3. Top 10 Indian Cities which recieved most amount of fundings 

# In[61]:


from collections import Counter

cityWithTotalAmount = Counter()
for city, amount in zip(knownCitiesDataset.City, knownCitiesDataset.Amount) :
    cityWithTotalAmount[city] += amount
    
relevantData = cityWithTotalAmount.most_common()[: 10]
city = []
totalStartupAmount = []

for content in relevantData :
    city.append(content[0])
    totalStartupAmount.append(content[1])


# In[62]:


currentColors = random.sample(colours, 10)

plt.figure(figsize = (20, 7))

plt.subplot(1, 2, 1)
plt.pie(totalStartupAmount, labels = city, autopct = '%.2f%%', explode = [0.05 for _ in range(len(startupCounts))], colors = currentColors)
plt.title('Percentage of total startup amount for top 10 cities in India over period 2015 - 2020')
plt.axis('equal')

plt.subplot(1, 2, 2)
for _city, amount, colour in zip(city, totalStartupAmount, currentColors) :
    plt.bar(_city, amount / 10, color = colour)
    plt.text(_city, amount / 10, str(round(amount / (10 ** 9), 2)))
plt.xlabel('City')
plt.ylabel('Total funds for startup (in Billion USD)')
plt.xticks(rotation = 40)
plt.title('City-wise total funding amount')
plt.grid(alpha = 0.3)

plt.show()


# ## 4. Percentage of amount funded for investment types that are Private Equity, Seed Funding, Debt Funding, and Crowd Funding :

# In[63]:


definedInvestorTypeDataset = dataset[dataset.InvestorType != 'Undefined']
investorTypeToTotalAmount = Counter()

for investorType, amount in zip(definedInvestorTypeDataset.InvestorType, definedInvestorTypeDataset.Amount) :
    investorTypeToTotalAmount[investorType] += amount

inverstorType = ['Private', 'Seed', 'Debt', 'Crowd']
amount = [0, 0, 0, 0]
for content in investorTypeToTotalAmount.most_common() :
    if 'private' in content[0].lower() :
        amount[0] += content[1]
    if 'seed' in content[0].lower() :
        amount[1] += content[1]
    if 'debt' in content[0].lower() :
        amount[2] += content[1]
    if 'crowd' in content[0].lower() :
        amount[3] += content[1]


# In[64]:


investorTypeToTotalAmount.most_common()


# In[65]:


currentColors = random.sample(colours, 4)

plt.figure(figsize = (7, 7))
plt.pie(amount, labels = inverstorType, autopct = "%.2f%%", explode = [0.05 for _ in range(len(amount))], colors = currentColors)
plt.title('Percentage of total amount funded amongst investment types : Private Equity, Seed Funding, Debt Funding, Crowd Funding')
plt.axis('equal')

plt.show()


# ## 5. Top 5  industries which get most funding 

# In[66]:


validIndustryDataset = dataset[dataset.IndustryVertical != 'Unknown']

industryTypeWithTotalFunding = Counter()
for industryType, amount in zip(validIndustryDataset.IndustryVertical, validIndustryDataset.Amount) :
    industryTypeWithTotalFunding[industryType] += amount

relevantData = industryTypeWithTotalFunding.most_common()[: 5]
industryType = []
totalAmount = []
for content in relevantData :
    industryType.append(content[0])
    totalAmount.append(content[1])


# In[67]:


currentColors = random.sample(colours, 5)

plt.figure(figsize = (7, 7))
plt.pie(totalAmount, labels = industryType, autopct = '%.2f%%', explode = [0.05 for _ in range(len(totalAmount))], colors = currentColors)
plt.title('Percenage of total amount for top 10 funded industry types')
plt.axis('equal')

plt.show()


# ## 6  10 Startups with the maximum amount of funding 

# In[68]:


startupsWithTotalFunding = Counter()

for startup, amount in zip(dataset.StartupName, dataset.Amount) :
    startupsWithTotalFunding[startup] += amount

relevantData = startupsWithTotalFunding.most_common()[: 10]
startup = []
totalAmount = []

for content in relevantData :
    startup.append(content[0])
    totalAmount.append(content[1])


# In[69]:


currentColors = random.sample(colours, 10)

plt.figure(figsize = (10, 7))
for _startup, _totalAmount, colour in zip(startup, totalAmount, currentColors) :
    plt.bar(_startup, _totalAmount, color = colour)
    plt.text(_startup, _totalAmount, str(round(_totalAmount / (10 ** 9), 2)))

plt.title('Startups with maximum total funding amount')
plt.xlabel('Startup Name')
plt.ylabel('USD(in Billions)')
plt.xticks(rotation = 40)

plt.show()


# ## 7. Top 10 startups which had the most funding rounds :

# In[70]:


relevantData = dataset.StartupName.value_counts()[: 10]
startup = relevantData.index
rounds = relevantData.values


# In[71]:


plt.figure(figsize = (14, 7))
plt.stem(rounds, markerfmt = ' ')

(markers, stemlines, baseline) = plt.stem(rounds)
plt.setp(markers, marker = 'X', markersize = 10, markeredgecolor = "orange", markeredgewidth = 1, color = 'red')
index = 0
for _startup, _round, colour in zip(startup, rounds, currentColors) :
    plt.text(index, _round, str(_startup) + '\n(' + str(_round) + ")", rotation = 40)
    index += 1

plt.tick_params(axis = 'x', which = 'both', bottom = False, top = False, labelbottom = False)
plt.ylabel('Number of funding rounds')
plt.title('Top 10 startups with the most funding rounds')
plt.ylim(0, 16)
plt.xlim(-1, 10)
plt.show()


# ## 8. Top 5 Investors, who have invested for maximum number of times :

# In[72]:


knownInvestorsDataset = dataset[dataset.InvestorName != 'Undisclosed Investors']

investorWithFrequency = Counter()
for names in knownInvestorsDataset.InvestorName :
    for name in names.split(',') :
        investorWithFrequency[name] += 1

relevantData = investorWithFrequency.most_common()[: 5]
investorName = []
investorFrequency = []

for content in relevantData :
    investorName.append(content[0])
    investorFrequency.append(content[1])


# In[73]:


currentColors = random.sample(colours, 5)

plt.figure(figsize = (14, 7))
plt.stem(investorFrequency, markerfmt = ' ')

(markers, stemlines, baseline) = plt.stem(investorFrequency)
plt.setp(markers, marker = 'X', markersize = 10, markeredgecolor = "orange", markeredgewidth = 1, color = 'red')
index = 0
for name, freq, colour in zip(investorName, investorFrequency, currentColors) :
    plt.text(index, freq, str(name) + '\n(' + str(freq) + ")", rotation = 40)
    index += 1

plt.tick_params(axis = 'x', which = 'both', bottom = False, top = False, labelbottom = False)
plt.ylabel('Number of times funding done by these investors')
plt.title('Top 5 investors with the most frequency in funding')
plt.ylim(0, 100)
plt.xlim(-1, 5)

plt.show()


# ## 9. Funding of the 4 major investment types, that are Private Equity, Seed Funding, Debt Funding, and Crowd Funding over 2015 - 2020:

# In[74]:


privateData = {}
seedData = {}
debtData = {}
crowdData = {}

for year in dataset.Date.dt.year :
    privateData[year] = 0
    seedData[year] = 0
    debtData[year] = 0
    crowdData[year] = 0

for index in range(dataset.shape[0]) :
    fundType = dataset.loc[index].InvestorType.lower()
    amount = dataset.loc[index].Amount
    year = dataset.loc[index].Date.year
    if 'private' in fundType :
        privateData[year] += amount
    if 'seed' in fundType :
        seedData[year] += amount
    if 'debt' in fundType :
        debtData[year] += amount
    if 'crowd' in fundType :
        crowdData[year] += amount

privateYears = sorted(privateData.keys())
privateAmount = []
for year in privateYears :
    privateAmount.append(privateData[year] / (10 ** 9))

seedYears = sorted(seedData.keys())
seedAmount = []
for year in seedYears :
    seedAmount.append(seedData[year] / (10 ** 9))

debtYears = sorted(debtData.keys())
debtAmount = []
for year in debtYears :
    debtAmount.append(debtData[year] / (10 ** 9))

crowdYears = sorted(crowdData.keys())
crowdAmount = []
for year in crowdYears :
    crowdAmount.append(crowdData[year] / (10 ** 9))


# In[75]:


currentColor = random.sample(colours, 4)

plt.figure(figsize = (30, 7))

plt.subplot(1, 3, 1)
plt.plot(privateYears, privateAmount, label = 'Private Funding', color = currentColor[0])
plt.plot(seedYears, seedAmount, label = 'Seed Funding', color = currentColor[1])
plt.plot(debtYears, debtAmount, label = 'Debt Funding', color = currentColor[2])
plt.plot(crowdYears, crowdAmount, label = 'Crowd Funding', color = currentColor[3])
plt.legend(title = 'Funding Type')
plt.grid()
plt.xlabel('Years')
plt.ylabel('Total Funding Amount(in Billion $)')

plt.subplot(1, 3, 2)
plt.plot(seedYears, [(amount * 1000) for amount in seedAmount], label = 'Seed Funding', color = currentColor[1])
plt.plot(debtYears, [(amount * 1000) for amount in debtAmount], label = 'Debt Funding', color = currentColor[2])
plt.plot(crowdYears, [(amount * 1000) for amount in crowdAmount], label = 'Crowd Funding', color = currentColor[3])
plt.legend(title = 'Funding Type')
plt.grid()
plt.xlabel('Years')
plt.ylabel('Total Funding Amount(in Million $)')

plt.subplot(1, 3, 3)
plt.plot(debtYears, [(amount * 1000) for amount in debtAmount], label = 'Debt Funding', color = currentColor[2])
plt.plot(crowdYears, [(amount * 1000) for amount in crowdAmount], label = 'Crowd Funding', color = currentColor[3])
plt.legend(title = 'Funding Type')
plt.grid()
plt.xlabel('Years')
plt.ylabel('Total Funding Amount(in Million $)')

plt.suptitle('Trend of different funding types over years 2015 - 2020')

plt.show()


# ## 10. Funding status of top 5 most amount funded over year 2015 - 2020 :

# In[76]:


startupToTotalAmount = Counter()
for index in range(dataset.shape[0]) :
    startupName = dataset.loc[index].StartupName
    amount = dataset.loc[index].Amount
    startupToTotalAmount[startupName] += amount

relevantData = startupToTotalAmount.most_common()[: 5]
top_5_startups = [content[0] for content in relevantData]

startup_1_name = top_5_startups[0]
startup_1_data = {}
startup_2_name = top_5_startups[1]
startup_2_data = {}
startup_3_name = top_5_startups[2]
startup_3_data = {}
startup_4_name = top_5_startups[3]
startup_4_data = {}
startup_5_name = top_5_startups[4]
startup_5_data = {}

years = sorted(dataset.Date.dt.year.unique())
for year in years :
    startup_1_data[year] = 0
    startup_2_data[year] = 0
    startup_3_data[year] = 0
    startup_4_data[year] = 0
    startup_5_data[year] = 0

for index in range(dataset.shape[0]) :
    startupName = dataset.loc[index].StartupName
    year = dataset.loc[index].Date.year
    amount = dataset.loc[index].Amount
    if startupName == startup_1_name :
        startup_1_data[year] += amount
    elif startupName == startup_2_name :
        startup_2_data[year] += amount
    elif startupName == startup_3_name :
        startup_3_data[year] += amount
    elif startupName == startup_4_name :
        startup_4_data[year] += amount
    elif startupName == startup_5_name :
        startup_5_data[year] += amount

startup_1_yearwiseAmount = []
startup_2_yearwiseAmount = []
startup_3_yearwiseAmount = []
startup_4_yearwiseAmount = []
startup_5_yearwiseAmount = []

for year in years :
    startup_1_yearwiseAmount.append(startup_1_data[year] / (10 ** 9))
    startup_2_yearwiseAmount.append(startup_2_data[year] / (10 ** 9))
    startup_3_yearwiseAmount.append(startup_3_data[year] / (10 ** 9))
    startup_4_yearwiseAmount.append(startup_4_data[year] / (10 ** 9))
    startup_5_yearwiseAmount.append(startup_5_data[year] / (10 ** 9))


# In[77]:


currentColors = random.sample(colours, 5)

plt.figure(figsize = (20, 10))

plt.plot(years, startup_1_yearwiseAmount, label = startup_1_name, color = currentColors[0])
plt.plot(years, startup_2_yearwiseAmount, label = startup_2_name, color = currentColors[1])
plt.plot(years, startup_3_yearwiseAmount, label = startup_3_name, color = currentColors[2])
plt.plot(years, startup_4_yearwiseAmount, label = startup_4_name, color = currentColors[3])
plt.plot(years, startup_5_yearwiseAmount, label = startup_5_name, color = currentColors[4])

for index in range(1, len(years) - 1) :
    if startup_1_yearwiseAmount[index] > startup_1_yearwiseAmount[index - 1] and startup_1_yearwiseAmount[index] > startup_1_yearwiseAmount[index + 1] :
        plt.text(years[index], startup_1_yearwiseAmount[index], startup_1_name + '\n(' + str(round(startup_1_yearwiseAmount[index], 2)) + ')')
    if startup_2_yearwiseAmount[index] > startup_2_yearwiseAmount[index - 1] and startup_2_yearwiseAmount[index] > startup_2_yearwiseAmount[index + 1] :
        plt.text(years[index], startup_2_yearwiseAmount[index], startup_2_name + '\n(' + str(round(startup_2_yearwiseAmount[index], 2)) + ')')
    if startup_3_yearwiseAmount[index] > startup_3_yearwiseAmount[index - 1] and startup_3_yearwiseAmount[index] > startup_3_yearwiseAmount[index + 1] :
        plt.text(years[index], startup_3_yearwiseAmount[index], startup_3_name + '\n(' + str(round(startup_3_yearwiseAmount[index], 2)) + ')')
    if startup_4_yearwiseAmount[index] > startup_4_yearwiseAmount[index - 1] and startup_4_yearwiseAmount[index] > startup_4_yearwiseAmount[index + 1] :
        plt.text(years[index], startup_4_yearwiseAmount[index], startup_4_name + '\n(' + str(round(startup_4_yearwiseAmount[index], 2)) + ')')
    if startup_5_yearwiseAmount[index] > startup_5_yearwiseAmount[index - 1] and startup_5_yearwiseAmount[index] > startup_5_yearwiseAmount[index + 1] :
        plt.text(years[index], startup_5_yearwiseAmount[index], startup_5_name + '\n(' + str(round(startup_5_yearwiseAmount[index], 2)) + ')')

plt.xlabel('Startup Year')

plt.ylabel('Funded Amount(in Billion $)')
plt.title('Trend of the top 5 most funded startups')

plt.legend(title = 'Startup Names :')
plt.grid()

plt.show()

