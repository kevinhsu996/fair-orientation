from src.fair_orientation.sat import *

def test_solve_2sat():
    F = [[1, 2], [2, -3], [-1, 4], [1]]
    A = solve_2SAT(F)
    assert is_satisfying_assignment(F, A)

    F = [[1], [-1]]
    A = solve_2SAT(F)
    assert not A

    F = [[1, -1]]
    A = solve_2SAT(F)
    assert is_satisfying_assignment(F, A)

    F = [[1, -1], [1], [-1]]
    A = solve_2SAT(F)
    assert not A

    F = [[1, 2], [-1, -2], [1], [2]]
    A = solve_2SAT(F)
    assert not A

    F = [[1, 2], [-1, -2], [1], [-2]]
    A = solve_2SAT(F)
    assert is_satisfying_assignment(F, A)


def test_is_satisfying_assignment():
    F = [[1, 2], [3]]
    A = [None, True, True, False]
    assert not is_satisfying_assignment(F, A)

    F = [[1, 2], [3]]
    A = [None, True, False, True]
    assert is_satisfying_assignment(F, A)

    F = [[1, 2], [-3, -4, 5], [6]]
    A = [None, True, False, True, False, False, True]
    assert is_satisfying_assignment(F, A)

    F = [[1, 2], [-3, -4], [5]]
    A = [None, False, True, True, True, True]
    assert not is_satisfying_assignment(F, A)
