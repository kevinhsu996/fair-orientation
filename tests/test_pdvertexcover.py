from src.fair_orientation.pdvertexcover import *

def test_is_PD_vertex_cover():
    H = Graph([1, 2, 3, 4, 5], [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)])
    P = [[1, 2], [3, 4]]
    D = [1]
    C = [2, 4, 5]
    assert is_PD_vertex_cover(C, H, P, D)

    H = Graph([1, 2, 3, 4, 5], [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)])
    P = [[1, 2], [3, 4]]
    D = [1]
    C = [1, 4, 5]
    assert not is_PD_vertex_cover(C, H, P, D)

    H = Graph([1, 2, 3, 4, 5], [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)])
    P = [[1, 2], [3, 4]]
    D = [1]
    C = [2, 5]
    assert not is_PD_vertex_cover(C, H, P, D)

    H = Graph([1, 2, 3, 4, 5], [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)])
    P = [[1, 2], [3, 4]]
    D = [1]
    C = [2, 3, 4, 5]
    assert not is_PD_vertex_cover(C, H, P, D)

def test_find_PD_vertex_cover():
    H = Graph([1, 2, 3, 4], [(1, 2), (2, 3), (3, 4), (4, 1)])
    P = [[1,2], [3,4]]
    D = [1]
    assert is_PD_vertex_cover(find_PD_vertex_cover(H, P, D), H, P, D)

    H = Graph([1, 2, 3, 4], [(1, 2), (2, 3), (3, 4), (4, 1)])
    P = [[1, 2], [3, 4]]
    D = [1, 2]
    assert not find_PD_vertex_cover(H, P, D)

    H = Graph([1, 2, 3, 4], [(1, 2), (2, 3), (3, 4), (4, 1)])
    P = [[1, 2], [3, 4]]
    D = [1, 3]
    assert sorted(find_PD_vertex_cover(H, P, D)) == [2, 4]

    H = Graph([1, 2, 3, 4, 5], [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)])
    P = [[1, 2], [3, 4]]
    D = [5]
    assert find_PD_vertex_cover(H, P, D) == False

    H = Graph([1, 2, 3, 4], [])
    P = []
    D = [1, 2, 3, 4]
    assert find_PD_vertex_cover(H, P, D) != False