#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 13:31:58 2017

@author: adurand
"""
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd



def urlForPage(medoc, page):
    return 'https://open-medicaments.fr/api/v1/medicaments?query=' \
        + medoc + '&page=' + str(page)


def getJsonForUrlForPage(url):
    r = requests.get(url) 
    if r.status_code == 200:
        return r.json()
    else:
        return None

## MAIN
        
medicament = 'ibuprofene'
page = 1
json = getJsonForUrlForPage(urlForPage(medicament, page))

#page = 2
#while getJsonForUrlForPage(urlForPage(medicament, page)) != []:
#    json = json + getJsonForUrlForPage(urlForPage(medicament, page))
#    page = page + 1

df = pd.DataFrame.from_dict(json).set_index('codeCIS')
print(df)


# Pour chacun des codeCIS :
codeCIS = '64565560'
url_medoc1 = 'https://open-medicaments.fr/api/v1/medicaments/' + codeCIS
json_medoc1 = getJsonForUrlForPage(url_medoc1)

titulaire = json_medoc1['titulaires'][0]
compo = json_medoc1['compositions'][0]['referenceDosage']
amm = json_medoc1['dateAMM']
print(titulaire)
print(compo)
print(amm)
