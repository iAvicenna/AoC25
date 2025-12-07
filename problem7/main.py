
from pathlib import Path
from time import time

import numpy as np
import itertools as it

cwd = Path(__file__).parent


def timing(f):
  def wrap(*args, **kw):
    ts = time()
    result = f(*args, **kw)
    te = time()
    print(f"func{f.__name__} args: {args} took: {te-ts:.4f} sec")

    return result
  return wrap


def parse_input(file_path):
  with file_path.open("r") as fp:
    data = list(map(str.strip, fp.readlines()))

  return np.array([list(row) for row in data], dtype=object)


class Node:

  def __init__(self, symbol, row, col):
    self.symbol = symbol
    self.loc = tuple([row, col])
    self.parents = []
    self.npaths_to_start = -1

  @property
  def is_connected(self):
    return self.symbol=='S' or len(self.parents)>0

  def connect(self, node_dict, s0, s1):

    if self.loc[0]==0:
      return

    top = node_dict[(self.loc[0]-1, self.loc[1])]

    if top.symbol in ['.','S'] and top.is_connected:
      self.parents.append(top)

    if self.symbol=='^' and top.is_connected:
      left =  node_dict[(self.loc[0], self.loc[1]-1)]
      right =  node_dict[(self.loc[0], self.loc[1]+1)]

      left.parents.append(self)
      right.parents.append(self)


def count_paths_to_start(node0, node1):
  '''
  node0 should always be the start node else
  result is meaningless
  '''

  if node0 in node1.parents:
    return 1
  else:
    npaths = 0
    for p in node1.parents:
      if p.npaths_to_start != -1:
        npaths += p.npaths_to_start
      else:
        p.npaths_to_start = count_paths_to_start(node0, p)
        npaths += p.npaths_to_start

    return npaths


@timing
def solve_problem(file_name, quantum=False):

  grid = parse_input(Path(cwd, file_name))
  s0,s1 = grid.shape

  node_dict = {(i,j):Node(grid[i,j], i, j) for i,j in it.product(range(s0), range(s1))}
  [node.connect(node_dict, s0, s1) for node in node_dict.values()]

  if not quantum:
    return len([x for x in node_dict.values() if x.symbol == '^' and
                x.is_connected>0])
  else:
    start_ind = [(0, j) for j in range(s1) if node_dict[0,j].symbol=='S'][0]
    start_node = node_dict[start_ind]

    npaths = 0

    end_nodes = [node_dict[(s0-1,j)] for j in range(s1) if
                 node_dict[s0-1,j].is_connected]

    for indn, end_node in enumerate(end_nodes):

      npaths += count_paths_to_start(start_node, end_node)

    return npaths


if __name__ == "__main__":

  assert solve_problem("test_input") == 21
  assert solve_problem("input") == 1633
  assert solve_problem("test_input", True) == 40
  assert solve_problem("input", True) == 34339203133559
