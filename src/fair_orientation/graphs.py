# This module contains the graph classes used by the other modules in the package.

from collections import deque

class Graph:
    def __init__(self, V = [], E = []):
        """
        :param V: A list of vertices, each represented by an integer.
        :param E: The set of (unoriented) edges, each represented by a tuple of two vertices (u, v).
                  Internal to the Graph class, we always store the tuples so that u <= v for convenience.
        """
        self.V = V
        self.E = [tuple(sorted(e)) for e in E]
    def get_vertices(self):
        return self.V
    def get_edges(self):
        return self.E
    def add_vertex(self, name):
        self.V.append(name)
    def add_edge(self, e):
        self.E.append(tuple(sorted(e)))
    def get_next_index(self):
        """
        Returns a positive integer that has not been used as a vertex label. Useful when adding a new vertex.
        """
        return max(self.V)+1
    def get_components(self):
        """
        Returns the omponents of G.
        :return: A list of the components of G, each of which is represented as a list of vertices.
        """
        visited = set()
        queue = deque()
        components = []
        while len(visited) < len(self.V):
            # Find an unvisited vertex.
            unvisited_vertex = None
            for i in range(len(self.V)):
                unvisited_vertex = self.V[i]
                if unvisited_vertex not in visited:
                    break

            # BFS from the unvisited vertex.
            queue.append(unvisited_vertex)
            component = []
            while len(queue) > 0:
                v = queue.popleft()
                component.append(v)
                visited.add(v)
                for e in self.E:
                    if v in e:
                        other_endpoint = e[0] if v == e[1] else e[1]
                        if other_endpoint not in visited:
                            queue.append(other_endpoint)
                            visited.add(other_endpoint)
            components.append(component)
        return components

class DirectedGraph:
    """
    A class representing a directed graph. The outneighbors of each vertex is stored using a dictionary, so looking
    up the outneighborhood of a vertex takes O(1) time.
    """
    def __init__(self):
        self.V = []
        self.outneighborhood = {}
    def add_vertex(self, name):
        """Adds a new vertex with label 'name'. The label can be any immutable type (e.g. integers, strings, etc)."""
        self.V.append(name)
        self.outneighborhood[name] = []
    def add_edge(self, u, v):
        """Adds a directed edge from u to v."""
        self.outneighborhood[u].append(v)
    def get_strong_components(self):
        """Returns the strong components found using Tarjan's algorithm."""
        def strongconnect(v, index, stack, onstack, indices, lowlink, strong_components):
            indices[v] = index
            lowlink[v] = index
            index += 1
            stack.append(v)
            onstack[v] = True

            for w in self.outneighborhood[v]:
                if w not in indices.keys():
                    index = strongconnect(w, index, stack, onstack, indices, lowlink, strong_components)
                    lowlink[v] = min(lowlink[v], lowlink[w])
                elif onstack[w]:
                    lowlink[v] = min(lowlink[v], indices[w])

            if lowlink[v] == indices[v]:
                strong_component = []
                while True:
                    w = stack.pop()
                    onstack[w] = False
                    strong_component.append(w)
                    if w == v:
                        break
                strong_components.append(strong_component)
            return index

        index = 0
        stack = deque()
        onstack = {v:False for v in self.V}
        indices = {}
        lowlink = {}
        strong_components = []
        for v in self.V:
            if v not in indices.keys():
                index = strongconnect(v, index, stack, onstack, indices, lowlink, strong_components)

        return strong_components

