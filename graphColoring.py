#### imports

import networkx as nx
import matplotlib.pyplot as plt
from pysat.formula import CNF
from pysat.solvers import Solver

####

def get_cnf_from_graph(G):
    """ returns a cnf formula that is satisfiable if the graph is colorable
    literals names:
        - 1i = node i is green
        - 2i = node i is red
        - 3i = node i is blue

    Parameters
    -----------
    G: Networkx graph
        graph taht we want to color
        
    Returns
    --------
    cnf: pysat.formula.CNF
        cnf formula
    """
    cnf = CNF()

    # node iteration
    for i in G.nodes:
        # each node have at least one color
        cnf.append([int("1"+i), int("2"+i), int("3"+i)])
        # each node has at most one color
        cnf.append([-int("1"+i), -int("2"+i)])
        cnf.append([-int("1"+i), -int("3"+i)])
        cnf.append([-int("2"+i), -int("3"+i)])

    # edge iteration
    for i, j in G.edges:
        # two neighboring nodes cannot have the same color
        cnf.append([-int("1"+i), -int("1"+j)])
        cnf.append([-int("2"+i), -int("2"+j)])
        cnf.append([-int("3"+i), -int("3"+j)])

    return cnf

def get_list_color(G, cnf):
    """ returns a list of colors in the order of the graph nodes, 
        respecting the coloring rules

    Parameters
    -----------
    G: Networkx graph
        graph taht we want to color
    cnf: pysat.formula.CNF
        cnf formula corresponding
        
    Returns
    --------
    unamed: list
        list of color (str) in order of G nodes
    """
    with Solver(bootstrap_with = cnf) as solver: # pysat solver
        if not solver.solve():
            return False
        model = [str(n) for n in solver.get_model() if n > 0]

    dict_colors = {}; dict_links = {'1': 'green', '2': 'red', '3': 'blue'}
    for n in model:
        dict_colors[n[1:len(n)+1]] = dict_links[n[0]]
    return [dict_colors[n] for n in G.nodes]

#### main

nb_nodes = 100 #int(input("number of nodes : "))
nb_edges = 150 #int(input("number of edges : "))

G = nx.gnm_random_graph(nb_nodes, nb_edges)
nx.relabel_nodes(G, {n: str(n) for n in G.nodes}, False)
cnf_formula = get_cnf_from_graph(G)
pos = nx.random_layout(G)

cnf_formula.to_file('graph_formula.cnf')  # writing to a file

plt.subplot(131)
plt.title("uncolored graph")
nx.draw_networkx(G, pos = pos)   # Draw graph

""" verif avec greedy_color
plt.subplot(132)
dict_greedy = nx.greedy_color(G, 'DSATUR')
plt.title(f"greedy colored graph : {len(set(dict_greedy.values()))}-coloring")
nx.draw_networkx(G, pos = pos, node_color = [dict_greedy[n] for n in G.nodes])   # Draw graph
"""

list_colors = get_list_color(G, cnf_formula)
if list_colors: 
    plt.subplot(133)
    plt.title("colored graph : 3-coloring")
    nx.draw_networkx(G, pos = pos, node_color = list_colors)   # Draw graph

wm = plt.get_current_fig_manager()      # > plt fullscreen
wm.window.state('zoomed')               #/

plt.show()