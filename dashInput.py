#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 14:12:54 2026

@author: inf-48-2025
"""
from dash import Dash, html, dcc, Input, Output, callback, State
import pandas as pd
from collections import Counter

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
        


app = Dash()

def haplogroup_storyteller(userGroup): 
    return_text= ''
    nl = '\n'
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
    return_text = return_text+f"The {mainLineage} lineage is estimated to have diverged from the rest of humanity around {firstSplit-2000} BCE."
    return_text = return_text + "  "
    if upTheTree == True:
        return_text= return_text+"Our database has no information on dates for futher divergances of the line."
    else:    
        return_text= return_text+f"The most recent common ancestor for the {userTrunc} maternal line is estimated to have lived around {latestSplit-2000} BCE"
    return(return_text)

app.layout = html.Div([
    html.Hr(),

    html.Label('Input 1'),
    dcc.Input(id='input1'),


    html.Button('click me', id='button'),

    html.Div(id='output')
])

@app.callback(
    Output('output', 'children'),
    [Input('button', 'n_clicks')],
    State('input1', 'value'))

def update_output_div(n_clicks, input_value):
    display_text = haplogroup_storyteller(input_value)
    return(html.Div(children=[dcc.Markdown(display_text, style={"display": 'flex','textAlign': 'center', 'vertical-align': 'top',
    'color': '#292929', 'justify-content': 'center', 'background-color':'#F0F0F0', 'padding': 10, 'flex': 1})]))




           
if __name__ == '__main__':
    app.run(debug=True)