class GraphicalInstance(Graph):
    """
    A class representing a graphical instance of the fair division problem. The utilities of the edges
    are represented using a dictionary util in the following way: For each edge e=(i,j) where i <= j,
    we have util[e] = (u_i(e), u_j(e)). Moreover, e has zero utility to vertices other than i and j.

    :parem V: A set of vertices, represented by positive integers.
    :parem E: A set of edges, represented by tuples of two positive integers each.
    """
    def __init__(self, V = [], E = []):
        super().__init__(V, E)
        self.util = {}
    def get_util(self, v, e):
        """
        Returns the utility of an edge to a vertex.
        :param v: vertex
        :param e: edge
        :return: The utility of edge e to vertex v.
        """
        if v not in e:
            return 0
        elif v == e[0]:
            return self.util[e][0]
        else:
            return self.util[e][1]
    def set_util(self, e, util_u, util_v):
        """
        Sets the utility of the edge e=(u,v) to u to util_u and v to util_v.
        :param e: edge
        :param util_u: An integer or float.
        :param util_v: An integer or float.
        """
        u = e[0]
        v = e[1]
        if u <= v:
            self.util[(u,v)] = (util_u, util_v)
        else:
            self.util[(v,u)] = (util_v, util_u)
    def number_of_negative_edges(self, S):
        """
        Computes the number of negative edges whose endpoints both belong in S.
        :param S: A set of vertices.
        :return: The number of negative edges whose endpoints both belong in S.
        """
        count = 0
        for e in self.E:
            if e[0] in S and e[1] in S and self.is_negative_edge(e):
                count += 1
        return count

    def is_negative_edge(self, e):
        """
        Checks if a given edge is a negative edge (i.e. e has negative utility to both endpoints).
        :param e: An edge.
        :return: True if e is a negative edge and False otherwise.
        """
        if self.get_util(e[0], e) < 0 and self.get_util(e[1], e) < 0:
            return True
        else:
            return False

    def is_objective_edge(self, e):
        """
        Checks if a given edge e is an objective edge (i.e. either e has negative utility to both endpoints or zero
        utility to both endpoints).
        :param e: An edge.
        :return: True if e is an objective edge and False otherwise.
        """
        if self.is_negative_edge(e) or (self.get_util(e[0], e) == 0 and self.get_util(e[1], e) == 0):
            return True
        else:
            return False

    def get_negative_subinstance(self):
        """
        Returns a new GraphicalInstance object that has the same vertex set but only the negative edges. This is done
        by copying over everything but ignoring the non-negative edges.
        """
        subinstance = GraphicalInstance(self.V, [])
        for e in self.E:
            if self.is_negative_edge(e):
                subinstance.add_edge(e)
                subinstance.set_util(e, self.get_util(e[0], e), self.get_util(e[1], e))
        return subinstance

    def get_negative_components(self):
        """
        Finds the negative components of G. This function assumes G is an objective instance (i.e. every edge is
        objective).
        :return: A list of the negative components of G, each of which is represented as a list of vertices.
        """
        # Generate the subgraph that contains only the negative edges.
        G_negative = Graph(self.V, [e for e in self.E if self.is_negative_edge(e)])
        return G_negative.get_components()

