from src.fair_orientation.findfairorientation import *

def test_find_EFX_orientation():
    # Test 1: This is the test in the README.md. There is no EFX orientation.
    G = GraphicalInstance([1, 2, 3, 4, 5],
                          [(1, 2), (2, 3), (3, 4), (4, 1), (1, 5), (5, 3)])
    G.set_util((1, 2), -1, -1)
    G.set_util((2, 3), -1, -1)
    G.set_util((3, 4), -1, -1)
    G.set_util((4, 1), -1, -1)
    G.set_util((3, 5), 0, -1)  # i.e. the edge {3,5} has utility 0 to 3 and utility -1 to 5
    G.set_util((1, 5), 0, -1)

    EFX_orientation = find_EFX_orientation(G)
    assert EFX_orientation == False

    # Test 2: G is a 4-cycle with a chord. The edges on the 4-cycle have -1 util to both endpoints, and the
    # chord has negative utility to one endpoint and zero utility to the other.
    # In this case, G has no EFX orientations.
    G = GraphicalInstance([1, 2, 3, 4],\
                          [(1,2),(2,3),(3,4),(4,1),(1,3)])
    G.set_util((1,2), -1,-1)
    G.set_util((2,3), -1, -1)
    G.set_util((3,4), -1, -1)
    G.set_util((4,1), -1, -1)
    G.set_util((1,3),-1,0)

    assert G.is_negative_edge((1,2))
    assert G.is_objective_edge((1,2))
    assert G.get_util(1, (1,2)) == -1
    assert G.get_util(3, (1,2)) == 0

    EFX_orientation = find_EFX_orientation(G)
    assert EFX_orientation == False

    # Test 3: G looks like the following.
    # 2 --- 1
    # |   / |
    # |  5  |
    # | /   |
    # 3 --- 4
    # where every edge has negative utility to both endpoints, except for the two edges incident with 5.
    # These two edges have zero utility to 5 but -1 utility to the other endpoints (namely, 1 and 3).
    # In this case, G has an EFX orientation (orient the two edges toward 5, and then the rest clockwise).
    G = GraphicalInstance([1, 2, 3, 4, 5],
                          [(1, 2), (2, 3), (3, 4), (4, 1), (1, 5), (5, 3)])
    G.set_util((1, 2), -5, -1)
    G.set_util((2, 3), -1, -10)
    G.set_util((3, 4), -1, -3)
    G.set_util((4, 1), -4, -1)
    G.set_util((3, 5), -1, 0)
    G.set_util((1, 5), -1, 0)

    EFX_orientation = find_EFX_orientation(G)
    assert EFX_orientation.is_EFX()
    assert EFX_orientation.get_orientation((3, 5)) == 5
    assert EFX_orientation.get_orientation((1, 5)) == 5

    # Test 4: G is a 3-cycle with vertices 1, 2, and 3 together with a self-loop at vertex 1.
    # The self-loop has zero utility and the edges on the 3-cycle have -1 utility to one endpoint and 0 to the other.
    # In this case, there is an EFX orientation.

    G = GraphicalInstance([1, 2, 3],
                          [(1, 2), (2, 3), (3, 1), (1, 1)])
    G.set_util((1,2), 0, -1)
    G.set_util((2, 3), 0, -1)
    G.set_util((3, 1), 0, -1)
    G.set_util((1, 1), 0, 0)

    EFX_orientation = find_EFX_orientation(G)
    assert EFX_orientation.is_EFX()

    # Test 5: G is a 3-cycle with vertices 1, 2, and 3 together with a self-loop at vertex 1.
    # All edges have -1 utility to both endpoints. In this case, G has no EFX orientation.

    G = GraphicalInstance([1, 2, 3],
                          [(1, 2), (2, 3), (3, 1), (1, 1)])
    G.set_util((1, 2), -1, -1)
    G.set_util((2, 3), -1, -1)
    G.set_util((3, 1), -1, -1)
    G.set_util((1, 1), -1, -1)

    EFX_orientation = find_EFX_orientation(G)
    assert EFX_orientation == False

