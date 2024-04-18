##### packages
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

plt.figure(figsize=(8, 8))
#### Fonctions

def get_base_graph(nb_var: int):  # -> nx.Graph
    G = nx.Graph()
    G.add_edges_from([('V', 'F'), ('N', 'F'), ('V', 'N')])
    for i in range(1, nb_var+1):
        G.add_edges_from([(str(i), str(-i)), (str(i), 'N'), (str(-i), 'N')])
    return G
    

def add_or2(G, n_cl: int, en1: str, en2: str) -> str:
    L = 'L'+n1+str(n_cl)
    R = 'R'+n2+str(n_cl)
    out = n1+n2+str(n_cl) 
    G.add_edges_from([(en1, L), (en2, R), (L, R), (out, L), (out, R)])
    return out

def add_or(G, en1: str, en2: str, en3: str) -> str:
    
    out = add_or2(G, add_or2(G, en1, en2), en3)
    G.add_edges_from([(out, 'F'), (out, 'N')])
    

#### Colors

def get_dict_link(dict_int: dict) -> dict:
    d = {}
    int_F = dict_int['F']; int_V = dict_int['V']; int_N = dict_int['N']
    d[int_F] = 'red'; d[int_V] = 'green'; d[int_N] = 'blue'
    for i in range(4):
        if i not in [int_F, int_V, int_N]:
            d[i] = 'grey'
    return d
    
def get_list_colors(dict_int: dict, dict_link: dict) -> list:
    return [dict_link[dict_int[name]] for name in G.nodes()]


#### Tests

nb_var = 3
G = get_base_graph(nb_var)
add_or3(G, '1', '2', '3')
add_or3(G, '1', '2', '-3')
d = nx.greedy_color(G, 'DSATUR')

#print(d)

# Draw graph
nx.draw_networkx(G,
                node_color = get_list_colors(d, get_dict_link(d)), 
                with_labels=True,
                font_color = 'black')
#ShowFigure
plt.show()