# This is an implementation of the FindPDVertexCover algorithm (Algorithm 1) from the paper "Polynomial-Time Algorithms
# for Fair Orientations of Chores" due to Hsu and King.
#
# Input:
#     An undirected graph H, a set P = [P1, P2, ..., Pk] of pairwise disjoint subsets
#     of vertices of H, and a subset D of vertices of H.
#
# Problem:
#     Does there exist a (P, D)-vertex cover C of H? Specifically, does there exist a
#     subset C of vertices of H satisfying all the following conditions:
#         - each edge of H is incident to at least one vertex of C
#         - for each set Pi in P, the intersection between C and Pi has size <= 1
#         - C does not intersect D
#
# Output: A (P,D)-vertex cover of C if it exists, and False if not.

from .sat import solve_2SAT
from .graphs import Graph
from itertools import combinations

def find_PD_vertex_cover(H, P, D):
    """
    Finds a (P, D)-vertex cover of H if one exists. Otherwise, returns False.

    :param H: A Graph object from graphs.py
    :param P: A list of lists (i.e. P = [P1, P2, ..., Pk] where each Pi is a list),
              Each Pi represents a subset of vertices of H.
    :param D: A list representing a subset of vertices of H.

    :return: A (P, D)-vertex cover C of H if one exists, or False if not. Here, C is
             represented as a list of vertices of H.
    """

    boolean_formula = []

    # Type 1 clauses
    for edge in H.get_edges():
        boolean_formula.append(edge)

    # Type 2 clauses
    for Pi in P:
        for pair in combinations(Pi, 2):
            boolean_formula.append((-pair[0], -pair[1]))

    # Type 3 clauses
    for i in D:
        boolean_formula.append((-i,))
    truth_assignment = solve_2SAT(boolean_formula)

    if not truth_assignment:
        return False
    else:
        return [v for v in H.get_vertices() if truth_assignment[v] == True]

def is_PD_vertex_cover(C, H, P, D):
    """Verifies that C is a (P, D)-vertex cover of H."""
    # Condition 1
    for edge in H.get_edges():
        if len(set(C).intersection(set(edge))) == 0:
            return False
    # Condition 2
    for Pi in P:
        if len(set(C).intersection(set(Pi))) > 1:
            return False
    # Condition 3
    if len(set(C).intersection(set(D))) > 0:
        return False
    return True
