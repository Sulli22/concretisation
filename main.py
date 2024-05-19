#### imports

import os
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from pysat.formula import CNF
from pysat.solvers import Solver
from pycsp3 import VarArray, solve, values, satisfy, SAT

#### cnf to graph functions

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
        graph that contains ``nb_vars`` 3-cliques and one for our 
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
        graph use to implement clauses
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

#### graph coloring functions

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
    # Relabel nodes if needed
    G_copy = relabel_nodes(G) if relabel_need else G

    x  = VarArray(size = len(G_copy), dom = ['green', 'red', 'blue'])
    dict_neighbor = {i: set(G_copy[i]) for i in G_copy}

    satisfy(
        x[i] != x[j] for i in G_copy for j in dict_neighbor[i]
    )

    # Return the list of colors
    if solve() is SAT:
        return values(x)

#### main cnf to graph

def main_cnf2graph():
    """ Generate the graph corresponding to the cnf formula
    and uses a coloring algorithm based on user input """
    print("<title>")
    
    # Prompt for file name and check existence
    formula_file = input("Enter the file name (without .cnf extension): ")
    while not os.path.isfile(f"./cnf_formulas/{formula_file}.cnf"):
        formula_file = input("File not found. Enter a valid file name: ")
    
    # Read the CNF formula from file
    cnf_formula = CNF(from_file=f"./cnf_formulas/{formula_file}.cnf")
    G, pos = get_graph_from_cnf(cnf_formula)
    
    # Prompt for algorithm choice
    print("Select an algorithm:")
    print("1 - DSATUR")
    print("2 - CNF")
    print("3 - PYCSP")
    rep = input("Your choice: ")
    dict_funct = {
        '1': get_list_colors_DSATUR, 
        '2': get_list_colors_CNF, 
        '3': get_list_colors_CSP
    }
    while rep not in dict_funct:
        rep = input("Invalid choice. Please select 1, 2, or 3: ")

    # Get list of colors using the selected algorithm
    if rep == '1':
        list_colors = dict_funct[rep](G, cnf_formula)
    else:
        list_colors = dict_funct[rep](G, True)
    
    if list_colors:
        # Standardize colors to green, red, and blue if needed
        if list_colors[:3] != ['green', 'red', 'blue']:
            dict_links = {list_colors[0]: 'green', list_colors[1]: 'red', \
                          list_colors[2]: 'blue'}
            list_colors = [dict_links[color] for color in list_colors]

        # Define labels for nodes
        labels = {n: (n.split('_')[0] if n[0] != 'I' and \
                      len(n.split('∨')) != 2 else '') for n in G.nodes}
        
        # Draw the graph
        nx.draw_networkx(G, node_color=list_colors, pos=pos, labels=labels, \
                         edge_color='grey')
        
        # Maximize the plot window
        plt.get_current_fig_manager().window.state('zoomed')
        
        # Show the plot
        plt.show()

#### main coloring

def main_graphColoring():
    """ Generate and color a random graph based on user input """
    print('<Title>')

    # Prompt for the number of nodes and edges
    nb_nodes = int(input("Enter the number of nodes: "))
    nb_edges = int(input("Enter the number of edges: "))

    # Generate a random graph with specified nodes and edges
    G = nx.gnm_random_graph(nb_nodes, nb_edges)
    pos = nx.random_layout(G)
    
    # Plot the uncolored graph
    plt.subplot(121)
    plt.title("Uncolored Graph")
    nx.draw_networkx(G, pos=pos)

    # Prompt for the coloring algorithm choice
    print("Select a coloring algorithm:")
    print("1 - CNF")
    print("2 - PYCSP")
    rep = input("Your choice: ")
    dict_funct = {'1': get_list_colors_CNF, '2': get_list_colors_CSP}
    while rep not in dict_funct:
        rep = input("Invalid choice. Please select 1 or 2: ")

    # Get the list of colors using the selected algorithm
    list_colors = dict_funct[rep](G, False)

    # Plot the colored graph if coloring is successful
    if list_colors:
        plt.subplot(122)
        plt.title("Colored Graph: 3-coloring")
        nx.draw_networkx(G, pos=pos, node_color=list_colors)

    # Maximize the plot window
    plt.get_current_fig_manager().window.state('zoomed')

    # Show the plot
    plt.show()

#### main program

def display_menu():
    """ Displays the main menu to the user """
    print('<Title>')
    print("1 - Get the graph corresponding to a CNF formula")
    print("2 - Get a graph coloring without greedy algorithm")

def get_user_choice(valid_choices: list) -> str:
    """ Prompts the user to make a choice and ensures it is valid

    Parameters:
    -----------
    valid_choices: list of str 
        List of valid choices

    Returns
    --------
    choice: str
        The user's valid choice
    """
    choice = input("Your choice: ")
    while choice not in valid_choices:
        choice = input("Invalid choice. Please enter a valid option: ")
    return choice

def main():
    """ Main function that runs the program """
    # Display the menu
    display_menu()

    # Get the user's choice
    choice = get_user_choice(['1', '2'])

    # Handle the user's choice
    dict_funct = {'1': main_cnf2graph, '2': main_graphColoring}
    dict_funct[choice]()

    # Remove files created by pycsp
    if os.path.exists("main.xml"):
        os.remove("main.xml")
        for file in [f for f in os.listdir() if f.endswith(".log")]:
                os.remove(file)

if __name__ == "__main__":
    main()
    