#### imports

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from pysat.formula import CNF
from pysat.solvers import Solver

#### cnf to graph

def get_cnf_from_file(file: str):
    """
    
    """
    try:
        return CNF(from_file = file + ".cnf")
    except:
        file = input("file don't find, file name (without .cnf): ")
        get_cnf_from_file(file + ".cnf")

def main_cnf2graph_DASTUR():
    """

    """
    formula_file = input("file name (without .cnf): ")
    cnf_formula = get_cnf_from_file(formula_file) 

#### cnf to graph pysat solver

def main_cnf2graph_SOLVER():
    """
    
    """
    formula_file = input("file name (without .cnf): ")
    cnf_formula = get_cnf_from_file(formula_file)

#### cnf to graph pyscp

def main_cnf2graph_PYCSP():
    """
    
    """
    formula_file = input("file name (without .cnf): ")
    cnf_formula = get_cnf_from_file(formula_file)

#### graph coloring with solver sat

def main_graph_coloring_with_solver():
    """

    """

#### main program


run = True

while run:
    print("1 - cnf to graph dsatur")
    print("2 - cnf to graph to cnf")
    print("3 - cnf to graph pycsp")
    print("4 - graph to cnf")
    print("5 - quit")
    list_choices = ['1', '2', '3', '4', '5']
    rep = input("choice : ")
    while rep not in list_choices:
        rep = input("wrong, try again : ")
    if rep == '5':
        run = False
    

"""
wm = plt.get_current_fig_manager()      # > plt fullscreen
wm.window.state('zoomed')               #/
"""