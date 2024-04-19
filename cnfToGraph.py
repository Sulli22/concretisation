##### import modules
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from pysat.formula import CNF

current_path = '/home/mashu/Documents/concretisation/'
plt.figure(figsize = (15, 15))

#### Functions

### Create graph

def get_graph_base(pos: dict, nb_var: int):
    """ returns a graph that will be used to implement the clauses

    Parameters
    -----------
    nb_var: int
        number of variables required
    
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
    return name[0] not in ['T', 'F', 'N', 'd', '-'] # non-variable nodes begin with these characters


def get_dict_bin_vars(dict_colors: dict):
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
    return {node: dict_colors[node] == 'green' for node in dict_colors.keys() 
            if is_a_var(node)}


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
            of 3-coloring, as second a dictation associating variables (str) 
            and their values (bool) (empty if no 3-coloring), and as third a 
            boolean corresponding to drawing execution
        and dict_coloring_int (dict) as second element
    """
    res_list = [False, {}, False]
    dict_coloring_int = nx.greedy_color(G, 'DSATUR')
    #if 3 not in dict_coloring_int.values():
    dict_links = get_dict_links(dict_coloring_int)
    dict_colors = get_dict_colors(dict_coloring_int, dict_links)
    res_list[0] = True
    res_list[1] = get_dict_bin_vars(dict_colors)
    if nb_clauses <= 3:  
        res_list[2] = True
        list_colors = get_list_colors(G, dict_colors)
        nx.draw_networkx(G, node_color = list_colors, pos = pos)   # Draw graph
    return res_list, dict_coloring_int

#### Main Program

cnf_formula = CNF(from_file=current_path+'simple_formula.cnf')

G, pos = get_graph_from_cnf(cnf_formula)
solv_list = graph_3_coloring(G, len(cnf_formula.clauses))
print("dict_coloring :", solv_list[1])
print("solv by graph :", solv_list[0][:2])

if solv_list[0][2]:
    plt.show()                                      # ShowFigure