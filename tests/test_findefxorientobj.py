from src.fair_orientation.findefxorientobj import *

def test_find_EFX_orient_obj():

    # Test 1: G is a 4-cycle with a chord. The edges on the 4-cycle have -1 util to both endpoints, and the
    # chord has zero utility to both endpoints. In this case, there is no EFX orientation because the 4-cycle
    # forces each vertex to have at least one incoming negative edge. After orienting the chord, there must be
    # a vertex with both an incoming negative edge and an incoming edge of zero utility. The orientation is not
    # EFX for such a vertex.

    G = GraphicalInstance([1, 2, 3, 4],
                          [(1,2),(2,3),(3,4),(4,1),(1,3)])
    G.set_util((1,2), -1,-1)
    G.set_util((2,3), -1, -1)
    G.set_util((3,4), -1, -1)
    G.set_util((4,1), -1, -1)
    G.set_util((1,3),0,0)

    assert G.is_negative_edge((1,2))
    assert G.is_objective_edge((1,2))
    assert G.get_util(1, (1,2)) == -1
    assert G.get_util(3, (1,2)) == 0
    assert(len(G.get_negative_components())) == 1
    assert find_EFX_orient_obj(G) == False

    # Test 2: G is a 4-cycle. The edges on the 4-cycle have -1 util to both endpoints.
    # In this case, there is an EFX orientation - just orient G as a directed cycle.

    G = GraphicalInstance([1, 2, 3, 4],
                          [(1, 2), (2, 3), (3, 4), (4, 1)])
    G.set_util((1, 2), -1, -1)
    G.set_util((2, 3), -1, -1)
    G.set_util((3, 4), -1, -1)
    G.set_util((4, 1), -1, -1)

    assert (len(G.get_negative_components())) == 1
    assert find_EFX_orient_obj(G) != False

    # Test 3: G looks like the following.
    # 2 - 1
    # |   |
    # 3 - 4 - 5 - 6
    # where the edge (3,5) has zero utility to both endpoints, and every other edge has -1 utility to both endpoints.
    # In this case, there is an EFX orientation.

    G = GraphicalInstance([1, 2, 3, 4, 5, 6],
                          [(1, 2), (2, 3), (3, 4), (4, 1), (4, 5), (5, 6)])
    G.set_util((1, 2), -1, -1)
    G.set_util((2, 3), -1, -1)
    G.set_util((3, 4), -1, -1)
    G.set_util((4, 1), -1, -1)
    G.set_util((4, 5), 0, 0)
    G.set_util((5, 6), -1, -1)

    assert find_EFX_orient_obj(G) != False

    # Test 3: G looks like the following.
    # 2 --- 1
    # |   / |
    # |  5  |
    # | /   |
    # 3 --- 4
    # where the edges (1,5) and (3,5) have zero utility to both endpoints, and every other edge has -1 utility to
    # both endpoints. In this case, there is an EFX orientation (two edges directed toward 5, and the rest of the
    # edges directed clockwise).

    G = GraphicalInstance([1, 2, 3, 4, 5],
                          [(1, 2), (2, 3), (3, 4), (4, 1), (1, 5), (5, 3)])
    G.set_util((1, 2), -1, -1)
    G.set_util((2, 3), -1, -1)
    G.set_util((3, 4), -1, -1)
    G.set_util((4, 1), -1, -1)
    G.set_util((3, 5), 0, 0)
    G.set_util((1, 5), 0, 0)

    G_orientation = find_EFX_orient_obj(G)

    assert G_orientation != False
    assert G_orientation.get_orientation((3,5)) == 5
    assert G_orientation.get_orientation((1,5)) == 5
