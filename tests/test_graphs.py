from src.fair_orientation.graphs import *

def test_get_strong_components():
    G = DirectedGraph()
    vertices = [1,2,3,4,5,6,7]
    arcs = [(1,2), (2,3), (3,4), (4,1),
            (4,5), (5,6), (6,5)]
    for vertex in vertices:
        G.add_vertex(vertex)
    for arc in arcs:
        G.add_edge(*arc)

    sorted_strong_components = [sorted(component) for component in G.get_strong_components()]
    assert len(sorted_strong_components) == 3
    assert [1,2,3,4] in sorted_strong_components
    assert [5,6] in sorted_strong_components
    assert [7] in sorted_strong_components

def test_get_negative_components():
    # Test 1:
    #   G looks like the following.
    #   1 - 2 - 4
    #     \ |   |
    #       3 - 5
    # The edges on the 3-cycle (1,2,3) and the edge (4,5) are the only negative edges,
    # so there should be only two negative components, namely, [1,2,3] and [4,5].

    G = GraphicalInstance([1,2,3,4,5],
                          [(1,2), (2,3), (3,1),
                           (2,4), (3,5),
                           (4,5)])
    G.set_util((1,2), -1, -2)
    G.set_util((2,3), -1, -1)
    G.set_util((3,1), -2, -5)
    G.set_util((4,5), -1, -3)
    G.set_util((2,4), 0, -1)
    G.set_util((3,5), 0, 0)

    negative_components = G.get_negative_components()
    negative_components.sort(key=len) # Sort by size
    negative_components = [sorted(K) for K in negative_components] # Sort each component in non-decreasing order

    assert len(negative_components) == 2
    assert [len(K) for K in negative_components] == [2,3]
    assert [4,5] in negative_components
    assert [1,2,3] in negative_components