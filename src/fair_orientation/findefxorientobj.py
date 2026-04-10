# This is an implementation of the FindEFXOrientObj algorithm (Algorithm 2) from the paper "Polynomial-Time Algorithms
# for Fair Orientations of Chores" due to Hsu and King.
#
# Input:
#     An objective instance (G, u) of the fair chores division problem on graphs. Here,
#     G is a graph and u is a set of utility functions associated with the agents represented
#     by the vertices of G.
#
# Problem:
#     Does there exist an EFX orientation of G?
#
# Output:
#     An EFX orientation of G if it exists, and False if not.

from collections import deque

from .graphs import GraphicalInstance, Orientation, Graph
from .pdvertexcover import find_PD_vertex_cover

def find_EFX_orient_obj(G):
    """
    Finds an EFX orientation of the objective instance (G, u) if it exists.

    :param G: An objective graphical instance represented by a GraphicalInstance object from graphs.py.
    :return: An EFX orientation O of G if it exists, and False otherwise.
    """
    negative_components = G.get_negative_components()

    for K in negative_components:
        if G.number_of_negative_edges(K) > len(K):
            return False

    # Construct the instance of PDVertexCover.
    H = Graph(G.get_vertices(), [])
    for e in G.get_edges():
        # Only add e to H if e is a dummy edge with zero utility to both endpoints.
        if not G.is_negative_edge(e):
            H.add_edge(e)
    P = []
    D = []
    for K in negative_components:
        if G.number_of_negative_edges(K) == len(K)-1:
            P.append(K)
        else: #G.number_of_negative_edges(K) == len(K)
            # Add the vertices of K to D
            D = D + K

    C = find_PD_vertex_cover(H, P, D)

    if C == False:
        return False

    # Construct the EFX orientation of G using C.
    # First, orient the dummy edges.
    orientation = Orientation(G)
    for e in H.get_edges():
        if e[0] in C:
            orientation.orient(e, e[0])
        else:
            orientation.orient(e, e[1])

    # Finally, orient the negative edges according to the method described in Observation 3.
    G_negative = G.get_negative_subinstance()
    G_negative_orientation = Orientation(G_negative)
    G_negative_orientation._orient_using_observation_3()

    for e in G_negative_orientation.get_edges():
        orientation.orient(e, G_negative_orientation.get_orientation(e))

    return orientation

