##### import modules
import networkx as nx
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 8))

#### Functions

### Create graph

def get_graph_base(nb_var):
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
    for i in range(1, nb_var+1):
        G.add_edges_from([(str(i), str(-i)), (str(i), 'N'), (str(-i), 'N')])
    return G

def add_clause(G, clause_nb, x1, x2, x3) :
    """ adds a disjunction clause with input variables x1, x2 and x3 to the graph 

    Parameters
    -----------
    G: Networkx graph
        graph use to implement clauses
    clause_nb: int
        clause's number in the cnf formula
    x1, x2, x3 : str
        clause input variable names
    """
    # set names
    N_x1 = f"N_{x1}_{clause_nb}"; N_x2 = f"N_{x2}_{clause_nb}"
    N_x3 = f"N_{x2}_{clause_nb}"; dij_x1x2 = f"dij_{x1}{x2}_{clause_nb}"
    N_x1x2 = f"N_{x1}{x2}_{clause_nb}"; dij_x1x2x3 = f"dij_{x1}{x2}{x3}_{clause_nb}"
    # add edges (and nodes)
    G.add_edges_from([(x1, N_x1), (x2, N_x2), (N_x1, N_x2), (N_x1, dij_x1x2), (N_x2, dij_x1x2),
                      (dij_x1x2, N_x1x2), (x3, N_x3), (N_x1x2, N_x3), (N_x1x2, dij_x1x2x3),
                      (N_x3, dij_x1x2x3), (dij_x1x2x3, 'F'), (dij_x1x2x3, 'N')])

def get_graph_from_cnf(list_cnf, nb_vars): 
    """ returns the graph corresponding to the cnf formula

    Parameters
    -----------
    list_cnf: list
        list of 3-uplet of literals (str), each corresonding to a clause
    nb_vars: int
        number of clauses in the formula
    
    Returns
    --------
    G: Networkx graph
        graph that contains variables and clauses
    """
    G = get_graph_base(nb_vars)
    for clause_nb in range(len(list_cnf)):
        add_clause(G, clause_nb+1, list_cnf[clause_nb][0], 
                   list_cnf[clause_nb][1], list_cnf[clause_nb][2])
    return G

### Coloring

def get_dict_links(dict_int):
    """ returns a dict that links int and colors according to our desired color references

    Parameters
    -----------
    dict_int: dict
        dict with graph nodes (str) as keys and integers representing colors as values 
    
    Returns
    --------
    dict_links: dict
        dict whose keys are integers and whose values are the corresponding colors (str)
    """
    dict_links = {}
    int_F = dict_int['F']; int_V = dict_int['V']; int_N = dict_int['N']
    dict_links[int_F] = 'red'; dict_links[int_V] = 'green'; dict_links[int_N] = 'blue'
    return dict_links
    
def get_dict_colors(dict_colors_int, dict_links):
    """ returns a dict that associates graph nodes and colors that will be used for draw

    Parameters
    -----------
    dict_colors_int: dict
        dict with graph nodes (str) as keys and integers representing colors as values 
    dict_links: dict
        dict whose keys are integers and whose values are the corresponding colors (str)

    Returns
    --------
    unamed: dict
        dict with graph nodes (str) as keys and colors as values (str)
    """
    return {node: dict_links[dict_colors_int[node]] for node in dict_colors_int.keys()}

def get_list_colors(G, dict_colors):
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
    return name[0] not in ['V', 'F', 'N', 'd', '-'] # non-variable nodes begin with these characters

def get_dict_bin_vars(dict_colors):
    """ returns a dict that associate variable nodes and boolean values according to their color

    Parameters
    -----------
    dict_colors: dict
        dict that associates graph nodes and colors that will be used for draw
    Returns
    --------
    unamed: dict
        dict with variable nodes (str) as keys and booleans as values
    """
    return {node: dict_colors[node] == 'green' for node in dict_colors.keys() if is_a_var(node)}

def graph_3_coloring(G, nb_vars: int, with_draw=True) -> tuple:
    """ returns a tuple of solutions deduced from the coloring and draws the graph 
    if possible and desired

    Parameters
    -----------
    G: Networkx graph
        graph on which we have implemented the cnf formula
    nb_vars: int
        number of variables in the cnf formula
    with_draw: bool
        optional, default value is True, must be set False if drawing is not desired
    
    Returns
    --------
    res_tuple: tuple
        tuple having as first element a boolean corresponding to the success of 3-coloring, 
        as second a dictation associating variables (str) and their values (bool) 
        (empty if no 3-coloring), and as third a boolean corresponding to drawing execution
    """
    res_tuple = (False, {}, False)
    dict_coloring_int = nx.greedy_color(G, 'DSATUR')
    if 3 not in dict_coloring_int.values():
        dict_links = get_dict_links(dict_coloring_int)
        dict_colors = get_dict_colors(dict_coloring_int, dict_links)
        res_tuple[0] = True
        res_tuple[1] = get_dict_bin_vars(dict_colors)
        if with_draw:  
            res_tuple[2] = True
            list_colors = get_list_colors(G, dict_colors)
            nx.draw_networkx(G, node_color = list_colors)   # Draw graph
    return res_tuple


#### Main Program

list_cnf_formula = [('1', '2', '3'),
                    ('1', '-2', '-3')]
nb_vars = 3

G = get_graph_from_cnf(list_cnf_formula, nb_vars)
solv_list = graph_3_coloring(G, nb_vars)
print(solv_list)

if solv_list[2]:
    plt.show()                                      # ShowFigure