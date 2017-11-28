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


my_key  ='???????????????'


filename = './ville.csv'
df = pd.read_csv(filename, sep=',', index_col=0)


#print(df)

origins = [df.iloc[i,0] for i in range(0, 2)]
destinations = origins

print(origins)

client = gm.Client(key=my_key)

for i in origins:
    for j  in destinations:
        distance_matrix = gm.client.distance_matrix(client, i, j)



print(distance_matrix)

print(type(distance_matrix), len(distance_matrix))

#df.loc[len(df)] = infos
#distance_matrix.to_csv('./distance_matrix.csv', index=False)



#def distance_matrix(client, origins, destinations,
#                    mode=None, language=None, avoid=None, units=None,
#                    departure_time=None, arrival_time=None, transit_mode=None,
#                    transit_routing_preference=None, traffic_model=None)
