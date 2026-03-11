#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 12:12:30 2026

@author: inf-48-2025
"""
from plotly.offline import plot
import plotly.graph_objects as go
from igraph import Graph, EdgeSeq
# %%


nr_vertices = 25
v_label = list(map(str, range(nr_vertices)))
G = Graph.Tree(nr_vertices, 2) # 2 stands for children number
lay = G.layout('rt')

position = {k: lay[k] for k in range(nr_vertices)}
Y = [lay[k][1] for k in range(nr_vertices)]
M = max(Y)

es = EdgeSeq(G) # sequence of edges
E = [e.tuple for e in G.es] # list of edges

L = len(position)
Xn = [position[k][0] for k in range(L)]
Yn = [2*M-position[k][1] for k in range(L)]
Xe = []
Ye = []
for edge in E:
    Xe+=[position[edge[0]][0],position[edge[1]][0], None]
    Ye+=[2*M-position[edge[0]][1],2*M-position[edge[1]][1], None]

labels = v_label
# %%

# g = Graph()

# g.add_vertices(3)
# g.add_edges([(0,1), (1,2)])

# g = Graph.Tree(8, 2)
# layout = g.layout_reingold_tilford(root=[2])
# plot(g, layout=layout)



