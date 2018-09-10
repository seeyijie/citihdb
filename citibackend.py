
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import re

sort = ""
# In[2]:


# Group 1
# Core Central Districts => &selectedDistrictIds=1,2,4,6,7,9,10,11
"""
D1 - Temasek Blvd, Raffles Link
D2 - Anson, Tanjong Pagar
D4 - Telok Blangah, Harbourfront
D6 - High Street, Beach Road
D7 - Middle Road, Golden Mile
D9 - Orchard, Cairnhill, River Valley
D10 - Bukit Timah, Holland Rd, Tanglin
D11 - Watten Estate, Novena, Thomson
"""
# Group 2
# Rest of Central Region => &selectedDistrictIds=2,3,7,8,12,13,14,15
"""
D2 - Anson, Tanjong Pagar
D3 - Queenstown, Tiong Bahru
D7 - Middle Road, Golden Mile
D8 - Little India
D12 - Balestier, Toa Payoh, Serangoon
D13 - Macpherson, Braddell
D14 - Geylang, Eunos
D15 - Katong, Joo Chiat, Amber Road
"""
# Group 3
# Outside Central Region => &selectedDistrictIds=5,16,17,18,19,20,21,22,23,24,25,26,27,28
"""
D5 - Pasir Panjang, Clementi
D16 - Bedok, Upper East Coast
D17 - Loyang, Changi
D18 - Tampines, Pasir Ris
D19 - Serangoon, Hougang, Punggol
D20 - Bishan, Ang Mo Kio
D21 - Upper Bukit Timah, Ulu Pandan
D22 - Jurong
D23 - Bukit Panjang, Choa Chu Kang
D24 - Lim Chu Kang, Tengah
D25 - Kranji, Woodgrove
D26 - Upper Thomson, Springleaf
D27 - Yishun, Sembawang
D28 - Seletar
"""
def districtFilter(groupCode):
    assert type(groupCode) == int and groupCode >= 1 and groupCode <=3, 'Group Code must be an 1, 2 or 3'
    if groupCode == 1:
        return('&selectedDistrictIds=1,2,4,6,7,9,10,11,2,7')
    # need to add in 2,7 in front even though its a duplicate
    if groupCode == 2:
        return('&selectedDistrictIds=2,7,2,3,7,8,12,13,14,15')
    if groupCode == 3:
        return('&selectedDistrictIds=5,16,17,18,19,20,21,22,23,24,25,26,27,28')

districtFilter(1)

def districtPicker(districtCode):
    return ('&selectedDistrictIds={}'.format(districtCode))

districtPicker(12)


# In[3]:


# property type:
#hdb?cdResearchSubTypes=16,17,1,2,3,4,18,19 => 1 room, 2 room, 3 room, 4 room, 5 room, executive, hudc, hdb multi-gen


def hdbTypeFilter(type_):
    if type_ == 'hdb-1':
        return('hdb?cdResearchSubTypes=16')
    if type_ == 'hdb-2':
        return('hdb?cdResearchSubTypes=17')
    if type_ == 'hdb-3':
        return('hdb?cdResearchSubTypes=1')
    if type_ == 'hdb-4':
        return('hdb?cdResearchSubTypes=2')
    if type_ == 'hdb-5':
        return('hdb?cdResearchSubTypes=3')
    if type_ == 'hdb-exec':
        return('hdb?cdResearchSubTypes=4')
    if type_ == 'hdb-hudc':
        return('hdb?cdResearchSubTypes=18')
    if type_ == 'hdb-multi':
        return('hdb?cdResearchSubTypes=19')

hdbTypeFilter('hdb-1')


# In[4]:


'''
hdb-1 = 1 Room HDB Flat (16)
hdb-2 = 2 Room HDB Flat (17)
hdb-3 = 3 Room HDB Flat (1)
hdb-4 = 4 Room HDB Flat (2)
hdb-5 = 5 Room HDB Flat (3)
hdb-exec = HDB Executive (4)
hdb-hudc = HUDC (18)
hdb-multi = HDB Multi-Gen (19)
'''
'''
Test Case 1:


urlGenerator(addPropertyTypeFilter('hdb-1','hdb-3', 'hdb-4'), budget(500000,1000000))
What is your budget?


What kind of property do you want?
addPropertyTypeFilter('hdb-1','condo','hdb-4')
'''

def budget(minimum,maximum):
    return[minimum,maximum]

def addPropertyTypeFilter(*args):
    #Returns a list of property filter to be applied
    return list(args)

def urlGenerator(addPropertyTypeFilter_, budget, districtFilter='',sort=''):
    # get the total number of fields for property and generate the respective url query points
    #limitation is hdb must come first followed by condo/landed
    hdbCounter = 0
    newPropertyQueryList=[]
    otherPropertyCounter = 0
    #search for hdb and if it exist, change it to the mapped part of the query string and store it in a new list.
    for property_ in addPropertyTypeFilter_:
        if property_[:3:] == 'hdb':
            if hdbCounter >= 1:
                newPropertyQueryList.append(','+hdbTypeFilter(property_)[:-2:-1])
                hdbCounter+=1
            elif hdbCounter == 0 and otherPropertyCounter==0:
                hdbCounter+=1
                newPropertyQueryList.append(hdbTypeFilter(property_))

        #only possibility is condo or landed
        elif len(addPropertyTypeFilter_)==1:
            newPropertyQueryList.append(property_)

        elif (property_ == 'landed' or property_ == 'condo') and otherPropertyCounter == 0 and hdbCounter==0:
            newPropertyQueryList.append(property_)
            otherPropertyCounter+=1

        else:
            newPropertyQueryList.append('&'+property_)


    propertyTypeString = ''
    for i in newPropertyQueryList:
        propertyTypeString += i

    #set sorting options for baseURL
    if sort == "None":
        sort = ""
    elif sort == "addr": #sort by asc address
        sort = "&orderCriteria=addressAsc"
    elif sort == "price":
        sort = "&orderCriteria=priceAsc"
    elif sort == "size":
        sort = "&orderCriteria=sizeAsc"
    elif sort == "psf":
        sort = "&orderCriteria=psfAsc"

    baseUrl = "https://www.srx.com.sg/search/sale/{}&minSalePrice={}&maxSalePrice={}{}&view=table{}".format(
        propertyTypeString,budget[0],budget[1],districtFilter,sort)
    print(baseUrl)
    return(baseUrl)

