<img src="./site/img/logo.png" width="40px">

# Boolean formulas and graph coloring

The primary objective of this project is to show the equivalence between satisfiability problems in propositional logic (SAT) and the graph coloring problem. In other words, our project illustrates the correspondence between the complexities of these two NP-complete problems.

## Usage

Our program is interactive and can be used in console mode, simply by interpreting main.py via any python interpreter.

In fact, via a rudimentary formatting, the user is offered various choices, the first of which opposes :
```
1 - Get the graph corresponding to a CNF formula and colour it
2 - Colour a graph without greedy algorithm
```

If the first is chosen, the user selects the coloring algorithm he or she wants : 
```
1 - DSATUR
2 - CNF
3 - CSP
```

The list of CNF files is then displayed, and the user is asked to enter the desired file. The graph corresponding to the formula is then generated, the coloring method applied and the colored graph displayed (if the formula is satisfiable). 

#### Example

<img src="./site/img/exemple2.png" width="100%">

In the other case, the user chooses the non-glutton coloring algorithm he wants :
```
1 - CNF
2 - CSP
```

Next, the user is asked to enter a number of nodes and edges, which is then followed by the generation of a graph corresponding to these characteristics, the application of the coloring method and the display of the generated graph without coloring and its colored version (if it is 3-colorable). 

#### Example

<img src="./site/img/exemple3.png" width="100%">
(V0 ∨ R0 ∨ B0) ∧ (-V0 ∨ -R0) ∧ (-V0 ∨ -B0) ∧ (-R0 ∨ -B0) ∧ (V1 ∨ R1 ∨ B1) ∧ (-V1 ∨ -R1) ∧ (-V1 ∨ -B1) ∧ (-R1 ∨ -B1) ∧ (V2 ∨ R2 ∨ B2) ∧ (-V2 ∨ -R2) ∧ (-V2 ∨ -B2) ∧ (-R2 ∨ -B2) ∧ (V3 ∨ R3 ∨ B3) ∧ (-V3 ∨ -R3) ∧ (-V3 ∨ -B3) ∧ (-R3 ∨ -B3) ∧ (V4 ∨ R4 ∨ B4) ∧ (-V4 ∨ -R4) ∧ (-V4 ∨ -B4) ∧ (-R4 ∨ -B4) ∧ (-V0 ∨ -V1) ∧ (-R0 ∨ -R1) ∧ (-B0 ∨ -B1) ∧ (-V0 ∨ -V2) ∧ (-R0 ∨ -R2) ∧ (-B0 ∨ -B2) ∧ (-V1 ∨ -V3) ∧ (-R1 ∨ -R3) ∧ (-B1 ∨ -B3) ∧ (-V1 ∨ -V2) ∧ (-R1 ∨ -R2) ∧ (-B1 ∨ -B2) ∧ (-V2 ∨ -V4) ∧ (-R2 ∨ -R4) ∧ (-B2 ∨ -B4) ∧ (-V3 ∨ -V4) ∧ (-R3 ∨ -R4) ∧ (-B3 ∨ -B4) 

We can also specify that during these various executions we display their approximate execution time as well as the total execution time at the end of them.

## Libraries used

- [Networkx](https://networkx.org/)
- [Matplotlib.pyplot](https://matplotlib.org/3.5.3/api/_as_gen/matplotlib.pyplot.html)
- [Pysat](https://pysathq.github.io/docs/html/)
- [PyCSP](https://www.pycsp.org/)

## Documentation

### main.py

#### main():
```
Main function that runs the program
```

#### main_graphColoring():
```
Generates and color a random graph based on user input
```

#### main_cnf2graph2color():
```
Generates the graph corresponding to the cnf formula
```

#### maximize():
```
Maximizes the plot window
```

### cnfToGraph.py

#### get_graph_from_cnf(cnf_formula):
```
Returns the graph corresponding to the cnf formula

Parameters
cnf_formula: pysat.formula CNF()
    list of 3-uplet of literals (int), each corresonding to a clause
    
Returns
G: Networkx graph
    graph that contains variables and clauses
pos: dict
    dict that associates nodes to their position
```

#### add_clause(G, pos, nb_clauses, clause_nb, x1, x2, x3):
```
Adds a disjunction clause with input variables x1, x2, x3 to the graph 

Parameters
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
```

#### get_graph_base(pos, nb_var):
``` 
Returns a graph that will be used to implement the clauses

Parameters
nb_var: int
    number of variables required
pos: dict
    dict that associates nodes to their position
    
Returns
G: Networkx graph
    graph that contains ``nb_vars`` 3-cliques and one more for our True, False and Neutral references
```

### graphColoring.py

#### get_list_colors_CSP(G, relabel_need):
```
Returns a list of colors in the order of the graph nodes, respecting the coloring rules

Parameters
G: Networkx graph
    graph that we want to color
relabel_need: bool
    does the G have to be copy with new labels
        
Returns
unamed: list or bool
    list of color (str) in order of G nodes or False if no coloring
```

#### get_list_colors_CNF(G, relabel_need):
```
Returns a list of colors in the order of the graph nodes, respecting the coloring rules

Parameters
G: Networkx graph
    graph we want to color
relabel_need: bool
    does the G have to be copy with new labels
        
Returns
unamed: list or bool
    list of color (str) in order of G nodes or False if no coloring
```

#### get_cnf_from_graph(G):
```
Returns a cnf formula that is satisfiable if the graph is colorable

Parameters
G: Networkx graph
    graph we want to color
        
Returns
cnf: pysat.formula.CNF
    cnf formula
```

#### get_list_colors_DSATUR(G, cnf_formula):
```
Returns a list of colors in the order of the graph nodes, respecting the coloring rules
    
Parameters
G: Networkx graph
    graph that we want to color
colors: dict
    dict associates nodes of G to colors, for those nodes that have already been colored
        
Returns
unamed: list or bool
    list of color (str) in order of G nodes or False if no coloring
```

#### DSATUR(G, colors):
```
Iterates over all the nodes of G in "saturation order" ("DSATUR")

Parameters
G: NetworkX graph
    graph we want to have the saturation order
colors: dict
    dict associates nodes of G to colors, for those nodes that have already been colored

Returns
unamed: generator object
```

#### relabel_nodes(G):
```
Relabels the nodes of a graph with integer labels

Parameters
G : Networkx graph
    The graph to be relabeled

Returns
G_copy : Networkx graph
    A copy of the graph with nodes relabeled with integers
```

## Authors

- [Masian Huneau](https://www.github.com/masianH)
- [Sullivan Driant](https://www.github.com/Sulli22)


## Support

For support, email sullivan.driant@etud.univ-angers.fr or masian.huneau@etud.univ-angers.fr

