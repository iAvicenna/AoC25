
from pathlib import Path
from time import time

import networkx as nx
import numpy as np

cwd = Path(__file__).parent.resolve()


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

  nodes = [y for line in data for y in line.replace(':','').split(' ')]
  M = np.zeros((len(nodes), len(nodes)))

  for line in data:
    from_node = line.split(':')[0]
    to_nodes = line.split(': ')[-1].split(' ')
    I0 = nodes.index(from_node)
    I1 = [nodes.index(n) for n in to_nodes]
    M[I0, I1] = 1

  return M, nodes


def count_paths_between(ind0, ind1, M):
  '''
  counts paths by severing any outgoing connection from node ind1
  and using transfer matrices. Stopping condition is having the
  same positive number of paths for 10 cycles.
  '''

  vec = np.zeros((M.shape[0]))
  vec[ind0] = 1
  nhistory = []
  A = M.T.copy()
  A[:, ind1] = 0
  A[ind1, ind1] = 1
  counter = 0

  while True:
    vec = A@vec
    nhistory.append(vec[ind1])
    counter +=1

    if len(nhistory)>10 and (len(set(nhistory[-10:]))==1 and  nhistory[-1]!=0):
      return nhistory[-1]


def count_paths_dag(G, source, target):

  npaths = {node: 0 for node in G.nodes()}
  npaths[source] = 1

  sorted_nodes = list(nx.topological_sort(G))

  for node in sorted_nodes[sorted_nodes.index(source):]:
    for nbr in G.successors(node):
      npaths[nbr] += npaths[node]

  return npaths[target]


@timing
def solve_problem1(file_name, path_nodes=None):

  M, nodes = parse_input(Path(cwd, file_name))

  if path_nodes is None:
    npaths = count_paths_between(nodes.index("you"), nodes.index("out"), M)

  else:
    G = nx.from_numpy_array(M, create_using=nx.DiGraph(),
                            nodelist=nodes)

    # assumed G is a DAG, below will raise error if not
    sorted_nodes = list(nx.topological_sort(G))

    sorted_path_nodes = sorted(path_nodes, key=sorted_nodes.index)

    #make sure path nodes are not topoligically equivalent
    for node1, node2 in zip(sorted_path_nodes[:-1], sorted_path_nodes[1:]):
      assert nx.has_path(G, node1, node2)


    npaths = np.prod([count_paths_dag(G, node1, node2) for node1, node2 in
                      zip(sorted_path_nodes[:-1], sorted_path_nodes[1:])])


  return npaths



if __name__ == "__main__":

  assert solve_problem1("test_input1") == 5
  assert solve_problem1("input") == 431

  assert solve_problem1("test_input2", ["svr","dac","fft","out"]) == 2
  assert solve_problem1("input",  ["svr","dac","fft","out"]) == 358458157650450
