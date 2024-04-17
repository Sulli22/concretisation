import networkx as nx
import matplotlib.pyplot as plt

def creat_or_graph():
    adjacency_dict = {0: (1, 2, 9), 1: (0, 2), 2: (0, 1, 9), 3 : (2, 4, 8), 4 : (2, 3, 7), 
                  5: (2, 6, 7, 8), 6: (2,5), 7: (8, 4, 5), 8: (7, 9, 3, 5), 9: (8, 0, 2)}

    '''
    0 : 0, 1 : 1, 2 : N, 3 : A, 4 : !A, 5 : B, 6 : !B
    '''
    return nx.Graph(adjacency_dict)


def permu_int(d):
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
    

def get_list_colors(dict_int) :
    dict_link = {0: 'red', 1: 'green', 2: 'blue', 3: 'grey'}
    return [dict_link[i[1]] for i in sorted(list(dict_int.items()), key = lambda i: i[0])]

def satif(dict_int) :
    if 3 in dict_int.values():
        return (False, dict_int[3], dict_int[5])
    return (True, dict_int[3], dict_int[5])

def test_10():
    for i in range(1):
        l = []
        G = creat_or_graph()
        dict_int = nx.greedy_color(G, 'random_sequential')
        permu_int(dict_int)
        r = satif(dict_int)
        if r[0] :
            l.append(("a =" + r[1], "b = " + r[2])
        #subax = plt.subplot(221+i)
        #nx.draw(G, with_labels=True, node_color = get_list_colors(dict_int))

test_10()
#plt.show()