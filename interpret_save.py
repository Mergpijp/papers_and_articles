# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 23:33:02 2019

@author: Emmanuel
"""

from pandas_ods_reader import read_ods
import pandas as pd

papers = 'papers.ods'
articles = 'articles.ods'

# load a file that does not contain a header row columns 
papers_df = read_ods(papers, 1, headers=False, columns=['paper', 'number', 'year', 'place'])
articles_df = read_ods(articles, 1, headers=False, columns=['id', 'paper', 'year_number', 'description'])
#convert to year_number
papers_df['year_number'] = [str(int(year)) + ':' + str(int(number)) for (year, number) in zip(papers_df['year'], papers_df['number'])]
#Cleaning up old columns:
del papers_df['year']
del papers_df['number']

Agrarisch_nieuwsblad = ['Agr Nieuwsb', 'Agr NB', 'AN']
Hollandsch_nieuwsblad = ['Hollands nieuws', 'HNB', 'HN']
Bataafsche_staats__courant = ['Bataafse staatscourant', 'Bataafsche Staatscourant', 'BS']
Dagelijksche_beurscourant = ['Dag beurscourant', 'Dagelijkse Beurskrant']
places = [None] * articles_df.shape[0]
#for each year and number add a place and add correct paper
for index, row in articles_df.iterrows():
    if row['paper'] in Agrarisch_nieuwsblad:
        articles_df.iloc[index, 1] = 'Agrarisch nieuwsblad'
    elif row['paper'] in Hollandsch_nieuwsblad:
        articles_df.iloc[index, 1] = 'Hollandsch nieuwsblad'
    elif row['paper'] in Bataafsche_staats__courant:
        articles_df.iloc[index, 1] = 'Bataafsche staats-courant'
    elif row['paper'] in Dagelijksche_beurscourant:
        articles_df.iloc[index, 1] = 'Dagelijksche beurscourant'    
        
    papers = papers_df.loc[papers_df['year_number'] == row['year_number']]
    paper = papers.loc[papers['paper'] == articles_df.iloc[index, 1]]
    places[index] = paper.iloc[0, 1]

articles_df['place'] = places

#first split article year_number into year and number
year_number = articles_df['year_number'].str.split(':')
#make year and number columns:
years = [element[0] for element in year_number]
#make number column:
numbers = [element[1] for element in year_number]
#add years and numbers to articles_df
articles_df['year'] = years
articles_df['number'] = numbers
#delete old year_number column:
del articles_df['year_number']

#pickle because runtime takes long.
articles_df.to_pickle('combined.pkl')

articles_df = pd.read_pickle('combined.pkl')

#take sample 500
part = articles_df.sample(500)

#dangerous overwriting
#part.to_html('partial_search.html')
