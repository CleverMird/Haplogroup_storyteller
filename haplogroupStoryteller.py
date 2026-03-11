#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 09:08:13 2026

@author: inf-48-2025
"""

import pandas as pd
from collections import Counter

mainDF = pd.read_excel('/home/inf-48-2025/BINP29/PopGenProj/Resources/Data/AADR_54.1/AADR_Annotations_2025.xlsx')

df = mainDF[['Genetic ID', 'Date mean in BP in years before 1950 CE [OxCal mu for a direct radiocarbon date, and average of range for a contextual date]', 'Political Entity',
            'mtDNA haplogroup if >2x or published']].copy()
# %%
#read our list of old and new DNA from the input files

with open("/home/inf-48-2025/BINP29/PopGenProj/lineageDates.txt") as mtClock:
    lines = mtClock.readlines()
    ancestDates = {}
    for line in lines:
        line = line.split('\t')
        ancestDates.update({line[0].strip().lower():line[1].strip()})

with open("/home/inf-48-2025/BINP29/PopGenProj/Resources/Data/AADR_54.1/Ancient_samples.txt") as oldList:
    lines = oldList.readlines()
    oldDNA = []
    for line in lines:
        line = line.lower().split()
        oldDNA.append(line[1])
    
with open("/home/inf-48-2025/BINP29/PopGenProj/Resources/Data/AADR_54.1/Modern_samples.txt") as newList:
    lines = newList.readlines()
    newDNA = []
    for line in lines:
        line = line.lower().split()
        newDNA.append(line[1])
        
# %%
#set user group and search out mtDNA clock info 
userGroup = 'u2'

#possible truncations in case full data isn't availible
userTrunc = userGroup
upTheTree = False

mainLineage = userGroup[0]

firstSplit = ancestDates.get(mainLineage, "ERROR")

latestSplit = ancestDates.get(userTrunc, "ERROR")

#if no data, go back until we find data
if firstSplit == "ERROR" or latestSplit == "ERROR":
    while len(userTrunc) >= 1 and latestSplit == "ERROR":
        userTrunc = userTrunc[:-1]
        latestSplit = ancestDates.get(userTrunc, "ERROR")
    if len(userTrunc) == 1 and latestSplit == "ERROR":
        print("This lineage is not in our database, please check spelling and try again.")
        quit()
    elif len(userTrunc) == 1:
        upTheTree = True

#print important info
firstSplit = int(firstSplit)
latestSplit = int(latestSplit)
print(f"The {mainLineage} lineage is estimated to have diverged from the rest of humanity around {firstSplit-2000} BCE")
if upTheTree == True:
    print("Our database has no information on dates for futher divergances of the line.")
else:    
    print(f"The most recent common ancestor for the {userTrunc} maternal line is estimated to have lived around {latestSplit-2000} BCE")
        
# %%
#separate out modern and ancient DNA from AADR database
modernPeople = []
oldPeople = []

for index, item in enumerate(df['Genetic ID'], start=0):
    item = str(item).strip().lower()
    if item in newDNA:
        modernPeople.append(index)
    if item in oldDNA:
        oldPeople.append(index)
    else:
        pass

# %%
#compile list of possible ancestors and relatives
ancestors = []
relatives = []

for oldPerson in oldPeople:
    oldHapGroup = str(df.at[oldPerson, 'mtDNA haplogroup if >2x or published']).lower()
    if oldHapGroup[0] == mainLineage:
        ancestors.append(oldPerson)

for modernPerson in modernPeople:
    newHapGroup = str(df.at[modernPerson, 'mtDNA haplogroup if >2x or published']).lower()
    if newHapGroup[0] == mainLineage:
        relatives.append(modernPerson)

# %%
#whittle down possible ancestors list 

for index, letter in enumerate(str(userGroup), start=0):
    newAncestors = []
    for ancestor in ancestors:
        ancestorGroup = df.at[ancestor, 'mtDNA haplogroup if >2x or published']
        if len(ancestorGroup) <= index or len(ancestorGroup) > index and ancestorGroup[index].lower() == letter:
                newAncestors.append(ancestor)
    if len(newAncestors) != 0:
        ancestors = newAncestors
    else:
        break
newAncestors = []    
for ancestor in ancestors:
    ancestorGroup = str(df.at[ancestor, 'mtDNA haplogroup if >2x or published']).strip()
    if len(ancestorGroup) <= len(userGroup):
        newAncestors.append(ancestor)
ancestors = newAncestors

# %%
#now we have only the ancient DNA that is the same group as our user, or from the same tree and not differentiated further and we 
#can look for the oldest and newest members of this group

oldestAncestor = ''
oldestAncestorDate = 0
oldestAncestorHapGroup = 0

newestAncestor = ''
newestAncestorDate = 1000000000
newestAncestorHapGroup = 0

for ancestor in ancestors: 
    if df.iat[ancestor, 1] > oldestAncestorDate:
        oldestAncestor = ancestor
        oldestAncestorDate = df.iat[ancestor, 1]
        oldestAncestorHapGroup = df.at[ancestor,'mtDNA haplogroup if >2x or published']
    if df.iat[ancestor, 1] < newestAncestorDate:
        newestAncestor = ancestor
        newestAncestorDate = df.iat[ancestor, 1]
        newestAncestorHapGroup = df.at[ancestor,'mtDNA haplogroup if >2x or published'] 
        
if oldestAncestorDate > 1950:
    print(f"The oldest known member of the {userGroup} line lived around {(1950-oldestAncestorDate)*-1} BCE in modern-day {df.iat[oldestAncestor, 2]}")
else:
    print(f"The oldest known member of the {userGroup} line lived around {1950-oldestAncestorDate} CE in modern-day {df.iat[oldestAncestor, 2]}")
  
    
if newestAncestorDate > 1950:
    print(f"The most recent member of the {userGroup} line in the AADR database lived around {(1950-newestAncestorDate)*-1} BCE in modern-day {df.iat[newestAncestor, 2]}")
else:
    print(f"The most recent member of the {userGroup} line in the AADR database lived around {1950-newestAncestorDate} CE in modern-day {df.iat[newestAncestor, 2]}")

# %%
#whittle down possible relatives list 

# for index, letter in enumerate(str(userGroup), start=0):
#     newRelatives = []
#     for relative in relatives:
#         relativeGroup = str(df.at[relative, 'mtDNA haplogroup if >2x or published'])
#         if len(relativeGroup) <= index or len(relativeGroup) > index and relativeGroup[index].lower() == letter:
#                 newRelatives.append(relative)
#     if len(newRelatives) != 0:
#         relatives = newRelatives
#     else:
#         break
# newRelatives = []    
# for relative in relatives:
#     relativeGroup = str(df.at[relative, 'mtDNA haplogroup if >2x or published']).strip()
#     if len(relativeGroup) <= len(userGroup):
#         newRelatives.append(relative)
# relatives = newRelatives

# %%
#find info on relatives
relativeOrigins = []

for relative in relatives: 
    relativeOrigins.append(str(df.iat[relative, 2]).strip())
    
groupCounts = Counter(relativeOrigins)
    
if len(relativeOrigins) == 0:
    print(f"No other modern members of the {mainLineage.upper()} lineage have submitted their DNA to AADR")
    
else: 
    print(f"{len(relatives)} other modern members of the {mainLineage.upper()} lineage have submitted their DNA to AADR, tracing their origins to the following countries:")
    for country in groupCounts.keys():
        print(f"{country}: {groupCounts[country]}")
    


