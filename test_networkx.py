import networkx as nx
import matplotlib.pyplot as plt

adjacency_dict = {0: (1, 2), 1: (0, 2), 2: (0, 1)} #, 3 : (2, 4), 4 : (2, 3)

G = nx.Graph(adjacency_dict)

nodes_colors_dict = {1: 'green', 2: 'blue', 0: 'red'}

def get_colors_from_dict(d : dict) -> list :
    L = ['' for i in range(len(d))]
    for couple in list(d.items()):
        L[couple[0]] = couple[1]
    return L

colors = get_colors_from_dict(nodes_colors_dict)

nx.draw(G, with_labels=True, node_color = colors)
plt.show()