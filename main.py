#### imports

import time
import os
from platform import system
import networkx as nx
import matplotlib.pyplot as plt
from pysat.formula import CNF

from cnfToGraph import *
from graphColoring import *

#### Maximize the plot window

def maximize():
    """ Maximize the plot window """
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
    """ Generate the graph corresponding to the cnf formula
    and uses a coloring algorithm based on user input """
    print("----------------------------------------------------------")
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
    print("----------------------------------------------------------")
    print("cnf files: ")
    for file in os.listdir("./cnf_formulas"):
        print("\t", file)
    print("----------------------------------------------------------")
    
    # Prompt for file name and check existence
    formula_file = input("Enter the file name (without .cnf extension): ")
    while not os.path.isfile(f"./cnf_formulas/{formula_file}.cnf"):
        formula_file = input("File not found. Enter a valid file name: ")

    # Read the CNF formula from file
    t1 = time.time()
    cnf_formula = CNF(from_file=f"./cnf_formulas/{formula_file}.cnf")
    G, pos = get_graph_from_cnf(cnf_formula)
    t2 = time.time()
    list_duration = [t2-t1]
    print(f"- get graph ~ {list_duration[-1]}s")

    # Get list of colors using the selected algorithm
    t1 = time.time()
    if rep == '1':
        list_colors = dict_funct[rep](G, cnf_formula)
    else:
        list_colors = dict_funct[rep](G, True)
    t2 = time.time()    
    list_duration.append(t2-t1)
    print(f"- get list color ~ {list_duration[-1]}s")

    if list_colors:
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
        nx.draw_networkx(G, node_color=list_colors, pos=pos, labels=labels, \
                         edge_color='grey')
        t2 = time.time()    
        list_duration.append(t2-t1)
        print(f"- plot colored graph ~ {list_duration[-1]}s")

        # Maximize the plot window
        maximize()
        
        # Show the plot
        plt.show()
    
    else:
        print("-> the formula is unsatisfiable")
    
    print(f"-> duration ~ {sum(list_duration)}s")


#### main coloring

def main_graphColoring():
    """ Generate and color a random graph based on user input """
    print("----------------------------------------------------------")
    # Prompt for the coloring algorithm choice
    print("Select a coloring algorithm:")
    print("1 - CNF")
    print("2 - PYCSP")
    rep = input("Your choice: ")
    dict_funct = {'1': get_list_colors_CNF, '2': get_list_colors_CSP}
    while rep not in dict_funct:
        rep = input("Invalid choice. Please select 1 or 2: ")
    print("----------------------------------------------------------")

    # Prompt for the number of nodes and edges
    nb_nodes = int(input("Enter the number of nodes: "))
    nb_edges = int(input("Enter the number of edges: "))
    print("----------------------------------------------------------")

    # Generate a random graph with specified nodes and edges
    t1 = time.time()
    G = nx.gnm_random_graph(nb_nodes, nb_edges)
    pos = nx.random_layout(G)
    t2 = time.time()
    list_duration = [t2-t1]
    print(f"- generate random graph ~ {list_duration[-1]}s")

    # Plot the uncolored graph
    t1 = time.time()
    plt.subplot(121)
    plt.title("Uncolored Graph")
    nx.draw_networkx(G, pos=pos)
    t2 = time.time()    
    list_duration.append(t2-t1)
    print(f"- plot uncolored graph ~ {list_duration[-1]}s")

    # Get the list of colors using the selected algorithm
    t1 = time.time()
    list_colors = dict_funct[rep](G, False)
    t2 = time.time()
    list_duration.append(t2-t1)
    print(f"- get list colors: {list_duration[-1]}s")

    # Plot the colored graph if coloring is successful
    t1 = time.time() # start
    plt.subplot(122)
    if list_colors:
        plt.title("Colored Graph: 3-coloring")
        nx.draw_networkx(G, pos=pos, node_color=list_colors)
    else:
        plt.title("Colouring not found")
    t2 = time.time() # 
    list_duration.append(t2-t1)
    print(f"- plot colored graph ~ {list_duration[-1]}s")

    #
    print(f"-> duration: ~ {sum(list_duration)}s")

    # Maximize the plot window
    maximize()

    # Show the plot
    plt.show()

#### main program

def main():
    """ Main function that runs the program """
    # Display the menu
    os.system('cls' if os.name == 'nt' else 'clear')
    print("1 - Get the graph corresponding to a CNF formula and colour it")
    print("2 - Colour a graph without greedy algorithm")

    # Get the user's choice
    choice = input("Your choice: ")
    while choice not in ['1', '2']:
        choice = input("Invalid choice. Please enter a valid option: ")

    # Handle the user's choice
    dict_funct = {'1': main_cnf2graph2color, '2': main_graphColoring}
    dict_funct[choice]()

    # Remove files created by pycsp
    for f in os.listdir():
        if f.endswith(".log") or f == "main.xml":
            os.remove(f)

if __name__ == "__main__":
    main()