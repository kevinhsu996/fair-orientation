# This is an implementation of the linear-time 2SAT algorithm due to Aspvall et al. in their paper "A Linear-Time
# Algorithm for Testing the Truth of Certain Quantified Boolean Formulas". We briefly describe the 2SAT problem and
# give an example usage of this module.
#
# Instance:
#   A Boolean formula F in conjunctive normal form (CNF) in which each clause consists of at most 2 literals,
#   using Boolean variables x1, x2, ..., xn.
#
# Problem:
#   Given F, the 2SAT problem asks whether it is possible to assign truth values to each Boolean variable used
#   by F, so that the formula F evaluates to TRUE. Note: Such a truth assignment is called a "satisfying truth
#   assignment". A satisfying truth assignment is not necessarily unique - it is possible for a Boolean formula to
#   have multiple satisfying truth assignments.
#
# Example:
#   Suppose F is the Boolean formula (x1 OR x2) AND (x2 OR (not x3)) AND ((not x1) OR x4) AND (x1), where x1, x2, x3,
#   and x4 are Boolean variables. In this case, the truth assignment x1 = x2 = x3 = x4 = TRUE is a satisfying truth
#   assignment, because it causes F to evaluate to TRUE. So, the algorithm successfully finds a satisfying truth
#   assignment and outputs it. In the case that no satisfying truth assignment exists, the algorithm outputs FALSE.
#
# Example Usage:
#   Consider the following instance of 2SAT:
#       (x1 OR x2) AND (x2 OR (not x3)) AND ((not x1) OR x4) AND (x1).
#   To use this module to find a satisfying truth assignment, we do the following:
#       F = [[1, 2], [2, -3], [-1, 4], [1]]
#       L = solve_2SAT(F)
#   If a satisfying truth assignment exists, then L will be a list of Boolean values representing such
#   a truth assignment as follows:
#       for each i=1,2,3,4:
#           L[i] = True if xi is set to true
#           L[i] = False if xi is set to false
#   and L[0] is always set to None and can be ignored.
#   Otherwise, a satisfying truth assignment does not exist and L=False.
#
# Implementation Details:
#   Each literal xi or (not xi) is represented as the integer i or -i.
#   A clause (xi OR (not xj)) is represented a tuple (i, -j).
#   A Boolean formula is represented as a list of lists.
#   A truth assignment is represented as a list L of length n+1, in which
#       L[i] = True if xi is set to TRUE, and
#       L[i] = False if xi is set to FALSE.
#       (Note: We always set L[0] = None because the first Boolean variable is x1.)
#
#   For example, we represent the following formula F
#       (x1 OR x2) AND (x2 OR (not x3)) AND ((not x1) OR x4) AND (x1)
#   as follows:
#       F = [[1, 2], [2, -3], [-1, 4], [1]]
#   and a satisfying truth assignment for F as follows:
#       L = [None, True, True, True, True]

from .graphs import DirectedGraph

def solve_2SAT(formula):
    """
    Solves the given instance of 2SAT.

    :param formula: An instance of 2SAT represented as a list of clauses. Each clause is
                    represented as a list of two non-zero integers. The negation of a variable is
                    represented using a negative integer.

                    E.g. [[1, -2], [2, 3]] represents the instance (x1 OR (NOT x2)) AND (x2 OR x3).

    :return: A satisfying truth assignment A if it exists, and False if not.
             Here, A is represented as a list in which the ith entry represents the truth value it
             assigns to the Boolean variable xi. A[0] is always set to None as a dummy placeholder.

             E.g. [None, True, False] represents the truth assignment in which x1 = True, x2 = False.
    """
    number_of_variables = max([abs(var) for clause in formula for var in clause])

    # Construct the directed graph.
    D = DirectedGraph()
    for i in range(1, number_of_variables+1):
        D.add_vertex(i)
        D.add_vertex(-i)
    for clause in formula:
        if len(clause) == 1:
            # Treat a clause of the form [xi] as the equivalent clause [xi, xi] instead.
            D.add_edge(-clause[0], clause[0])
        elif len(clause) == 2:
            D.add_edge(-clause[0], clause[1])
            D.add_edge(-clause[1], clause[0])
        else:
            raise ValueError("The formula contains the clause", clause, "of length >2.")

    # Process the strong components of D.
    strong_components = D.get_strong_components()
    marks = [None for i in range(len(strong_components))]

    for i, S in enumerate(strong_components):
        if marks[i] != None:
            pass
        # If S = complement(S), then there is no satisfying assignment.
        # Here, complement(S) = [-x for x in S].
        # Note that S = complement(S) if and only if there exists some x such that
        # x and -x are both in S.
        elif any([(-x in S) for x in S]):
            return False
        else:
            # Mark S as True and complement(S) as False.
            marks[i] = True
            for j, T in enumerate(strong_components):
                if -S[0] in T:
                    marks[j] = False

    # Return the satisfying truth assignment in which a variable xi is True if and only if
    # the vertex i is in a strong component marked as True.
    A = [None for i in range(number_of_variables+1)]
    for mark, S in zip(marks, strong_components):
        if mark == True:
            # Set all variables xi such that i is in S as True.
            for i in S:
                if i>0:
                    A[i] = True
        else:
            for i in S:
                if i>0:
                    A[i] = False

    return A

def is_satisfying_assignment(formula, assignment):
    """Verifies whether the given truth assignment satisfies the given formula in CNF."""
    for clause in formula:
        clause_satisfied = False
        for literal in clause:
            if literal>0 and assignment[literal] == True or\
                literal<0 and assignment[-literal] == False:
                # As long as one literal is satisfied, the entire clause is satisfied.
                clause_satisfied = True
                break
            else:
                continue
        if not clause_satisfied:
            return False

    # Every clause is satisfied.
    return True
