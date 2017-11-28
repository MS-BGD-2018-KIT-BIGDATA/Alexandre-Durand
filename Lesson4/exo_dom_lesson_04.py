#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


def defineURLfor(region, vendor_type, page):
    brand = "Renault"
    model = "Zoe"
    energie = "4"  # 4 = electrique
    
    url = "https://www.leboncoin.fr/voitures/offres/" \
        + region + "/" \
        + "?o=" + page \
        + "&brd=" + brand \
        + "&mdl=" + model \
        + "&fu=" + energie \
        + "&f=" + vendor_type
    return url


def getSoupFromURL(url, method='get', data={}):
  if method == 'get':
    res = requests.get(url)
  elif method == 'post':
    res = requests.post(url, data=data)
  else:
    return None

  if res.status_code == 200:
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup
  else:
    return None


def getZOEmodelfromDescr(descr):
    regexLife = "[l]{1}[i]{1}[f]{1}[e]{1}"
    regexZen = "[zZ][eE][nN]"
    regexIntens = "[Ii][Nn][Tt][Ee][Nn][Ss]"

    if re.search(regexLife, descr):
        model = "Life"
    elif re.search(regexZen, descr):
        model = "Zen"
    elif re.search(regexIntens, descr):
        model = "Intens"
    else:
        model = "Inconnu"
    return model


def getPhoneNumberfromDescr(descr):    
    regexTelNumber = '(0[1-9](?P<sep>[-. ]?)(?:\d{2}(?P=sep)){3}\d{2})'
    num = re.search(regexTelNumber, descr)
    if num :
        number = num.group(0).replace(" ", "").replace("-", "").replace(".", "")
        return number
    else :
        return "Numéro Inconnu"



def getOfferInfosFromOfferPage(url):
    
    soup = getSoupFromURL(url)
    
    
    title = soup.find('h1', {'itemprop': "name"}, class_='no-border').text.strip()
    title = title.lower()
    #print(title, type(title))
    
    descr = soup.find('p', {'itemprop': 'description'}, class_='value').text.strip()
    descr = descr.lower()
    #print(descr, type(descr), len(descr))
    model = getZOEmodelfromDescr(descr + title)
    #print(model, type(model))
    
    
    mdl_year = soup.find('span', {'itemprop': "releaseDate"}).text.strip()
    mdl_year = int(mdl_year)
    #print("YEAR =", mdl_year, type(mdl_year))
    
    km = soup.find('span', text='Kilométrage', class_='property')
    km = km.next_sibling.next_sibling.text.lower()
    km = km.replace('km', '').replace(' ', '')
    km = int(km)
    #print(" KM  =", km, type(km))
    
    price = soup.find('h2', {'itemprop': 'price'}, class_='item_price clearfix').get('content')
    price = int(price)
    #print("PRICE=", price, type(price))
    
    phone_numb = getPhoneNumberfromDescr(descr + title)
    #print(phone_numb, type(phone_numb))
    
    #date = soup.find('p', {'itemprop': 'availabilityStarts'}, class_='line line_pro').get('content')
    #print("DATE =", date, type(date))
    
    return model, mdl_year, km, price, phone_numb






## MAIN

page = '1'
regions = ["ile_de_france", "aquitaine", "provence_alpes_cote_d_azur"]
vendor_types = ["p", "c"] # p=particulier; c=professionnel


df = pd.DataFrame(columns=['ZOE_model', 'Model_Year', 'KM', 'Price',
                           'Phone_Num','Region', 'Vendor_type'])

for region in regions:
    for vendor_type in vendor_types:
        # Create url
        url_search = defineURLfor(region, vendor_type, page)
        
        # Get soup
        lbc_soup = getSoupFromURL(url_search)
        maintab = lbc_soup.find('section', class_='tabsContent block-white dontSwitch')
        tab = maintab.findChildren('li')
        
        #get info for each offer
        for line in tab[:]:
            
            url = "https:" + line.find('a')['href']
            infos = getOfferInfosFromOfferPage(url)
            
            if vendor_type == "p": full_vend_type = "particulier"
            if vendor_type == "c": full_vend_type = "professionnel"
            
            
            infos = infos + (region, full_vend_type)
            print(infos)
            df.loc[len(df)] = infos
            df.to_csv('./Result.csv', index=False)





