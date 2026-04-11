# This is an implementation of the two main algorithms from the paper Polynomial-Time Algorithms for Fair Orientations
# of Chores" due to Hsu and King, namely
#
#   1) find_EF1_orientation for finding EF1 orientations (informally described in Section 3 of the paper)
#   2) find_EFX_orientation for finding EFX orientations (Algorithm 3 of the paper)
#
# The behavior of these two algorithms are similar and are described below.
#
# Input:
#     An instance (G, u) of the fair chores division problem on graphs.
#     Here, G is a graph and u is a set of utility functions associated with the agents represented by the
#     vertices of G.
#
# Problem:
#     Does there exist an EF1 (or EFX) orientation of G?
#
# Output:
#     An EF1 (or EFX) orientation of G if it exists, and False if not.

from .findefxorientobj import find_EFX_orient_obj
from .graphs import GraphicalInstance, Orientation, Graph

def find_EF1_orientation(G):
    """
    Finds an EF1 orientation of the instance (G, u) if it exists.

    :param G: A graphical instance represented by a GraphicalInstance object from graphs.py.
    :return: An EF1 orientation O of G if it exists, and False otherwise.
    """
    # Class to hold the oriented edges
    G_orientation = Orientation(G)

    # Find the subgraph of G that contains only the negative edges of G.
    G_negative = Graph(G.get_vertices(), [e for e in G.get_edges() if G.is_negative_edge(e)])

    # Find the subgraph of G induced by its negative edges.
    negative_components = G_negative.get_components()

    # If any negative component has too many edges, then the pigeonhole precludes the existence
    # of an EF1 orientation.
    for K in negative_components:
        if G.number_of_negative_edges(K) > len(K):
            return False

    # Otherwise, we orient each non-negative edge e toward an endpoint i such that util(i, e)=0,
    # and the negative edges according to Observation 3 of the paper.
    for e in G_orientation.get_edges():
        i = e[0]
        j = e[1]
        if G_orientation.get_util(i, e) == 0:
            G_orientation.orient(e, i)
        elif G_orientation.get_util(j, e) == 0:
            G_orientation.orient(e, j)

    G_negative = G.get_negative_subinstance()
    G_negative_orientation = Orientation(G_negative)
    G_negative_orientation._orient_using_observation_3()

    for e in G_negative_orientation.get_edges():
        G_orientation.orient(e, G_negative_orientation.get_orientation(e))

    return G_orientation

def find_EFX_orientation(G):
    """
    Finds an EFX orientation of the instance (G, u) if it exists.

    :param G: A graphical instance represented by a GraphicalInstance object from graphs.py.
    :return: An EFX orientation O of G if it exists, and False otherwise.
    """

    # Construct the objective instance Go by subdividing non-objective edges
    Go = GraphicalInstance(G.get_vertices(), [])
    edge_subdivisions = {} # To keep track of subdivided edges.
    for e in G.get_edges():
        if G.is_objective_edge(e):
            Go.add_edge(e)
            Go.set_util(e, G.get_util(e[0], e), G.get_util(e[1], e))
        else:
            # Subdivide the non-objective edges.
            i, j, k = e[0], e[1], Go.get_next_vertex_label()
            eik = (i, k)
            ejk = (j, k)

            Go.add_vertex(k)

            Go.add_edge(eik)
            Go.set_util(eik, G.get_util(i, e), G.get_util(i, e))

            Go.add_edge(ejk)
            Go.set_util(ejk, G.get_util(j, e), G.get_util(j, e))

            # We store the subdivided edges to keep track of them. Because we don't need to do anything with ejk
            # later in the algorithm, we only store eik.
            edge_subdivisions[e] = eik

    Go_orientation = find_EFX_orient_obj(Go)

    if Go_orientation == False:
        return False

    # Generate the orientation of G using the orientation of Go
    G_orientation = Orientation(G)
    for e in G.get_edges():
        if G.is_objective_edge(e):
            # Objective edges were not subdivided, and the algorithm orients them as in Go_orientation.
            G_orientation.orient(e, Go_orientation.get_orientation(e))
        else:
            # Each non-objective edge (i,j) was subdivided into two edges (i,k) and (j,k) where k is a new vertex.
            # The algorithm orients (i,j) in the same direction as (i,k), i.e.
            #     1) If (i,k) is directed toward i, then orient (i,j) toward i.
            #     2) If (i,k) is directed toward k, then orient (i,j) toward j.
            eik = edge_subdivisions[e]
            i = e[0]
            k = eik[0] if eik[1]==i else eik[1]

            if Go_orientation.get_orientation(eik) == i:
                G_orientation.orient(e, i)
            else:
                G_orientation.orient(e, j)

    return G_orientation
