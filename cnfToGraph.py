#### imports

import networkx as nx

#### Functions

def get_graph_base(pos: dict, nb_var: int): 
    """ Returns a graph that will be used to implement the clauses

    Parameters
    -----------
    nb_var: int
        number of variables required
    pos: dict
        dict that associates nodes to their position
    
    Returns
    --------
    G: Networkx graph
        graph that contains ``nb_vars`` 3-cliques and one more for our 
        True, False and Neutral references
    """
    # Create an empty graph
    G = nx.Graph()

    # Add reference nodes and their positions
    G.add_edges_from([('T', 'F'), ('N', 'F'), ('T', 'N')]) 
    pos.update({'T': [0, 6], 'F': [0, 4], 'N': [10, 5]}) 

    # Add nodes and edges for variables and their negations
    for i in range(1, nb_var + 1):
        var_str = str(i)
        neg_var_str = str(-i)

        G.add_edges_from([(var_str, neg_var_str), (var_str, 'N'), (neg_var_str, 'N')])

        # Assign positions to variable and negation nodes
        pos[var_str] = [(i - 1) * 15, 2]
        pos[neg_var_str] = [(i - 1) * 15 + 7, 2]

    return G
    
def add_clause(G, pos: dict, nb_clauses: int, \
               clause_nb: int, x1: int, x2: int, x3: int):
    """ Adds a disjunction clause with input variables x1, x2, x3 to the graph 

    Parameters
    -----------
    G: Networkx graph
        graph used to implement clauses
    nb_clauses: int
        total number of clauses
    clause_nb: int
        clause number in the cnf formula
    x1, x2, x3 : int
        clause input variable names
    pos: dict
        dict that associates nodes to their position
    """
    # Set names for nodes
    I_x1 = f"I_{x1}_{clause_nb}"; I_x2 = f"I_{x2}_{clause_nb}"
    x1x2 = f"{x1}∨{x2}_{clause_nb}"; I_x1x2 = f"I_{x1}∨{x2}_{clause_nb}"
    I_x3 = f"I_{x3}_{clause_nb}"; x1x2x3 = f"{x1}∨{x2}∨{x3}_{clause_nb}"
    
    # Set positions for nodes
    pos[I_x1] = [(clause_nb)*12, 0]; pos[I_x2] = [(clause_nb)*12+5, 0]
    pos[x1x2] = [(clause_nb)*12+2.5, -2];pos[I_x1x2] = [(clause_nb)*12+2.5, -3]
    pos[I_x3] = [(clause_nb)*12+7.5, -3]
    pos[x1x2x3] = [(clause_nb)*12+5, \
                     -5-(clause_nb%(nb_clauses//(6 if nb_clauses >=6 else 1)))]

    # Add edges and nodes to the graph
    G.add_edges_from([(str(x1), I_x1), (str(x2), I_x2), 
                      (I_x1, I_x2), (I_x1, x1x2), (I_x2, x1x2), 
                      (x1x2, I_x1x2), (str(x3), I_x3), 
                      (I_x1x2, I_x3), (I_x1x2, x1x2x3), (I_x3, x1x2x3), 
                      (x1x2x3, 'F'), (x1x2x3, 'N')])    

def get_graph_from_cnf(cnf_formula) -> tuple: 
    """ Returns the graph corresponding to the cnf formula

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
    # Initialize an empty dictionary to store node positions
    pos = {}

    # Create the base graph structure
    G = get_graph_base(pos, cnf_formula.nv)

    # Extract clauses from the CNF formula
    clauses = cnf_formula.clauses

    # Iterate over each clause and add it to the graph
    for clause_nb, clause in enumerate(clauses):
        # Add the current clause to the graph
        add_clause(G, pos, len(clauses), clause_nb, *clause)

    # Return the constructed graph and node positions
    return G, pos