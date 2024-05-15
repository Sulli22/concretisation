from pycsp3 import *
import networkx as nx
import matplotlib.pyplot as plt 

G = nx.gnm_random_graph(100,150)

x  = VarArray(size = [1,len(G)], dom = range(3))
dict_neighbor = {}

for i in G:
   A = []
   for voisin in G[i]:
       A.append(voisin)
   dict_neighbor[i] = A

satisfy(
    x[0][i] != x[0][j] for i in G for j in dict_neighbor[i] 
)

if solve() is SAT:
    list_color = values(x[0])

nx.draw(G,with_labels = True, node_color=list_color)
plt.show()