class Orientation(GraphicalInstance):
    """
    A class representing an orientation of a graphical instance, that is, a graphical instance in which
    each edge is oriented toward one of its endpoints. This can be interpreted as each edge being
    allocated to the endpoint that it is oriented toward.
    """
    def __init__(self, G):
        super().__init__(G.get_vertices(), G.get_edges())
        self.util = G.util.copy()

        # We use a dictionary to keep track of the orientations of the edges
        # e.g. orientations[(u,v)] = v means that the edge e is oriented toward v.
        self.orientations = {}

        # The is_oriented dictionary keeps tracks of which edges have been oriented.
        self.oriented = {e:False for e in self.E}
    def orient(self, e, v):
        """
        Orients the edge e toward the vertex v.
        :param e: An edge.
        :param v: A vertex.
        """
        self.orientations[e] = v
        self.oriented[e] = True
    def is_oriented(self, e):
        """Returns True if the edge e has been oriented and False otherwise."""
        if self.oriented[e]:
            return True
        else:
            return False
    def get_orientation(self, e):
        """Returns the endpoint of the edge e that it is directed toward."""
        return self.orientations[e]
    def is_EFX(self):
        """Returns True if the orientation is EFX and False otherwise."""
        # To check whether the orientation is EFX, we verify that for each vertex v, there is either one edge directed
        # toward v, or every edge directed toward v has zero utility to v
        for v in self.V:
            edges_directed_toward_v = [e for e in self.E if self.get_orientation(e) == v]
            if len(edges_directed_toward_v) > 1 and \
                    len([e for e in edges_directed_toward_v if self.get_util(v, e) < 0]) > 0:
                return False
        return True
    def is_EF1(self):
        """Returns True if the orientation is EF1 and False otherwise."""
        # To check whether the orientation is EF1, we verify that for each vertex v, among all edges directed toward v,
        # at most one has negative utility to v.
        for v in self.V:
            if len([e for e in self.E if self.get_orientation(e) == v and self.get_util(v,e)<0]) > 1:
                return False
        return True
    def get_directed_edges(self):
        """Returns the directed edges of the orientation."""
        return self.orientations.copy()
    def __str__(self):
        s = "Vertices: " + str(self.V) + "\nOriented Edges: "
        unoriented_edges = [e for e in self.E if e not in self.orientations.keys()]
        if len(unoriented_edges) > 0:
            for e in unoriented_edges:
                s = s + '{' + str(e[0]) + ', ' + str(e[1]) + "}, "
            s = s[:-2] + "\nOriented Edges: "
        else:
            s = s + "None\nOriented Edges: "
        if len(self.orientations.keys()) > 0:
            for e in self.orientations.keys():
                dst = self.get_orientation(e)
                src = e[0] if dst == e[1] else e[1]
                s = s + '(' + str(src) + ', ' + str(dst) + '), '
            s = s[:-2]
        else:
            s = s + "None"
        return s

    def _orient_using_observation_3(self):
        """
        Orients the graph in the way described by Obervation 3 in the paper. Specifically,
        this function attempts to orient the edges in a way that each vertex receives at most one incoming edge.

        Precondition: This function assumes that this is possible to do. The caller should verify this before calling
        this function. Note: Such an orientation exists if and only if G does not contain a component K with more than
        |V(K)| edges.
        """
        # For each negative component K, we use BFS to find a rooted spanning tree T of K with root r(T). We orient all
        # tree edges from parent to child. If K only has |V(K)|-1 negative edges, then all of them are tree edges so we
        # are done. Otherwise, K has |V(K)| negative edges, so K contains exactly one unoriented edge uw. In this case,
        # we orient uw toward w, and reverse the orientations of all tree edges between r(T) and w.

        visited = set()
        queue = deque()

        # To keep track of the BFS trees of each negative component, we use a dictionary "parent" that stores the
        # parent of each vertex in the trees. A root vertex is its own parent.
        parent = {}

        while len(visited) < len(self.V):
            # Find an unvisited vertex to start a new BFS from.
            unvisited_vertex = None
            for i in range(len(self.V)):
                unvisited_vertex = self.V[i]
                if unvisited_vertex not in visited:
                    break
            parent[unvisited_vertex] = unvisited_vertex

            # Start a new BFS from the unvisited vertex.
            queue.append(unvisited_vertex)
            visited.add(unvisited_vertex)

            while len(queue) > 0:
                v = queue.popleft()
                for e in self.E:
                    if v in e and self.is_negative_edge(e):
                        other_endpoint = e[0] if v == e[1] else e[1]
                        if other_endpoint not in visited:
                            parent[other_endpoint] = v  # Add the edge to the BFS tree
                            self.orient(e, other_endpoint)  # Orient the edge "downward" from parent to child
                            queue.append(other_endpoint)
                            visited.add(other_endpoint)

        # As described in Observation 3, we now orient each remaining unoriented edge uw to an arbitrary endpoint w,
        # then reverse the orientations all negative edges between w and the root of the BFS tree r.
        for e in self.E:
            if not self.is_oriented(e):
                u = e[0]
                w = e[1]
                self.orient(e, w)
                while parent[w] != w:  # If parent[w] == w, then w is the root of the BFS tree it belongs to, so we stop.
                    backtrack_edge = (parent[w], w)
                    self.orient(backtrack_edge, parent[w])
                    w = parent[w]  # Backtrack along the BFS tree toward the root.



