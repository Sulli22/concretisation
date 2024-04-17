##### packages
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

plt.figure(figsize=(8, 8))

##### Fonctions

#### A OR B

def get_or2_graph():
    adjacency_dict = {  0: (1, 2, 9), 1: (0, 2), 2: (0, 1, 9), 3: (2, 4, 8), 4: (2, 3, 7), 
                        5: (2, 6, 7, 8), 6: (2, 5), 7: (8, 4, 5), 8: (7, 9, 3, 5), 9: (8, 0, 2)}
    return nx.Graph(adjacency_dict)

def get_relabel_or2_dict():
    return {0: "F", 1: "V", 2: "X", 3: "A", 4: "!A", 5: "B", 6: "!B", 7: "N1", 8: "N2", 9: "A∨B"}

def get_pos_or2_graph():
    return {0: np.array([3, 10]), 1: np.array([7, 10]), 2: np.array([5, 9]),
            3: np.array([2, 8]), 4: np.array([3, 8]), 5: np.array([8, 8]),
            6: np.array([7, 8]), 7: np.array([6, 6]), 8: np.array([6, 5]),
            9: np.array([5, 3])}

#### Couleurs

def get_dict_link(dict_int):
    d = {}
    int_0 = dict_int[0]; int_1 = dict_int[1]; int_2 = dict_int[2]
    d[int_0] = 'red'; d[int_1] = 'green'; d[int_2] = 'blue'
    for i in range(4):
        if i not in [int_0, int_1, int_2]:
            d[i] = 'grey'
    return d
    
def get_list_colors(dict_int, dict_link):
    return [dict_link[i[1]] for i in sorted(list(dict_int.items()))]

def satif(dict_int):
    if len(set(dict_int.values())) > 3:
        return (False, dict_int[3], dict_int[5])
    return (True, dict_int[3], dict_int[5])

##### Fonctions test 

def tuple_to_bin(c, dict_link):
    l = []
    if dict_link[c[0]] == 'red':
        b1 = False
    elif dict_link[c[0]] == 'green':
        b1 = True
    if dict_link[c[1]] == 'red':
        b2 = False
    elif dict_link[c[1]] == 'green':
        b2 = True
    l.append((b1, b2))
    return l

def test_or2():
    l = []
    for i in range(4):
        G = get_or2_graph()
        dict_int = nx.greedy_color(G, 'DSATUR')
        dict_link = get_dict_link(dict_int)
        r = satif(dict_int)
        if r[0] and (r[1], r[2]) not in l:
            l.append(tuple_to_bin((r[1], r[2]), dict_link))
        subax = plt.subplot(221+i)
        nx.draw_networkx(G, 
                        pos = get_pos_or2_graph(), 
                        font_size = 10, 
                        labels = get_relabel_or2_dict(),
                        font_color = 'white', 
                        node_color = get_list_colors(dict_int, dict_link), 
                        width = 0.5)
    print("valeurs de A et B satifaisant :", l)

test_or2()

plt.show() # affiche la figure