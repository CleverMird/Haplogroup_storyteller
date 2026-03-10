#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 09:08:13 2026

@author: inf-48-2025
"""

import pandas as pd

df = pd.read_excel('/home/inf-48-2025/BINP29/PopGenProj/Resources/Data/AADR_54.1/AADR_Annotations_2025.xlsx')
# %%
#read our list of old and new DNA from the input files

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
oldPeople = []
modernPeople = []
for index, item in enumerate(df['Genetic ID'], start=0):
    item = str(item).strip().lower()
    if item in oldDNA:
        oldPeople.append(index)
    elif item in newDNA:
        modernPeople.append(index)
    else:
        pass
        
# %%

userGroup = 'r2b2'
parentGroup = userGroup[0]

ancestors = []
relatives = []

for oldPerson in oldPeople:
    oldHapGroup = str(df.at[oldPerson, 'mtDNA haplogroup if >2x or published']).lower()
    if oldHapGroup[0] == parentGroup:
        ancestors.append(oldPerson)

for modernPerson in modernPeople:
    newHapGroup = str(df.at[modernPerson, 'mtDNA haplogroup if >2x or published']).lower()
    if newHapGroup[0] == parentGroup:
        relatives.append(modernPerson)


# %%
oldestAncestor = ''
oldestAncestorDate = 0
oldestAncestorHapGroup = 0

newestAncestor = ''
newestAncestorDate = 1000000000
newestAncestorHapGroup = 0

for ancestor in ancestors: 
    if df.iat[ancestor, 8] > oldestAncestorDate:
        oldestAncestor = ancestor
        oldestAncestorDate = df.iat[ancestor, 8]
        oldestAncestorHapGroup = df.at[ancestor,'mtDNA haplogroup if >2x or published']
    if df.iat[ancestor, 8] < newestAncestorDate:
        newestAncestor = ancestor
        newestAncestorDate = df.iat[ancestor, 8]
        newestAncestorHapGroup = df.at[ancestor,'mtDNA haplogroup if >2x or published'] 
     
if oldestAncestorDate > 1950:
    print(f"The oldest known member of {userGroup}'s maternal line lived around {(1950-oldestAncestorDate)*-1} BCE in modern-day {df.iat[ancestor, 14]}")
else:
    print(f"The oldest known member of {userGroup}'s maternal line lived around {1950-oldestAncestorDate} CE in modern-day {df.iat[ancestor, 14]}")
 
if newestAncestorDate > 1950:
    print(f"The most recent known member of {userGroup}'s maternal line lived around {(1950-newestAncestorDate)*-1} BCE in modern-day {df.iat[ancestor, 14]}")
else:
    print(f"The most recent known member of {userGroup}'s maternal line lived around {1950-newestAncestorDate} CE in modern-day {df.iat[ancestor, 14]}")
