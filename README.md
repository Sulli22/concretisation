<img src="./site/img/logo.png" width="40px">

# Boolean formulas and graph coloring

The primary objective of this project is to show the equivalence between satisfiability problems in propositional logic (SAT) and the graph coloring problem. In other words, our project illustrates the correspondence between the complexities of these two NP-complete problems.


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
<div style="background-color='ffffff';">
Returns the graph corresponding to the cnf formula

Parameters
cnf_formula: pysat.formula CNF()
    list of 3-uplet of literals (int), each corresonding to a clause
    
Returns
G: Networkx graph
    graph that contains variables and clauses
pos: dict
    dict that associates nodes to their position
</div>

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

