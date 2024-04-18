##### packages
import networkx as nx
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 8))

#### Functions

def get_base_graph(nb_var: int):  # -> nx.Graph
    G = nx.Graph()
    G.add_edges_from([('V', 'F'), ('N', 'F'), ('V', 'N')])
    for i in range(1, nb_var+1):
        G.add_edges_from([(str(i), str(-i)), (str(i), 'N'), (str(-i), 'N')])
    return G

def add_clause(G, clause_nb: int, x1: str, x2: str, x3: str) -> None:
    N_x1 = f"N_{x1}_{clause_nb}"; N_x2 = f"N_{x2}_{clause_nb}"
    N_x3 = f"N_{x2}_{clause_nb}"; dij_x1x2 = f"dij_{x1}{x2}_{clause_nb}"
    N_x1x2 = f"N_{x1}{x2}_{clause_nb}"; dij_x1x2x3 = f"dij_{x1}{x2}{x3}_{clause_nb}"
    G.add_edges_from([(x1, N_x1), (x2, N_x2), (N_x1, N_x2), (N_x1, dij_x1x2), (N_x2, dij_x1x2),
                      (dij_x1x2, N_x1x2), (x3, N_x3), (N_x1x2, N_x3), (N_x1x2, dij_x1x2x3),
                      (N_x3, dij_x1x2x3), (dij_x1x2x3, 'F'), (dij_x1x2x3, 'N')])

def get_graph_from_cnf(list_cnf: list, nb_vars: int): # -> nx.Graph
    G = get_base_graph(nb_vars)
    for clause_nb in range(len(list_cnf)):
        add_clause(G, clause_nb+1, list_cnf[clause_nb][0], 
                   list_cnf[clause_nb][1], list_cnf[clause_nb][2])
    return G

#### Coloring

def get_dict_links(dict_int: dict) -> dict:
    d = {}
    int_F = dict_int['F']; int_V = dict_int['V']; int_N = dict_int['N']
    d[int_F] = 'red'; d[int_V] = 'green'; d[int_N] = 'blue'
    return d
    
def get_dict_colors(dict_colors_int: dict, dict_links: dict) -> dict:
    return {node: dict_links[dict_colors_int[node]] for node in dict_colors_int.keys()}

def get_list_colors(dict_colors: dict) -> list:
    return [dict_colors[node] for node in G.nodes()]

def is_a_var(x: str) -> bool:
    return x[0] not in ['V', 'F', 'N', 'd', '-']

def get_dict_bin_vars(dict_colors: dict) -> dict:
    return {node: dict_colors[node] == 'green' for node in dict_colors.keys() if is_a_var(node)}

def graph_3_coloring(G, nb_vars: int, with_fig=True) -> list:
    dict_coloring_int = nx.greedy_color(G, 'DSATUR')
    if 3 in dict_coloring_int.values():
        return [False, {}]
    dict_links = get_dict_links(dict_coloring_int)
    dict_colors = get_dict_colors(dict_coloring_int, dict_links)
    res_list = [True]
    res_list.append(get_dict_bin_vars(dict_colors))
    if not with_fig:
        return res_list
    list_colors = get_list_colors(dict_colors)
    nx.draw_networkx(G, node_color = list_colors)   # Draw graph
    return res_list


#### Main Program

list_cnf_formula = [('1', '2', '3'),
                    ('1', '-2', '-3')]
nb_vars = 3

G = get_graph_from_cnf(list_cnf_formula, nb_vars)
solv_list = graph_3_coloring(G, nb_vars)
print(solv_list)

if solv_list[0]:
    plt.show()                                      # ShowFigure