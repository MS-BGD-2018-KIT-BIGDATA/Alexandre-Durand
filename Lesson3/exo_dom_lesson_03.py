#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 22:59:55 2017

@author: adurand
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


### !!! INSERT YOUR USERNAME AND TOKEN FOR GITHUB API AUTHORIZATION !!!
### ===================================================================
my_username = ''
my_token = ''



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


def getJsonForCode(getCode):
    url_api = 'https://api.github.com' + getCode
    r = requests.get(url_api, auth=(my_username, my_token))
    if r.status_code == 200:
        return r.json()
    else:
        return None


def getUserInfoFromLineTabWithBS(line):
    #### INFO DE LA LIGNE DU TABLEAU
    rank = line.find('th', {'scope' : 'row'}).get_text()
    rank = int(rank[1:])  # skip the "#" of "#x" with x = rank
    
    username = line.find('a').get_text()
    
    fullname = line.find('a').nextSibling
    if fullname:
        fullname = fullname[2:-1]  # pour enlever ' (' au début du nom et ')' à la fin
    
    nb_contribs = int(line.find_all('td')[1].get_text())
    
    location = line.find_all('td')[2].get_text()
    
    return [rank, username, fullname, nb_contribs, location]


def getNbReposNbStarsforUserForPage(username, page):
    getCode = '/users/' + username + '/repos?page=' + str(page) + '&per_page=100'  # List public repo
    js = getJsonForCode(getCode)
    if js != []:
        nb_repos = len(js)
        stars_list = [repo['stargazers_count'] for repo in js]
        return [nb_repos, sum(stars_list)]
    else:
        return [0, 0]




# ----- MAIN  -----
# =================

start = time.time()

url_topContribs = 'https://gist.github.com/paulmillr/2657075'
soup = getSoupFromURL(url_topContribs)
lines_of_tab = soup.find('tbody').findChildren('tr')

df = pd.DataFrame(columns=['rank', 'username', 'fullname', 'contribs',
                           'location','nb_repo', 'total_stars'])

for line in lines_of_tab[:]:
    
    # Récupère infos du TopContributeurs via crawling de la page
    infos = getUserInfoFromLineTabWithBS(line)
    
    username = infos[1]
    
    # Récupère le nombre de repos et le nombre de Stars cumulées
    NbReposNbStars = getNbReposNbStarsforUserForPage(username, 1)
    if NbReposNbStars[0] < 100:
        infos += NbReposNbStars
    else:  # API ne renvoie les infos que sur 100 repos max par requete
        page =2  # donc tant que la requete renvoie des repos, on continue à boucler
        while getNbReposNbStarsforUserForPage(username, page)[0] != 0:
            NbReposNbStars[0] += getNbReposNbStarsforUserForPage(username, page)[0]
            NbReposNbStars[1] += getNbReposNbStarsforUserForPage(username, page)[1]
            page += 1
        infos += NbReposNbStars
    
    print(infos, '\n')
    df.loc[len(df)] = infos
    df.to_csv('./TopContribsData.csv', index=False)  # on imprime les infos après chaque ligne,
                                                     # pour ne pas tout perdre
                                                     # au cas où il y ait un problème de serveur

# CALCULATE STARS/REPOS MEAN :
# ============================
df['stars/repo_mean'] = df.apply(lambda row: 0 if row['nb_repo']==0 
                                 else round(row['total_stars']/row['nb_repo'], 2), axis=1)

df.to_csv('./TopContribsData.csv', index=False)


# On tri le tableau en fonction de la moyenne Stars/Repos
# =======================================================
df_sorted = df.sort_values('stars/repo_mean', axis=0, ascending=False)
df_sorted.to_csv('./TopContribsData_sorted.csv', index=False)

print(df_sorted.head())

end = time.time()
totaltime = end - start
print('\n' + 'Time =', round(totaltime, 2), 's')