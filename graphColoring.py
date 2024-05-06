#### imports
import networkx as nx
import matplotlib.pyplot as plt
from pysat.formula import CNF
from pysat.solvers import Solver

####

def get_cnf_from_graph(G):
    """
    
    """
    nodes = G.nodes
    E = G.edges
    cnf = CNF()
    for i in nodes:
        cnf.append([int("1"+str(i)), int("2"+str(i)), int("3"+str(i))])

        cnf.append([-int("1"+str(i)), -int("2"+str(i))])
        cnf.append([-int("1"+str(i)), -int("3"+str(i))])
        cnf.append([-int("2"+str(i)), -int("3"+str(i))])

    for i, j in E:
        cnf.append([-int("1"+str(i)), -int("1"+str(j))])
        cnf.append([-int("2"+str(i)), -int("2"+str(j))])
        cnf.append([-int("3"+str(i)), -int("3"+str(j))])

    return cnf

def get_list_color(cnf, G):
    """
    
    """
    with Solver(bootstrap_with = cnf) as solver:
        if not solver.solve():
            return False
        model = [n for n in solver.get_model() if n > 0]

    dict_colors = {}
    for n in model:
        n = str(n)
        dict_colors[int(n[-1])] = {'1': 'green', '2': 'red', '3': 'blue'}[n[0]]
    return [dict_colors[n] for n in G.nodes]

#### main
nb_nodes = int(input("number of nodes : "))
nb_edges = int(input("number of edges : "))

G = nx.gnm_random_graph(nb_nodes, nb_edges)
cnf_formula = get_cnf_from_graph(G)
pos = nx.spring_layout(G)

plt.subplot(121)
plt.title("uncolored graph")
nx.draw_networkx(G, pos = pos)   # Draw graph

list_colors = get_list_color(cnf_formula, G)
if list_colors: 
    plt.subplot(122)
    plt.title("colored graph")
    nx.draw_networkx(G, pos = pos, node_color = list_colors)   # Draw graph

wm = plt.get_current_fig_manager()      # > plt fullscreen
wm.window.state('zoomed')               #/

plt.show()