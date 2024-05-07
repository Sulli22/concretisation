#### imports

import networkx as nx
import matplotlib.pyplot as plt
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

### Coloring

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

def get_list_colors(G, colors: dict) -> list:
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
    if len(G) == 0:
        return {}
    
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

def graph_coloring(G, pos: dict, model: list) -> list:
    """ returns a coloring and draws the graph

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
    list_colors: list
        list of colors in order of G nodes
    """
    colors = {'T': 'green', 'F': 'red', 'N': 'blue'}
    # add colors from model
    for var in model:
        colors[str(var)] = 'green'

    list_colors = get_list_colors(G, colors)
    # labels used for proper display
    labels = {n: (n.split('_')[0] \
                if n[0] != 'I' and len(n.split('∨')) != 2 else '') \
                for n in G.nodes}
    
    plt.title(f"{model}")
    nx.draw_networkx(G, node_color = list_colors, 
                    pos = pos, labels = labels, edge_color = 'grey')   # Draw graph
    
    return list_colors

#### Main Program

#file_name = input('file name : ')
cnf_formula = CNF(from_file = 'graph_formula.cnf')

print("solv by pysat solver :")

with Solver(bootstrap_with = cnf_formula) as solver:
    # call the solver for this formula :
    is_satisfiable = solver.solve()
    print('\tformula is', f'{"s" if is_satisfiable else "uns"}atisfiable')
        
    # the formula is satisfiable :
    model = solver.get_model()
    print('\tand the model is:', model)

if is_satisfiable:
    print("graph coloring corresponding:")

    G, pos = get_graph_from_cnf(cnf_formula)
    list_colors = graph_coloring(G, pos, model)

    print(f"\t-> {len(set(list_colors))}-coloring")
    plt.show()                                      # ShowFigure