# urlGenerator(addPropertyTypeFilter('hdb-1','hdb-3', 'hdb-4'), budget(500000,1000000))
# urlGenerator(addPropertyTypeFilter('hdb-1'), budget(500000,1000000))

# urlGenerator(addPropertyTypeFilter('condo'), budget(500000,1000000))
# urlGenerator(addPropertyTypeFilter('landed'), budget(500000,1000000))
# urlGenerator(addPropertyTypeFilter('hdb-1','hdb-3', 'hdb-exec'), budget(250000,500000), districtFilter(2))
# urlGenerator(addPropertyTypeFilter('hdb-1','hdb-3', 'hdb-exec'), budget(600000,700000), districtFilter(2))
# https://www.srx.com.sg/search/sale/hdb?cdResearchSubTypes=16,1,4?minSalePrice=600000&maxSalePrice=700000&selectedDistrictIds=2,3,7,8,12,13,14,15&view=table
# https://www.srx.com.sg/search/sale/hdb?cdResearchSubTypes=16,1,4&minSalePrice=600000&maxSalePrice=700000&selectedDistrictIds=2,3,7,8,12,13,14,15
# https://www.srx.com.sg/search/sale/hdb?cdResearchSubTypes=16,1,4&minSalePrice=600000&maxSalePrice=700000&selectedDistrictIds=2,7,2,3,7,8,12,13,14,15
# https://www.srx.com.sg/search/sale/hdb?cdResearchSubTypes=16,1,4&maxSalePrice=1000000


# In[5]:


def getListingLinks(url):
    response = requests.get(url)
    print(response)
    soup = BeautifulSoup(response.content, 'html.parser')
    pageNumberElement = soup.find_all(class_='has-properties')
    maxPageNumber = int(pageNumberElement[0].find_all('strong')[1].text)

    baseUrl = 'https://www.srx.com.sg'
    urlPage = []
    urlListing = []

    #cap it at 2 pages for now.
    if maxPageNumber > 1:
        for i in range(1,2+1):
            print(str(i) + 'th iteration already!')
            urlPage.append((url+'&page={}'.format(i)))
#             print(urlPage)

            response = requests.get(urlPage[i-1])
            soup = BeautifulSoup(response.content, 'html.parser')
            listingLink = soup.find_all(class_='listing-table-view-id')

            for i in listingLink:
                info = str(i.find_all('a')[0])
                cleanInfo = re.findall(r'"(.*?)"', info)[0]
#                 print(cleanInfo)
                urlListing.append((baseUrl+cleanInfo))

#             print(len(urlListing))
        return(urlListing)

    else:
        for i in range(1,2):
            print(str(i) + 'th iteration already!')
            urlPage.append((url+'&page={}'.format(i)))
#             print(urlPage)
#             print(urlListing)


            response = requests.get(urlPage[i-1])
            soup = BeautifulSoup(response.content, 'html.parser')
            listingLink = soup.find_all(class_='listing-table-view-id')

            for i in listingLink:
                info = str(i.find_all('a')[0])
                cleanInfo = re.findall(r'"(.*?)"', info)[0]
#                 print(cleanInfo)
                urlListing.append((baseUrl+cleanInfo))

            print(len(urlListing))
        return(urlListing)

# getListingLinks('https://www.srx.com.sg/search/sale/condo?minSalePrice=500000&maxSalePrice=1000000&view=table')


# In[6]:


def getOneListingDetails(oneUrl):
    listdict = {}
    response = requests.get(oneUrl)
    soup = BeautifulSoup(response.content, 'html.parser')
    searchKey = soup.find_all(class_='listing-about-main-key')
    searchValue = soup.find_all(class_='listing-about-main-value')
    for i,j in enumerate(searchKey):
        listdict[j.text]=searchValue[i].text.replace('\n','').replace('\t','').replace('\r','')
    listdict['Url'] = oneUrl
    return listdict


# In[7]:


def getAllListingDetails(listOfUrl):
    library = {}
    print(len(listOfUrl))
    for i,j in enumerate(listOfUrl):
        library[i]=getOneListingDetails(j)
        print(str((i/len(listOfUrl))*100)+'% completed!')
    return library


# In[8]:


# computation = urlGenerator(addPropertyTypeFilter('hdb-3', 'hdb-5'), budget(300000,500000))


# In[9]:


# getAllListingDetails(getListingLinks(computation))


# In[10]:


# computation2 = urlGenerator(addPropertyTypeFilter('condo'), budget(666666,777777), districtFilter(1))


# In[22]:


# getAllListingDetails(getListingLinks(computation2))


# In[69]:


# computation3 = urlGenerator(addPropertyTypeFilter('condo'), budget(600000,700000), districtFilter(1))


# In[70]:


# getAllListingDetails(getListingLinks(computation3))


# In[73]:


# computation4 = urlGenerator(addPropertyTypeFilter('condo'), budget(600000,700000), districtPicker(2))
# getAllListingDetails(getListingLinks(computation4))
