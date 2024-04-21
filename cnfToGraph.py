##### import modules
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from pysat.formula import CNF
from pysat.solvers import Solver

current_path = ''
#current_path = '/home/mashu/Documents/concretisation/'
plt.figure(figsize = (15, 15))

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
    G.add_edges_from([('T', 'F'), ('N', 'F'), ('T', 'N')])
    pos['T'] = np.array([0, 5])
    pos['F'] = np.array([2, 5])
    pos['N'] = np.array([1, 3])
    for i in range(1, nb_var+1):
        G.add_edges_from([(str(i), str(-i)), (str(i), 'N'), (str(-i), 'N')])
        pos[str(i)] = np.array([i-1, 2]); pos[str(-i)] = np.array([i-0.5, 2])
    return G
    
def add_clause(G, pos: dict, clause_nb: int, x1: int, x2: int, x3: int) :
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
    # set names and positions
    N_x1 = f"N_{x1}_{clause_nb}"; 
    pos[N_x1] = np.array([(clause_nb-1)*2, 0])
    N_x2 = f"N_{x2}_{clause_nb}"; 
    pos[N_x2] = np.array([(clause_nb-1)*2+1, 0])
    dij_x1x2 = f"dij_{x1}{x2}_{clause_nb}"; 
    pos[dij_x1x2] = np.array([(clause_nb-1)*2+0.5, -2])
    N_x1x2 = f"N_{x1}{x2}_{clause_nb}"; 
    pos[N_x1x2] = np.array([(clause_nb-1)*2+0.5, -3])
    N_x3 = f"N_{x3}_{clause_nb}"; 
    pos[N_x3] = np.array([(clause_nb-1)*2+1.5, -3])
    dij_x1x2x3 = f"dij_{x1}{x2}{x3}_{clause_nb}"; 
    pos[dij_x1x2x3] = np.array([(clause_nb-1)*2+1, -5])
    # add edges (and nodes)
    G.add_edges_from([(str(x1), N_x1), (str(x2), N_x2), (N_x1, N_x2), 
                      (N_x1, dij_x1x2), (N_x2, dij_x1x2), (dij_x1x2, N_x1x2), 
                      (str(x3), N_x3), (N_x1x2, N_x3), (N_x1x2, dij_x1x2x3),
                      (N_x3, dij_x1x2x3), (dij_x1x2x3, 'F'), 
                      (dij_x1x2x3, 'N')])

def get_graph_from_cnf(cnf_formula): 
    """ returns the graph corresponding to the cnf formula

    Parameters
    -----------
    cnf_formula: pysat.formula CNF()
        list of 3-uplet of literals (int), each corresonding to a clause
    
    Returns
    --------
    G: Networkx graph
        graph that contains variables and clauses
    """
    pos = {}
    G = get_graph_base(pos, cnf_formula.nv)
    clauses = cnf_formula.clauses
    for clause_nb in range(len(clauses)):
        add_clause(G, pos, clause_nb+1, clauses[clause_nb][0], 
                   clauses[clause_nb][1], clauses[clause_nb][2])
    return G, pos

### Coloring

def get_dict_links(dict_int: dict) -> dict:
    """ returns a dict that links int and colors according to our desired 
    color references

    Parameters
    -----------
    dict_int: dict
        dict with graph nodes (str) as keys and integers representing colors as
        values 
    
    Returns
    --------
    dict_links: dict
        dict whose keys are integers and whose values are the corresponding 
        colors (str)
    """
    dict_links = {}
    int_F = dict_int['F']; int_T = dict_int['T']; int_N = dict_int['N']
    dict_links[int_F] = 'red'; dict_links[int_T] = 'green' 
    dict_links[int_N] = 'blue'
    for i in range(4):
        if i not in [int_F, int_T, int_N]:
            dict_links[i] = 'grey'
    return dict_links
    

def get_dict_colors(dict_colors_int: dict, dict_links: dict) -> dict:
    """ returns a dict that associates graph nodes and colors that will be 
    used for draw

    Parameters
    -----------
    dict_colors_int: dict
        dict with graph nodes (str) as keys and integers representing colors 
        as values 
    dict_links: dict
        dict whose keys are integers and whose values are the corresponding 
        colors (str)

    Returns
    --------
    unamed: dict
        dict with graph nodes (str) as keys and colors as values (str)
    """
    return {node: dict_links[dict_colors_int[node]] for node in 
            dict_colors_int.keys()}


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


def is_a_var(name: str) -> bool:
    """ returns the answer to: is the node a variable?

    Parameters
    -----------
    name: str
        node name
    
    Returns
    --------
    unamed: bool
        True if node is a variable else False
    """
    return name[0] not in ['T', 'F', 'N', 'd', '-'] 
                        # non-variable nodes begin with these characters


def get_model(dict_colors: dict):
    """ returns a dict that associate variable nodes and boolean values 
    according to their color

    Parameters
    -----------
    dict_colors: dict
        dict that associates graph nodes and colors that will be used for draw
        
    Returns
    --------
    unamed: dict
        dict with variable nodes (str) as keys and booleans as values
    """
    list_model = []
    for node in dict_colors.keys():
        if is_a_var(node):
            list_model.append(int(node) if dict_colors[node] == 'green' else -int(node)) 
    return sorted(list_model, key = lambda i: abs(i))


def graph_3_coloring(G, nb_clauses: int) -> list:
    """ returns a list of solutions deduced from the coloring and draws the 
    graph if possible

    Parameters
    -----------
    G: Networkx graph
        graph on which we have implemented the cnf formula
    nb_clauses: int
        number of clauses in cnf formula implemented    
    
    Returns
    --------
    unamed: list
        list having as first element res_list (list) descirbe by
            list having as first element a boolean corresponding to the success 
            of 3-coloring and as second a list of the model (empty if no 
            3-coloring)
        and k (int) - coloring
    """
    res_list = [False, []]
    dict_coloring_int = nx.greedy_color(G, 'DSATUR')
    dict_links = get_dict_links(dict_coloring_int)
    dict_colors = get_dict_colors(dict_coloring_int, dict_links)
    if 3 not in dict_coloring_int.values():
        res_list[0] = True
        res_list[1] = get_model(dict_colors)
    #if nb_clauses <= 3:  
    #res_list[2] = True
    list_colors = get_list_colors(G, dict_colors)
    nx.draw_networkx(G, node_color = list_colors, pos = pos)   # Draw graph
    return res_list, len(set(dict_coloring_int.values()))

#### Main Program

cnf_formula = CNF(from_file=current_path+'simple_formula.cnf')

print("solv by pysat solver :")

with Solver(bootstrap_with=cnf_formula) as solver:
    # call the solver for this formula:
    print('\tformula is', f'{"s" if solver.solve() else "uns"}atisfiable')
    
    # the formula is satisfiable :
    print('\tand the model is:', solver.get_model())

    # the formula is unsatisfiable :
    print('\tand the unsatisfiable core is:', solver.get_core())

print("solv by graph :")

G, pos = get_graph_from_cnf(cnf_formula)
solv_list = graph_3_coloring(G, len(cnf_formula.clauses))

print(f"\tformula is {"s" if solv_list[1] <= 3 else "uns"}atisfiable ({solv_list[1]}-coloring)")
print('\t', solv_list[0][1])

#if solv_list[0][2]:
plt.show()                                      # ShowFigure