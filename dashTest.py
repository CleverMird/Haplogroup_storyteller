#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 14:46:29 2026

@author: inf-48-2025
"""

from dash import Dash, html, dcc


app = Dash()

from igraph import Graph
import plotly.graph_objects as go

usergroup = "U2c"
layers = len(usergroup)

nr_vertices = (len(usergroup)+(len(usergroup)-1))
v_label = list(map(str, range(nr_vertices)))
G = Graph.Tree(nr_vertices, 2) # 2 stands for children number

position = []
for k in range(0,layers):
    position.append((((k - (layers/2))),((layers-k))))
for k in range(0,layers):
    if k > 0:
       position.append((((k - (layers/2) + 0.5)),((layers-k+1)))) 

M = layers

E = [] 
for i in range(0,layers-1):
    E.append((i,i+1))
for i in range(0,layers):    
    if i > 0:
        E.append((i+layers-1,i))

L = len(position)
Xn = [position[k][0] for k in range(L)]
Yn = [2*M-position[k][1] for k in range(L)]
Xe = []
Ye = []
for edge in E:
    Xe+=[position[edge[0]][0],position[edge[1]][0], None]
    Ye+=[2*M-position[edge[0]][1],2*M-position[edge[1]][1], None]


fig = go.Figure()
fig.add_trace(go.Scatter(x=Xe,
                   y=Ye,
                   mode='lines',
                   line=dict(color='rgb(210,210,210)', width=1),
                   hoverinfo='none'
                   ))
fig.add_trace(go.Scatter(x=Xn,
                  y=Yn,
                  mode='markers',
                  name='bla',
                  marker=dict(symbol='circle-dot',
                                size=18,
                                color='#6175c1',    #'#DB4551',
                                line=dict(color='rgb(50,50,50)', width=1)
                                ),
                  opacity=0.8
                  ))

axis = dict(showline=False, # hide axis line, grid, ticklabels and  title
            zeroline=False,
            showgrid=False,
            showticklabels=False,
            )

fig.update_layout(title= f'The lineage of {usergroup}',
              font_size=12,
              showlegend=False,
              xaxis=axis,
              yaxis=axis,
              margin=dict(l=40, r=40, b=85, t=100),
              hovermode='closest',
              plot_bgcolor='rgb(248,248,248)'
              )

colors = {
    'background': '#ABCDD9',
    'text': '#F7FCFF'
}
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(children='Your Haplogroup Story',
            style={
            'textAlign': 'center',
            'color': colors['text']
        }),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run(debug=True)