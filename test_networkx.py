import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def creat_or2_graph():
    adjacency_dict = {0: (1, 2, 9), 1: (0, 2), 2: (0, 1, 9), 3: (2, 4, 8), 4: (2, 3, 7), 
                  5: (2, 6, 7, 8), 6: (2, 5), 7: (8, 4, 5), 8: (7, 9, 3, 5), 9: (8, 0, 2)}
    return nx.Graph(adjacency_dict)

def create_pos_or2_graph():
    return {"F": np.array([3, 10]), "V": np.array([7, 10]), "X": np.array([5, 9]),
            "A": np.array([2, 8]), "!A": np.array([2, 7]), "B": np.array([8, 8]),
            "!B": np.array([8, 7]), "N1": np.array([4, 6]), "N2": np.array([4, 5]),
            "A∨B": np.array([4, 3])}

def create_relabel_dict():
    return {0: "F", 1: "V", 2: "X", 3: "A", 4: "!A", 5: "B",
            6: "!B", 7: "N1", 8: "N2", 9: "A∨B"}

def create_dict_link(dict_int):
    d = {}
    int_0 = dict_int[0]; int_1 = dict_int[1]; int_2 = dict_int[2]
    d[int_0] = 'red'; d[int_1] = 'green'; d[int_2] = 'blue'
    for i in range(4):
        if i not in [int_0, int_1, int_2]:
            d[i] = 'grey'
    return d
    int_0 = d[0]
    if int_0 != 0:
        for key, value in d.items():
            if value == int_0:
                d[key] = 0
            elif value == 0:
                d[key] = int_0
    int_1 = d[1]
    if int_1 != 1:
        for key, value in d.items():
            if value == int_1:
                d[key] = 1
            elif value == 1:
                d[key] = int_1
    int_2 = d[2]
    if int_2 != 2:
        for key, value in d.items():
            if value == int_2:
                d[key] = 2
            elif value == 2:
                d[key] = int_2
    

def get_list_colors(dict_int):
    dict_link = create_dict_link(dict_int)
    return [dict_link[i[1]] for i in sorted(list(dict_int.items()))]

def satif(dict_int):
    if 3 in dict_int.values():
        return (False, dict_int[3], dict_int[5])
    return (True, dict_int[3], dict_int[5])

def test_or():
    l = []
    for i in range(20):
        G = creat_or2_graph()
        dict_int = nx.greedy_color(G, 'random_sequential')
        permu_int(dict_int)
        r = satif(dict_int)
        if r[0] and (r[1], r[2]) not in l:
            l.append((r[1], r[2]))
        '''subax = plt.subplot(121+i)
        H = nx.relabel_nodes(G, create_relabel_dict())
        nx.draw(H, pos = create_pos_or2_graph(), font_size = 10, font_color = 'white', 
                node_color = get_list_colors(dict_int), with_labels = True, width = 0.5)'''
    print("valeurs de A et B satifaisant :", l)

test_or()
plt.show()