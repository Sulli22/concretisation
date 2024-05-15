#### imports

import os
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from pysat.formula import CNF
from pysat.solvers import Solver

#### cnf to graph functions

def get_graph_base(pos: dict, nb_var: int): 
    """ returns a graph that will be used to implement the clauses

    Parameters
    -----------
    nb_var: int
        number of variables required
    pos: dict
        dict that associates nodes to their position
    
    Returns
    --------
    G: Networkx graph
        graph that contains ``nb_vars`` 3-cliques and one for our 
        True, False and Neutral references
    """
    G = nx.Graph()
    G.add_edges_from([('T', 'F'), ('N', 'F'), ('T', 'N')]) # references nodes
    # references positions
    pos['T'] = [0, 6]; pos['F'] = [0, 4]; pos['N'] = [10, 5]      
    for i in range(1, nb_var+1):        # adds nodes/edges and literals pos
        G.add_edges_from([(str(i), str(-i)), (str(i), 'N'), (str(-i), 'N')])
        pos[str(i)] = [(i-1)*15, 2]
        pos[str(-i)] = [(i-1)*15+7, 2]
    return G
    
def add_clause(G, pos: dict, clause_nb: int, x1: int, x2: int, x3: int):
    """ adds a disjunction clause with input variables x1, x2, x3 to the graph 

    Parameters
    -----------
    G: Networkx graph
        graph use to implement clauses
    clause_nb: int
        clause number in the cnf formula
    x1, x2, x3 : int
        clause input variable names
    pos: dict
        dict that associates nodes to their position
    """
    # sets names
    I_x1 = f"I_{x1}_{clause_nb}"; I_x2 = f"I_{x2}_{clause_nb}"
    x1x2 = f"{x1}∨{x2}_{clause_nb}"; I_x1x2 = f"I_{x1}∨{x2}_{clause_nb}"
    I_x3 = f"I_{x3}_{clause_nb}"; x1x2x3 = f"{x1}∨{x2}∨{x3}_{clause_nb}"
    # sets pos
    pos[I_x1] = [(clause_nb)*12, 0]; pos[I_x2] = [(clause_nb)*12+5, 0]
    pos[x1x2] = [(clause_nb)*12+2.5, -2];pos[I_x1x2] = [(clause_nb)*12+2.5, -3]
    pos[I_x3] = [(clause_nb)*12+7.5, -3]
    pos[x1x2x3] = [(clause_nb)*12+5, -5-(clause_nb%4)]
    # adds edges and nodes
    G.add_edges_from([(str(x1), I_x1), (str(x2), I_x2), 
                      (I_x1, I_x2), (I_x1, x1x2), (I_x2, x1x2), 
                      (x1x2, I_x1x2), (str(x3), I_x3), 
                      (I_x1x2, I_x3), (I_x1x2, x1x2x3), (I_x3, x1x2x3), 
                      (x1x2x3, 'F'), (x1x2x3, 'N')])       

def get_graph_from_cnf(cnf_formula) -> tuple: 
    """ returns the graph corresponding to the cnf formula

    Parameters
    -----------
    cnf_formula: pysat.formula CNF()
        list of 3-uplet of literals (int), each corresonding to a clause
    
    Returns
    --------
    G: Networkx graph
        graph that contains variables and clauses
    pos: dict
        dict that associates nodes to their position
    """
    pos = {}
    G = get_graph_base(pos, cnf_formula.nv)
    clauses = cnf_formula.clauses
    for clause_nb in range(len(clauses)):
        add_clause(G, pos, clause_nb, clauses[clause_nb][0], 
                   clauses[clause_nb][1], clauses[clause_nb][2])
    return G, pos

#### graph coloring functions

### DSATUR 

def DSATUR(G, colors: dict):
    """Iterates over all the nodes of G in "saturation order" ("DSATUR").

    Parameters
    -----------
    G: NetworkX graph
        graph we want to have the saturation order
    colors: dict
        dict associates nodes of G to colors, for those nodes that have 
        already been colored

    Returns
    --------
    unamed: generator object
    """
    distinct_colors = {v: set() for v in G} # neighbors colors for each nodes
    # Add the node color assignments given in colors to the
    # distinct colors set for each neighbor of that node
    for node, color in colors.items():
        for neighbor in G[node]: # G[node] is for the neighbors of the node
            distinct_colors[neighbor].add(color)

    while len(G) != len(colors):
        # Update the distinct color sets for the neighbors
        for node, color in colors.items():
            for neighbor in G[node]:
                distinct_colors[neighbor].add(color)
        # Compute the maximum saturation 
        # and the set of nodes that achieve that saturation
        saturation = {v: len(c) for v, c in distinct_colors.items() \
                                                            if v not in colors}
        # Yield the node with the highest saturation, and break ties by degree
        node = max(saturation, key=lambda v: (saturation[v], G.degree(v)))
        yield node

