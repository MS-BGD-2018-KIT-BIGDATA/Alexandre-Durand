#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 13:31:31 2017

@author: adurand
"""

# Distance en voiture Ville à ville des 100 plus grandes villes de france
# en utilsant API Google


import pandas as pd
import googlemaps as gm

# /!\ INSERT YOUR OWN KEY /!\
# =========================== 
my_key  =''

# On utilise comme base un fichier listant les 100 plus grandes villes
filename = './ville.csv'
df_ville = pd.read_csv(filename, sep=',', index_col=0)


origins = [df_ville.iloc[i,0] for i in range(0, 10)]
destinations = origins
print(origins)


client = gm.Client(key=my_key)
distance_matrix = gm.client.distance_matrix(client, origins, destinations,
                                            mode='driving')

df = pd.DataFrame(index=origins, columns=origins)

# Here, we print it as a Cartesian product.
for isrc, src in enumerate(distance_matrix['origin_addresses']):
    for idst, dst in enumerate(distance_matrix['destination_addresses']):
        if isrc <= idst:
            row = distance_matrix['rows'][isrc]
            cell = row['elements'][idst]
            if cell['status'] == 'OK':
                df.at[origins[isrc], origins[idst]] = int(cell['distance']['value']/1000)
                #print('{} to {}: {}, {}.'.format(src, dst, cell['distance']['text'], cell['duration']['text']))
            else:
                print('{} to {}: status = {}'.format(src, dst, cell['status']))


df.fillna(value='-', inplace=True)
df.to_csv('./distance_km_matrix.csv', index=True)
print(df)


# distance_matrix['rows'][i] ==> information pour la ie origine vers toutes les destinations
  # distance_matrix['rows'][i]['elements'][j] ==> ie origine vers la je destination

#def distance_matrix(client, origins, destinations,
#                    mode=None, language=None, avoid=None, units=None,
#                    departure_time=None, arrival_time=None, transit_mode=None,
#                    transit_routing_preference=None, traffic_model=None)
