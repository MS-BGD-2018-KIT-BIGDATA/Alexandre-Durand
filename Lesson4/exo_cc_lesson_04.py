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


def getJsonFromUrl(url):
    r = requests.get(url) 
    if r.status_code == 200:
        return r.json()
    else:
        return None


## MAIN
        
medicament = 'ibuprofene'
page = 1
json = getJsonFromUrl(urlForPage(medicament, page))

page = 2
while getJsonFromUrl(urlForPage(medicament, page)) != []:
    json = json + getJsonFromUrl(urlForPage(medicament, page))
    page = page + 1


df = pd.DataFrame.from_dict(json).set_index('codeCIS')


# Pour chacun des codeCIS :
def getInfosForMed(codeCIS):
    url_medoc = 'https://open-medicaments.fr/api/v1/medicaments/' + codeCIS
    json_medoc = getJsonFromUrl(url_medoc)

    labo = json_medoc['titulaires'][0]
    amm_y = json_medoc['dateAMM'].split('-')[0]
    amm_m = json_medoc['dateAMM'].split('-')[1]
    prix = json_medoc['presentations'][0]['prix']
    
    libelle = json_medoc['presentations'][0]['libelle']
    referenceDosage = json_medoc['compositions'][0]['referenceDosage']
    
    
    # Unit used for Quantity
    if re.search("(\d+) +(\w+)", referenceDosage) != None :
        unit = re.search("(\d+) +(\w+)", referenceDosage).group(2)
    else:
        unit = referenceDosage.split(" ")[-1]
    
    # Product Quantity
    if re.search("(\d+) +"+unit, libelle) != None:
        qty_PDT = re.search("(\d+) +"+unit, libelle).group(1)
        qty_PDT = float(qty_PDT.replace(',', '.'))
    else:
        qty_PDT = 0
    
    # Reference Quantity
    if re.search("\d+", referenceDosage) != None:
        qty_REF = referenceDosage.split(" ")[0]
        if str(qty_REF).isdigit():
            qty_REF = float(qty_REF.replace(',', '.'))
        else: qty_REF = 1
    else:
        qty_REF = 1
    
    # Rapport entre les quantités PRDOUIT et la quantité de REFERENCE
    qtyPDT_vs_qtyREF = qty_PDT/qty_REF
    
    # Dosage de Référence en IBUPROFENE
    if json_medoc['compositions'][0]['substancesActives'][0]['denominationSubstance'].lower().rfind("ibuprof") != -1 :
        dosageIbu = json_medoc['compositions'][0]['substancesActives'][0]['dosageSubstance']
        if dosageIbu != "":
            qty_dosage = float(dosageIbu.split(" ")[0].replace(',', '.'))
            unit_dosage = dosageIbu.split(" ")[1]
        else:
            qty_dosage = 0 # fictif
            unit_dosage = "g" # fictif
    else:
        qty_dosage = 0 # fictif
        unit_dosage = "g" # fictif
    
    # Dosage du PRODUIT en IBUPROFENE
    if unit_dosage == "mg":
        qty_DOS_g = qty_dosage/1000
    elif unit_dosage == "g":
        qty_DOS_g = qty_dosage
    
    
    
    df.at[codeCIS, 'labo'] = labo
    df.at[codeCIS, 'amm_y'] = amm_y
    df.at[codeCIS, 'amm_m'] = amm_m
    df.at[codeCIS, 'prix'] = prix
    df.at[codeCIS, 'libelle'] = libelle
    df.at[codeCIS, 'qty_PDT'] = qty_PDT
    df.at[codeCIS, 'unit_PDT'] = unit
    df.at[codeCIS, 'qty_REF'] = qty_REF
    df.at[codeCIS, 'unit_REF'] = unit
    df.at[codeCIS, 'qty_PDT/qty_REF'] = qtyPDT_vs_qtyREF
    #df.at[codeCIS, 'dosageIbu'] = dosageIbu
    #df.at[codeCIS, 'qtyIBU_REF'] = qty_dosage
    #df.at[codeCIS, 'unit_IBU_REF'] = unit_dosage
    df.at[codeCIS, 'qtyIBU_REF_g'] = qty_DOS_g
    df.at[codeCIS, 'Equivalent IBU (g)'] = round(qtyPDT_vs_qtyREF * qty_DOS_g, 2)
    
    df.to_csv('./ibuprofene_result.csv', index=True)
    
    return


for codeCIS, denom in df.iterrows():
    getInfosForMed(codeCIS)

print(df)
df.to_csv('./ibuprofene_result.csv', index=True)