def get_list_colors_DSATUR(G, cnf_formula) -> list:
    """ returns a list of colors in the order of the graph nodes, 
        respecting the coloring rules
    
    Parameters
    -----------
    G: Networkx graph
        graph that we want to color
    colors: dict
        dict associates nodes of G to colors, for those nodes that have 
        already been colored
        
    Returns
    --------
    unamed: list
        colors (str) in graph nodes order
    """

    with Solver(bootstrap_with = cnf_formula) as solver:
        if not solver.solve():
            return False
        model = solver.get_model()
    
    colors = {'T': 'green', 'F': 'red', 'N': 'blue'}
    # add colors from model
    for var in model:
        colors[str(var)] = 'green'
    
    for u in DSATUR(G, colors): # nodes of G in "saturation order"
        # Set to keep track of colors of neighbors
        names_colors = {colors[v] for v in G[u] if v in colors}
        
        # Find the first unused color
        for color in ['red', 'green', 'blue', 'grey']:
            if color not in names_colors:
                break
        # Assign the new color to the current node
        colors[u] = color
    return [colors[node] for node in G.nodes]

### CNF 

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

def get_list_colors_CNF(G, cnf_formula):
    """ returns a list of colors in the order of the graph nodes, 
        respecting the coloring rules

    Parameters
    -----------
    G: Networkx graph
        graph taht we want to color
    <>
        
    Returns
    --------
    unamed: list
        list of color (str) in order of G nodes
    """
    # relabel
    must_be_relabel = False
    for i in G.nodes:
        try:
            int(i)
        except:
            must_be_relabel = True
            break
    if must_be_relabel:
        dict_relabel = {}; i = 0
        for n in G.nodes:
            dict_relabel[n] = str(i); i += 1
        G_copy = nx.relabel_nodes(G, dict_relabel)
    else :
        G_copy = G

    cnf_formula_bis = get_cnf_from_graph(G_copy)

    with Solver(bootstrap_with = cnf_formula_bis) as solver: # pysat solver
        if not solver.solve():
            return False
        model = [str(n) for n in solver.get_model() if n > 0]

    dict_colors = {}; dict_links = {'1': 'blue', '2': 'green', '3': 'red'}
    for n in model:
        dict_colors[n[1:len(n)+1]] = dict_links[n[0]]

    return [dict_colors[n] for n in G_copy.nodes]

### PYSCSP 

def get_list_colors_PYCSP():
    """
    
    """

#### main cnf to graph

def main_cnf2graph():
    """

    """
    formula_file = input("file name (without .cnf): ")
    while formula_file + ".cnf" not in os.listdir():
        formula_file = input("file not found : ")

    cnf_formula = CNF(from_file = formula_file + ".cnf") 
    G, pos = get_graph_from_cnf(cnf_formula)

    print('<Title>')
    print("1 - DSATUR")
    print("2 - CNF")
    print("3 - PYCSP")
    rep = input("Your choice : ")
    dict_funct = {'1': get_list_colors_DSATUR, '2': get_list_colors_CNF, \
                  '3': get_list_colors_PYCSP}
    while rep not in ['1', '2', '3']:
        rep = input("This choice don't exist, your choice : ")

    list_colors = dict_funct[rep](G, cnf_formula)

    if list_colors:
        labels = {n: (n.split('_')[0] \
                    if n[0] != 'I' and len(n.split('∨')) != 2 else '') \
                    for n in G.nodes}
        
        nx.draw_networkx(G, node_color = list_colors, 
                pos = pos, labels = labels, edge_color = 'grey')   # Draw graph
        
        wm = plt.get_current_fig_manager()      # > plt fullscreen
        wm.window.state('zoomed')               #/

        plt.show()



#### main coloring


def main_graphColoring():
    """
    
    """
    nb_nodes = 10 #int(input("number of nodes : "))
    nb_edges = 10 #int(input("number of edges : "))

    G = nx.gnm_random_graph(nb_nodes, nb_edges)
    nx.relabel_nodes(G, {n: str(n) for n in G.nodes}, False)
    cnf_formula = get_cnf_from_graph(G)
    pos = nx.random_layout(G)
    
    plt.subplot(121)
    plt.title("uncolored graph")
    nx.draw_networkx(G, pos = pos)   # Draw graph

    print('<Title>')
    print("1 - CNF")
    print("2 - PYCSP")
    rep = input("Your choice : ")
    dict_funct = {'1': get_list_colors_CNF, '2': get_list_colors_PYCSP}
    while rep not in ['1', '2']:
        rep = input("This choice don't exist, your choice : ")

    list_colors = dict_funct[rep](G, cnf_formula)

    if list_colors: 
        plt.subplot(122)
        plt.title("colored graph : 3-coloring")
        nx.draw_networkx(G, pos = pos, node_color = list_colors)   # Draw graph

    wm = plt.get_current_fig_manager()      # > plt fullscreen
    wm.window.state('zoomed')               #/

    plt.show()


#### main program

run = True

while run:
    dict_funct = {'1': main_cnf2graph, '2': main_graphColoring}
    print('<Title>')
    print("1 - get the graph corresponding to a cnf formula")
    print("2 - get a graph coloring without greedy algo")
    print("3 - quit")
    rep = input("Your choice : ")
    while rep not in ['1', '2', '3']:
        rep = input("This choice don't exist, your choice : ")
    if rep == '3':
        run = False
    else:
        dict_funct[rep]()

"""
wm = plt.get_current_fig_manager()      # > plt fullscreen
wm.window.state('zoomed')               #/
"""