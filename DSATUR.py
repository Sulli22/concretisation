import networkx as nx
import matplotlib.pyplot as plt
import itertools

G = nx.Graph()
G.add_nodes_from([1,2,3,4,5,6,7,8,9])
G.add_edges_from([[2,4],[3,5],[4,6],[4,5],[5,6],[6,8],[1,7],[7,8],[7,9],[8,9]])


def DSATUR(G, colors):
    
    """Iterates over all the nodes of ``G`` in "saturation order" (also
    known as "DSATUR").

    ``G`` is a NetworkX graph. ``colors`` is a dictionary mapping nodes of
    ``G`` to colors, for those nodes that have already been colored.

    """
    distinct_colors = {v: set() for v in G}
    # Add the node color assignments given in colors to the
    # distinct colors set for each neighbor of that node
    """
    for node, color in colors.items():
        for neighbor in G[node]:
            distinct_colors[neighbor].add(color)
           
    # Check that the color assignments in colors are valid
    # i.e. no neighboring nodes have the same color
    if len(colors) >= 2:
        for node, color in colors.items():
            if color in distinct_colors[node]:
                raise nx.NetworkXError("Neighboring nodes must have different colors")
   
    """
    # If there is no colors in the dict "colors"
    if not colors:
        node = max(G, key=G.degree) # Take the node with the max degree
        yield node # Like a return but that don't stop 
        
        # Add the color 0 to the distinct colors set for each
        # neighbor of that node.If 0 nodes have been colored, simply choose the node of highest degree.
        for v in G[node]: # G[node] is for the neighbors of node between []
            distinct_colors[v].add(0)

    while len(G) != len(colors):
        # Update the distinct color sets for the neighbors.
        for node, color in colors.items():
            for neighbor in G[node]:
                distinct_colors[neighbor].add(color)
        # Compute the maximum saturation and the set of nodes that
        # achieve that saturation.
        saturation = {v: len(c) for v, c in distinct_colors.items() if v not in colors}
        # Yield the node with the highest saturation, and break ties by
        # degree.
        node = max(saturation, key=lambda v: (saturation[v], G.degree(v)))
        yield node


def greedy_color(G):

    if len(G) == 0:
        return {}

    colors = {}
    nodes = DSATUR(G,colors)
    
    for u in nodes:
        # Set to keep track of colors of neighbors
        num_colors = {colors[v] for v in G[u] if v in colors}
        
        # Find the first unused color.
        for color in itertools.count():
            if color not in num_colors:
                break
        # Assign the new color to the current node.
        colors[u] = color
    return colors

dict_coloring_int = greedy_color(G)

# nx.draw(G,with_labels=True)
# plt.show()
