#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 17:32:20 2017
@author: adurand
"""
import requests
from bs4 import BeautifulSoup


# url type = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=2013'

def getDataFor(year, dataType, column):
    if (int(year) < 2010 or int(year) > 2015):
        print('Année invalide.' + '\n' + 'Veuillez rentrer une année comprise entre 2010 et 2015')
        return None
    if (dataType != 'EurosParHab' and dataType != 'MoyenneStrate'):
        print("DataType Invalide. Entrer 'EurosParHab' ou 'MoyenneStrate'")
        return None
    column = column.upper()
    if column not in ['A', 'B', 'C', 'D']:
        print('Entrée invalide. Veuillez entrer une lettre entre A et D')
        return None
    else:
        soup = getSoupFromYear(year)
        if soup:
            return soup.find_all('td', class_='montantpetit G')[getIndexFor(dataType, column)].text.strip()


def getSoupFromYear(my_year):
    url = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?' \
              'icom=056&dep=075&type=BPS&param=5&exercice=' + str(my_year)
    res = requests.get(url)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        return soup
    else:
        return None


def getIndexFor(dataType, column):
    if dataType == 'EurosParHab':
        idxDict = {'A':1, 'B':4, 'C':10, 'D':13}
        return idxDict[column]
    if dataType == 'MoyenneStrate':
        idxDict = {'A':2, 'B':5, 'C':11, 'D':14}
        return idxDict[column]



# Print all Datas
#------------------

years = range(2010, 2016)
dataType = ['EurosParHab', 'MoyenneStrate']
colName = {'A':'TOTAL DES PRODUITS DE FONCTIONNEMENT', \
           'B':'TOTAL DES CHARGES DE FONCTIONNEMENT', \
           'C':'TOTAL DES RESSOURCES D\'INVESTISSEMENT', \
           'D':'TOTAL DES EMPLOIS D\'INVESTISSEMENT'}

for year in years:
    print('\n' * 2)
    print('Année :', year)
    print('================')
    for dt in dataType:
        print(dt)
        print('--------------')
        for col in colName:
            print(colName[col], ' : ', getDataFor(year, dt, col))


