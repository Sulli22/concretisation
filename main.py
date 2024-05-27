#### imports

import os
import time
import networkx as nx
from platform import system
from pysat.formula import CNF
import matplotlib.pyplot as plt

from cnfToGraph import *
from graphColoring import *

#### Maximize the plot window

def maximize():
    """ Maximizes the plot window """
    backend = plt.get_backend()
    cfm = plt.get_current_fig_manager()
    if backend == "wxAgg":
        cfm.frame.Maximize(True)
    elif backend == "TkAgg":
        if system() == "Windows":
            cfm.window.state("zoomed")  # This is windows only
        else:
            cfm.resize(*cfm.window.maxsize())
    elif backend == "QT4Agg":
        cfm.window.showMaximized()

#### main cnf to graph

def main_cnf2graph2color():
    """ Generates the graph corresponding to the cnf formula
    and uses a coloring algorithm based on user input """
    # Prompt for algorithm choice
    print("-"*70)
    print("Select an algorithm:")
    print("1 - DSATUR")
    print("2 - CNF")
    print("3 - CSP")
    rep = input("Your choice: ")
    while rep not in ['1', '2', '3']:
        rep = input("Invalid choice. Please select 1, 2, or 3: ")

    # Prompt for file name and check existence
    print('-'*70)
    print("cnf files: \n\t {nb of vars}v{nb of clauses}c.cnf")
    for file in os.listdir("./cnf_formulas"):
        print(f"\t {file}")
    formula_file = input("Enter the file name (without .cnf extension): ")
    while not os.path.isfile(f"./cnf_formulas/{formula_file}.cnf"):
        formula_file = input("File not found. Enter a valid file name: ")
    print('-'*70)
    
    # start chrono
    t1 = time.time()
    # Read the CNF formula from file
    cnf_formula = CNF(from_file=f"./cnf_formulas/{formula_file}.cnf")
    G, pos = get_graph_from_cnf(cnf_formula)
    # end chrono
    t2 = time.time()
    list_duration = [t2-t1]
    print(f"- get graph ~ {list_duration[-1]}s")

    # start chrono
    t1 = time.time()
    # Get list of colors using the selected algorithm
    if rep == '1':
        list_colors = get_list_colors_DSATUR(G, cnf_formula)
    elif rep == '2':
        list_colors = get_list_colors_CNF(G, True)
    else:
        list_colors = get_list_colors_CSP(G, True)
    # end chrono
    t2 = time.time()    
    list_duration.append(t2-t1)
    print(f"- get list color ~ {list_duration[-1]}s")

    if list_colors:
        # start chrono
        t1 = time.time()
        # Standardize colors to green, red, and blue if needed
        if list_colors[:3] != ['green', 'red', 'blue']:
            dict_links = {list_colors[0]: 'green', list_colors[1]: 'red', \
                          list_colors[2]: 'blue'}
            list_colors = [dict_links[color] for color in list_colors]

        # Define labels for nodes
        labels = {n: (n.split('_')[0] if n[0] != 'I' and \
                      len(n.split('∨')) != 2 else '') for n in G.nodes}
        
        # Draw the graph
        plt.title(f"{len(G)} nodes and {len(G.edges)} edges")
        nx.draw_networkx(G, node_color=list_colors, pos=pos, labels=labels, \
                         edge_color='grey')
        # end chrono
        t2 = time.time()    
        list_duration.append(t2-t1)
        print(f"- plot colored graph ~ {list_duration[-1]}s")

        # Maximize the plot window
        maximize()
        
        # Show the plot
        plt.show()
    
    else:
        print("-> the formula is unsatisfiable")
    
    # final duration
    print(f"-> duration ~ {sum(list_duration)}s")


#### main coloring

def main_graphColoring():
    """ Generates and color a random graph based on user input """
    print("-"*70)
    # Prompt for the coloring algorithm choice
    print("Select a coloring algorithm:")
    print("1 - CNF")
    print("2 - CSP")
    rep = input("Your choice: ")
    dict_funct = {'1': get_list_colors_CNF, '2': get_list_colors_CSP}
    while rep not in dict_funct:
        rep = input("Invalid choice. Please select 1 or 2: ")
    print("-"*70)

    # Prompt for the number of nodes and edges
    nb_nodes = None; nb_edges = None
    while nb_nodes is None:
        try:
            nb_nodes = int(input("Enter the number of nodes: "))
        except:
            print("Unvalid number,")
    while nb_edges is None:
        try:
            nb_edges = int(input("Enter the number of edges: "))
        except:
            print("Unvalid number,")
    print("-"*70)

    # start chrono
    t1 = time.time()
    # Generate a random graph with specified nodes and edges
    G = nx.gnm_random_graph(nb_nodes, nb_edges)
    pos = nx.random_layout(G)
    # end chrono
    t2 = time.time()
    list_duration = [t2-t1]
    print(f"- generate random graph ~ {list_duration[-1]}s")

    # Plot the uncolored graph
    t1 = time.time()
    plt.subplot(121)
    plt.title(f"Uncolored Graph: {nb_nodes} nodes and {nb_edges} edges")
    nx.draw_networkx(G, pos=pos)
    t2 = time.time()    
    list_duration.append(t2-t1)
    print(f"- plot uncolored graph ~ {list_duration[-1]}s")

    # start chrono
    t1 = time.time()
    # Get the list of colors using the selected algorithm
    list_colors = dict_funct[rep](G, False)
    # end chrono
    t2 = time.time()
    list_duration.append(t2-t1)
    print(f"- get list colors: {list_duration[-1]}s")
    
    # start chrono
    t1 = time.time() 
    # Plot the colored graph if coloring is successful
    plt.subplot(122)
    if list_colors:
        plt.title("Colored Graph: 3-coloring")
        nx.draw_networkx(G, pos=pos, node_color=list_colors)
    else:
        plt.title("Coloring not found")
    # end chrono
    t2 = time.time() 
    list_duration.append(t2-t1)
    print(f"- plot colored graph ~ {list_duration[-1]}s")

    # final duration
    print(f"-> duration: ~ {sum(list_duration)}s")

    # Maximize the plot window
    maximize()

    # Show the plot
    plt.show()

#### main program

def main():
    """ Main function that runs the program """
    # Display the menu
    print("-"*70)
    print("Select :")
    print("1 - Get the graph corresponding to a CNF formula and color it")
    print("2 - Color a graph without greedy algorithm")

    # Get the user's choice
    choice = input("Your choice: ")
    while choice not in ['1', '2']:
        choice = input("Invalid choice. Please enter 1 or 2: ")

    # Handle the user's choice
    {'1': main_cnf2graph2color, '2': main_graphColoring}[choice]()

    # Remove files created by pycsp
    for f in os.listdir():
        if f.endswith(".log") or f == "main.xml":
            os.remove(f)

if __name__ == "__main__":
    main()