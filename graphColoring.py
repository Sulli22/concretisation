#### imports

import networkx as nx
from pysat.formula import CNF
from pysat.solvers import Solver

#### Functions

### Relabel

def relabel_nodes(G):
    """ Relabels the nodes of a graph with integer labels

    Parameters
    -----------
    G : Networkx graph
        The graph to be relabeled

    Returns
    --------
    G_copy : Networkx graph
        A copy of the graph with nodes relabeled with integers
    
    """
    # Create a mapping from original node labels to new integer labels
    dict_relabel = {n: i for i, n in enumerate(G.nodes)}
    # Relabel nodes
    G_copy = nx.relabel_nodes(G, dict_relabel)

    return G_copy

### DSATUR 

def DSATUR(G, colors: dict):
    """ Iterates over all the nodes of G in "saturation order" ("DSATUR")

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
    """ Returns a list of colors in the order of the graph nodes, 
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
    unamed: list or bool
        list of color (str) in order of G nodes or False if no coloring
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
    """ Returns a cnf formula that is satisfiable if the graph is colorable
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

    # Node iteration
    for i in G.nodes:
        # Each node must be at least one color
        cnf.append([int(f"1{i}"), int(f"2{i}"), int(f"3{i}")])
        # Each node must be at most one color
        cnf.append([-int(f"1{i}"), -int(f"2{i}")])
        cnf.append([-int(f"1{i}"), -int(f"3{i}")])
        cnf.append([-int(f"2{i}"), -int(f"3{i}")])

    # Edge iteration
    for i, j in G.edges:
        # Two neighboring nodes cannot share the same color
        cnf.append([-int(f"1{i}"), -int(f"1{j}")])
        cnf.append([-int(f"2{i}"), -int(f"2{j}")])
        cnf.append([-int(f"3{i}"), -int(f"3{j}")])
    
    return cnf

def get_list_colors_CNF(G, relabel_need: bool) -> list:
    """ Returns a list of colors in the order of the graph nodes, 
        respecting the coloring rules

    Parameters
    -----------
    G: Networkx graph
        graph taht we want to color
    relabel_need: bool
        does the G have to be copy with new labels
        
    Returns
    --------
    unamed: list or bool
        list of color (str) in order of G nodes or False if no coloring
    """
    # Relabel nodes if needed
    G_copy = relabel_nodes(G) if relabel_need else G
    # Get CNF formula for the relabeled graph
    cnf_formula = get_cnf_from_graph(G_copy)

    with Solver(bootstrap_with=cnf_formula) as solver:
        if not solver.solve():
            return False
        model = [str(n) for n in solver.get_model() if n > 0]

    # Create a dictionary to map nodes to colors
    dict_colors = {}
    dict_links = {'1': 'green', '2': 'red', '3': 'blue'}
    for n in model:
        dict_colors[n[1:]] = dict_links[n[0]]

    # Return the list of colors in the order of the original graph nodes
    return [dict_colors[str(n)] for n in G_copy.nodes]

### CSP 

def get_list_colors_CSP(G, relabel_need: bool) -> list:
    """ Returns a list of colors in the order of the graph nodes, 
        respecting the coloring rules

    Parameters
    -----------
    G: Networkx graph
        graph taht we want to color
    relabel_need: bool
        does the G have to be copy with new labels
        
    Returns
    --------
    unamed: list or bool
        list of color (str) in order of G nodes or False if no coloring
    """
    # Imports from pycsp3 
    from pycsp3 import VarArray, solve, values, satisfy, SAT

    # Relabel nodes if needed
    G_copy = relabel_nodes(G) if relabel_need else G

    x = VarArray(size = len(G_copy), dom = ['green', 'red', 'blue'])
    dict_neighbor = {i: set(G_copy[i]) for i in G_copy}

    satisfy(x[i] != x[j] for i in G_copy for j in dict_neighbor[i])

    # Return the list of colors
    if solve() is SAT:
        return [c if c != '*' else 'green' for c in values(x)]
    return False