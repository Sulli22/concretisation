##### imports
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from pysat.formula import CNF
from pysat.solvers import Solver

wm = plt.get_current_fig_manager()      # > plt fullscreen
wm.window.state('zoomed')               #/

#### Functions

### Create graph

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
    pos['T'] = np.array([0, 5])     #\
    pos['F'] = np.array([2, 5])     # > references positions
    pos['N'] = np.array([1, 3])     #/
    for i in range(1, nb_var+1):        # adds nodes/edges and literals pos
        G.add_edges_from([(str(i), str(-i)), (str(i), 'N'), (str(-i), 'N')])
        pos[str(i)] = np.array([(i-1)*2, 2])
        pos[str(-i)] = np.array([(i-1)*2+1, 2])
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
    N_x1 = f"N_{x1}_{clause_nb}"
    N_x2 = f"N_{x2}_{clause_nb}"
    dij_x1x2 = f"dij_{x1}{x2}_{clause_nb}"
    N_x1x2 = f"N_{x1}{x2}_{clause_nb}"
    N_x3 = f"N_{x3}_{clause_nb}"
    dij_x1x2x3 = f"dij_{x1}{x2}{x3}_{clause_nb}"
    # sets pos
    pos[dij_x1x2] = np.array([(clause_nb-1)*2+0.5, -2])
    pos[N_x1x2] = np.array([(clause_nb-1)*2+0.5, -3])
    pos[N_x1] = np.array([(clause_nb-1)*2, 0])
    pos[N_x2] = np.array([(clause_nb-1)*2+1, 0])
    pos[N_x3] = np.array([(clause_nb-1)*2+1.5, -3])
    pos[dij_x1x2x3] = np.array([(clause_nb-1)*2+1, -5])
    # adds edges and nodes
    G.add_edges_from([(str(x1), N_x1), (str(x2), N_x2), (N_x1, N_x2), 
                      (N_x1, dij_x1x2), (N_x2, dij_x1x2), (dij_x1x2, N_x1x2), 
                      (str(x3), N_x3), (N_x1x2, N_x3), (N_x1x2, dij_x1x2x3),
                      (N_x3, dij_x1x2x3), (dij_x1x2x3, 'F'), 
                      (dij_x1x2x3, 'N')])       

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
    clauses = cnf_formula.clauses   # int list
    for clause_nb in range(len(clauses)):
        add_clause(G, pos, clause_nb+1, clauses[clause_nb][0], 
                   clauses[clause_nb][1], clauses[clause_nb][2])
    return G, pos

### Coloring

def get_list_DSATUR(G, colors: dict):
    """Iterates over all the nodes of ``G`` in "saturation order" (also
    known as "DSATUR").

    ``G`` is a NetworkX graph. ``colors`` is a dictionary mapping nodes of
    ``G`` to colors, for those nodes that have already been colored.

    """
    distinct_colors = {v: set() for v in G} # neighbors colors for each nodes
    # Add the node color assignments given in colors to the
    # distinct colors set for each neighbor of that node

    for node, color in colors.items():
        for neighbor in G[node]:
            distinct_colors[neighbor].add(color)
            
    # If there is no colors in the dict "colors"
    if not colors:
        node = max(G, key=G.degree) # Take the node with the max degree
        yield node # Like a return but that don't stop 
        
        # Add the color 0 to the distinct colors set for each
        # neighbor of that node.If 0 nodes have been colored, simply choose the node of highest degree.
        for v in G[node]: # G[node] is for the neighbors of the node
            distinct_colors[v].add(0)

    while len(G) != len(colors):
        # Update the distinct color sets for the neighbors.
        for node, color in colors.items():
            for neighbor in G[node]:
                distinct_colors[neighbor].add(color)
        # Compute the maximum saturation and the set of nodes that achieve that saturation
        saturation = {v: len(c) for v, c in distinct_colors.items() if v not in colors}
        # Yield the node with the highest saturation, and break ties by degree
        node = max(saturation, key=lambda v: (saturation[v], G.degree(v)))
        yield node

def get_dict_coloring(G, colors: dict):
    """
    """

    if len(G) == 0:
        return {}
    
    nodes = get_list_DSATUR(G, colors) # nodes of ``G`` in "saturation order"
    
    for u in nodes:
        # Set to keep track of colors of neighbors
        num_colors = {colors[v] for v in G[u] if v in colors}
        
        # Find the first unused color
        for color in ['red', 'green', 'blue', 'grey']:
            if color not in num_colors:
                break
        # Assign the new color to the current node
        colors[u] = color
    return colors

def get_list_colors(G, dict_colors: dict) -> list:
    """ returns a list of colors in graph nodes order

    Parameters
    -----------
    G: Networkx graph
        graph that we want to color
    dict_colors: dict
        with graph nodes as keys and colors as values
        
    Returns
    --------
    unamed: list
        list of colors (str)
    """
    return [dict_colors[node] for node in G.nodes()]

def add_colors_from_model(colors: dict, model: list):
    """ add colors from model (list) in colors dict

    Parameters
    -----------
    G: Networkx graph
        graph that we want to color
    dict_colors: dict
        with graph nodes as keys and colors as values
        
    Returns
    --------
    unamed: list
        list of colors (str)
    
    """
    for var in model:
        colors[str(var)] = 'green'

def graph_coloring(G, pos: dict, model: list) -> list:
    """ returns a solution deduced from the coloring and draws the 
    graph if possible

    Parameters
    -----------
    G: Networkx graph
        graph on which we have implemented the cnf formula
    pos: dict
        dict that associates nodes to their position
    model: list
        list of literals
    
    Returns
    --------
    unamed: tuple
        tuple having as first element a dict that associate node and color (str)
        and as second element k (int) - coloring corresponding
    """
    colors = {'N': 'blue', 'F': 'red', 'T': 'green'}
    add_colors_from_model(colors, model)
    dict_colors = get_dict_coloring(G, colors)    # coloring graph
    list_colors = get_list_colors(G, dict_colors)
    nx.draw_networkx(G, node_color = list_colors, pos = pos)   # Draw graph
    return dict_colors, len(set(dict_colors.values()))

#### Main Program

def main():
    cnf_formula = CNF(from_file='formula.cnf')

    print("solv by pysat solver :")

    with Solver(bootstrap_with=cnf_formula) as solver:
        # call the solver for this formula :
        is_satisfiable = solver.solve()
        print('\tformula is', f'{"s" if is_satisfiable else "uns"}atisfiable')
        
        # the formula is satisfiable :
        model = solver.get_model()
        print('\tand the model is:', model)

        # the formula is unsatisfiable :
        print('\tand the unsatisfiable core is:', solver.get_core())

    if is_satisfiable:
        print("graph coloring corresponding:")

        G, pos = get_graph_from_cnf(cnf_formula)
        dict, k = graph_coloring(G, pos, model)

        print(f"\tdict coloring: {dict}")
        print(f"\t-> {k}-coloring")
        plt.show()                                      # ShowFigure

main()