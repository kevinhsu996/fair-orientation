# Fair Division

This project implements two algorithms for fair division of tasks/chores
under graphical constraints. Specifically, it implements the algorithms from
the paper "*Polynomial-Time Algorithms for Fair Orientations of
Chores*" due to Hsu and King, published in the European Conference
on Artificial Intelligence (ECAI 2025) [1].

## Table of Contents
- [Introduction](#introduction)
  - [Problem Overview](#problem-overview)
  - [Example Applications](#example-applications)
- [Technical Details](#technical-details)
  - [Usage Guide](#usage-guide)
    - [Setting up a problem instance](#setting-up-a-problem-instance)
    - [Finding an EF1 or EFX orientation](#finding-an-ef1-or-efx-orientation)
    - [Interpreting the results](#interpreting-the-results)
  - [Tests](#tests)
  - [Bonus: 2SAT](#bonus-2sat)
- [References](#references)
- [License](#license)

# Introduction
## Problem Overview

Let $G=(V,E)$ be a graph. Suppose that each vertex represents an
*agent* and each edge $e=\{i, j\}$ represents a *chore/task*
that only agents $i$ and $j$ can perform. The edge $e$ is associated
with a cost to each of its endpoints $i$ and $j$, represented by
non-positive numbers denoted by $u_i(e)$ and $u_j(e)$. Note that
it is possible that $e$ has different costs to $i$ and $j$ (i.e.
perhaps agent $i$ finds task $e$ easier than agent $j$ does, in which
case $u_i(e) > u_j(e)$). We
can represent an *allocation*
of the chores to the agents as an *orientation*
of the graph $G$. Specifically, we do this by directing an edge
$e=\{i, j\}$ toward the endpoint $i$ whenever we would like to
allocate the chore $e$ to the agent $i$.

In many real-life applications, the agents that vertices represent
are humans or parties with conflicting interests. So, we would like
to orient the chores in a *fair* manner to reduce envy between the
agents. Unfortunately, it is usually impossible to find an
envy-free orientation of the chores, so researchers have devised
many relaxations of envy-freeness. Two particularly prominent
relaxations are called EF1 and EFX orientations, which have been
studied widely in the fair division literature. In short, an allocation
is

1) EF1 if for each pair of agents $i \neq j$, agent $i$ possibly
envies agent $j$, but ceases to envy $j$ if $i$ ignores the worst chore
allocated to them;
2) EFX if for each pair of agents $i \neq j$, agent $i$ possibly
envies agent $j$, but ceases to envy $j$ if $i$ ignores any single
chore allocated to them.

This project implements the two algorithms for computing EF1 and EFX
orientations due to Hsu and King.

## Example Applications

**Dividing Household Chores:** Dividing household chores between family members.\
Different family members often prefer different chores. Moreover,
some family members might not be able to do certain chores. For
example, somebody might not be home during the time when a chore
needs to be done, or a child might be too young to help with
more complex tasks.

**Assigning Delivery Tasks:** Allocating delivery tasks to delivery drivers.\
Drivers may have preferences over deliveries depending on their
familiarity with the neighborhoods, or over the distances that they
are away from the pick-up and delivery locations.

   
# Technical Details

Requires Python 3 (tested on Python 3.14). Standard library only and
no external dependencies.

## Usage Guide

### Installation

The package can be installed by running the following from the command line.
```bash
git clone https://github.com/kevinhsu996/fair-orientation.git
cd fair-orientation
pip install .
```

### Setting up a problem instance

Suppose $G$ is a 4-cycle $(1,2,3,4)$ together with a fifth vertex $5$
and edges $\{1,5\}$ and $\{3,5\}$, as shown below.
```
2 --- 1
|   / |
|  5  |
| /   |
3 --- 4
```
Suppose that each of the 4 edges on the 4-cycle $(1,2,3,4)$ has
utility -1 to both of its endpoints, and that the two edges
incident with vertex 5 have utility -1 to vertex 5 and utility
0 to their other endpoints.

We use the ```GraphicalInstance``` class to represent the problem
instance as follows.

```python
from fair_orientation import GraphicalInstance

# Construct the graph G.
G = GraphicalInstance([1, 2, 3, 4, 5],
                      [(1, 2), (2, 3), (3, 4), (4, 1), (1, 5), (5, 3)])

# Set the utilities of the edges.
G.set_util((1, 2), -1, -1)
G.set_util((2, 3), -1, -1)
G.set_util((3, 4), -1, -1)
G.set_util((4, 1), -1, -1)
G.set_util((3, 5), 0, -1) # i.e. the edge {3,5} has utility 0 to 3 and utility -1 to 5
G.set_util((1, 5), 0, -1) # i.e. the edge {1,5} has utility 0 to 1 and utility -1 to 5
```

### Finding an EF1 or EFX orientation
To find an EF1 or EFX orientation, we use the ```find_EF1_orientation```
and ```find_EFX_orientation``` functions. We reuse ```G``` from
the above example.

```python
from fair_orientation import find_EF1_orientation, find_EFX_orientation

EF1_orientation = find_EF1_orientation(G)
EFX_orientation = find_EFX_orientation(G)
```

### Interpreting the results
We purposely chose the example instance $G$ to be one that has an
EF1 orientation but no EFX orientation. 

Since $G$ has an EF1 orientation, ```EF1_orientation``` is an
```Orientation``` object. There are two ways to access its directed
edges. The first is to call its class function ```get_directed_edges()```,
which returns a Python dictionary in which each key is an edge ```e```,
and value that the key is mapped to is the endpoint that the edge
is directed toward.

```python
directed_edges = EF1_orientation.get_directed_edges()
print(directed_edges)

# This outputs {(1, 5): 1, (3, 5): 3, (1, 2): 2, (2, 3): 3, (3, 4): 4, (1, 4): 1}
# which means for example the edge {1, 5} is directed toward vertex 1.
```

Another way to simply call ```print(EF1_orientation)```.

```python
print(EF1_orientation)

# This prints the following:
#
# Vertices: [1, 2, 3, 4, 5, 6, 7]
# Unoriented Edges: None
# Oriented Edges: (5, 1), (5, 3), (1, 2), (2, 3), (3, 4), (4, 1)
```

(**Note:** There are never unoriented edges in an EF1 or an EFX
orientation because the problem requires that all edges be oriented.
The function ```Orientation.__str__``` behaves this
way in case the user wants to design another function to orient
the edges, and wants to see what edges are yet unoriented in the
midst of the process.)

On the other hand, because $G$ does not have an EFX orientation,
the function call ```find_EFX_orientation(G)``` returns ```False```.
Thus, the following assertion will run without error.

```python
assert EFX_orientation == False
```
## Tests
A few small unit tests are included in the `/tests` directory. They
can be run by calling `pytest` from the root directory.

## Bonus: 2SAT
This project also includes an implementation of the linear-time
algorithm for 2SAT due to Aspvall et al., which may be of
independent interest. See `sat.py` for details.

# References

[1] K. Hsu and V. King, "Polynomial-time algorithms for fair orientations of chores",
in *ECAI 2025*, IOS Press, 2025, pp. 3511-3518

# License

This project is licensed under the MIT License.
See the LICENSE file for details.

