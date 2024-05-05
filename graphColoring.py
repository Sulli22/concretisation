#### imports
import networkx as nx
import matplotlib.pyplot as plt
from pysat.formula import CNF
from pysat.solvers import Solver

wm = plt.get_current_fig_manager()      # > plt fullscreen
wm.window.state('zoomed')               #/

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

def get_list_color(cnf):
    with Solver(bootstrap_with=cnf) as solver:
        if not solver.solve():
            return False
        
        model = [n for n in solver.get_model() if n > 0]
    dict_colors = {}
    dict_links = {1: 'green', 2: 'red', 3: 'blue'}
    for n in model:
        n = str(n)
        dict_colors[int(n[-1])] = dict_links[int(n[0])]
    return [dict_colors[n] for n in G.nodes]

####

G = nx.Graph()

G.add_edges_from([(1, 2), (2, 3), (1, 3), (1, 4), (2, 4)])

cnf_formula = get_cnf_from_graph(G)


list_colors = get_list_color(cnf_formula)
if list_colors: 
    nx.draw_networkx(G, node_color = list_colors)   # Draw graph

plt.show()