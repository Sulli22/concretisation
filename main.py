#### imports

import os
import networkx as nx
import matplotlib.pyplot as plt
from pysat.formula import CNF
from pycsp3 import Var, solve, satisfy, SAT

from cnfToGraph import *
from graphColoring import *

#### main cnf to graph

def main_cnf2graph2color():
    """ Generate the graph corresponding to the cnf formula
    and uses a coloring algorithm based on user input """
    print("-----------------------------")
    print("cnf files: ")
    for file in os.listdir("./cnf_formulas"):
        print("\t", file)
    
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
    print('-----------------------------')

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
    os.system('cls' if os.name == 'nt' else 'clear')
    print("1 - Get the graph corresponding to a CNF formula and colour it")
    print("2 - Colour a graph without greedy algorithm")

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
    dict_funct = {'1': main_cnf2graph2color, '2': main_graphColoring}
    dict_funct[choice]()

    # Manage pycsp warning if not used
    if not os.path.isfile("main.xml"):
        x  = Var(0, 1); satisfy(x == 0)
        if solve() is SAT:
            os.system('cls' if os.name == 'nt' else 'clear')

    # Remove files created by pycsp
    for f in os.listdir():
        if f.endswith(".log") or f == "main.xml":
            os.remove(f)

if __name__ == "__main__":
    main()