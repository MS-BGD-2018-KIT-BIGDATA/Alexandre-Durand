#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 15:08:45 2017

@author: adurand
"""




"""
Expression Régulière :
    REGEX

(allez voir des regex cheat sheet)

- permet de tester si une donnée en entrée possède le format voulue



Importer le module Regex de Python:
    Import re



www.regex101.com
    permet de vérifier si notre regex marche
    permet d'expliquer explicitement une regex
    permet de creer une regex en fonction d'un texte en entrée'



On peut travailler les regex dans PANDAS également:
    
    email = "bonjour voici les emails de la promo: toto.durand@gmail.com,  bernard@telecom.fr, ..."
    
    import pandas as pd
    Series(regex_email.find_all(email))



Bonne pratique :
    si on n'a pas besoin de garder les Maj. ou min. du string en entrée,
    on peut tous passer en min ou maj.


"""