def test_find_EF1_orientation():
    # Test 1: This is the test in the README.md
    G = GraphicalInstance([1, 2, 3, 4, 5],
                          [(1, 2), (2, 3), (3, 4), (4, 1), (1, 5), (5, 3)])
    G.set_util((1, 2), -1, -1)
    G.set_util((2, 3), -1, -1)
    G.set_util((3, 4), -1, -1)
    G.set_util((4, 1), -1, -1)
    G.set_util((3, 5), 0, -1)  # i.e. the edge {3,5} has utility 0 to 3 and utility -1 to 5
    G.set_util((1, 5), 0, -1)

    EF1_orientation = find_EF1_orientation(G)
    assert EF1_orientation != False

    # Test 2: G is a 4-cycle with a chord. The edges on the 4-cycle have -1 util to both endpoints, and the
    # chord has negative utility to one endpoint and zero utility to the other.
    # In this case, G has an EF1 orientation.
    G = GraphicalInstance([1, 2, 3, 4],\
                          [(1,2),(2,3),(3,4),(4,1),(1,3)])
    G.set_util((1,2), -1,-1)
    G.set_util((2,3), -1, -1)
    G.set_util((3,4), -1, -1)
    G.set_util((4,1), -1, -1)
    G.set_util((1,3),-1,0)

    EF1_orientation = find_EF1_orientation(G)
    assert EF1_orientation != False
    assert EF1_orientation.is_EF1()

    # Test 3: G looks like the following.
    # 2 --- 1
    # |   / |
    # |  5  |
    # | /   |
    # 3 --- 4
    # where every edge has negative utility to both endpoints, except for the two edges incident with 5.
    # These two edges have zero utility to 5 but -1 utility to the other endpoints (namely, 1 and 3).
    # In this case, G has an EF1 orientation (orient the two edges toward 5, and then the rest clockwise).
    G = GraphicalInstance([1, 2, 3, 4, 5],
                          [(1, 2), (2, 3), (3, 4), (4, 1), (1, 5), (5, 3)])
    G.set_util((1, 2), -5, -1)
    G.set_util((2, 3), -1, -10)
    G.set_util((3, 4), -1, -3)
    G.set_util((4, 1), -4, -1)
    G.set_util((3, 5), -1, 0)
    G.set_util((1, 5), -1, 0)

    EF1_orientation = find_EF1_orientation(G)
    assert EF1_orientation.is_EF1()

    # Test 4: G is a 3-cycle with vertices 1, 2, and 3 together with a self-loop at vertex 1.
    # The self-loop has zero utility and the edges on the 3-cycle have -1 utility to one endpoint and 0 to the other.
    # In this case, there is an EFX orientation.

    G = GraphicalInstance([1, 2, 3],
                          [(1, 2), (2, 3), (3, 1), (1, 1)])
    G.set_util((1,2), 0, -1)
    G.set_util((2, 3), 0, -1)
    G.set_util((3, 1), 0, -1)
    G.set_util((1, 1), 0, 0)

    EF1_orientation = find_EF1_orientation(G)
    assert EF1_orientation.is_EF1()

    # Test 5: G is a 3-cycle with vertices 1, 2, and 3 together with a self-loop at vertex 1.
    # All edges have -1 utility to both endpoints. In this case, G has no EF1 orientation.

    G = GraphicalInstance([1, 2, 3],
                          [(1, 2), (2, 3), (3, 1), (1, 1)])
    G.set_util((1, 2), -1, -1)
    G.set_util((2, 3), -1, -1)
    G.set_util((3, 1), -1, -1)
    G.set_util((1, 1), -1, -1)

    EF1_orientation = find_EF1_orientation(G)
    assert EF1_orientation == False
