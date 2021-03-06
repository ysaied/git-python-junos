#!/usr/bin/python

# libraries
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Build a dataframe with 4 connections
df = pd.DataFrame( 
   { 
   'from':['A', 'A', 'A','A', 'B', 'B', 'C', 'D'], 
   'to':['B', 'C', 'D','E', 'D', 'C', 'E', 'E']
   }
)

# Build your graph
G=nx.from_pandas_edgelist(df, 'from', 'to')


# Plot it
nx.draw(G, with_labels=True)
plt.show()

