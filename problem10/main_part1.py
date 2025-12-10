
import itertools as it
import numpy as np
import galois
from pathlib import Path
from time import time

cwd = Path(__file__).parent
GF2 = galois.GF(2)


def timing(f):
  def wrap(*args, **kw):
    ts = time()
    result = f(*args, **kw)
    te = time()
    print(f"func{f.__name__} args: {args} took: {te-ts:.4f} sec")

    return result
  return wrap


def convert_line(line):

  target = line.split('] ')[0][1:]
  vectors = line.split('] ')[1].split(' ')[:-1]
  weights = line.split('] ')[1].split(' ')[-1].strip()

  ndims = len(target)

  target = np.array([0 if l=='.' else 1 for l in target], dtype=int)
  weights = np.array(list(map(int,weights[1:-1].split(','))))

  M = []

  for v in vectors:
    coords = [int(x) for x in v if x.isnumeric()]
    vec = np.zeros(ndims, dtype=int)
    vec[coords] = 1
    M.append(vec)

  return np.array(M).T,target,weights


def parse_input(file_path):
  with file_path.open("r") as fp:
    manual = list(map(convert_line, fp.readlines()))

  return manual


def find_pivots(R):
    pivots = []
    m, n = R.shape
    row = 0

    for col in range(n):
      if row < m and R[row, col] == 1:
        pivots.append(col)
        row += 1

    return pivots


def solve(A, x):

  M = GF2(np.hstack([np.array(A), np.array(x)[:,None]]))
  R = M.row_reduce()

  pivots = find_pivots(R)

  m, n_plus_1 = R.shape
  n = n_plus_1 - 1

  inconsistent = any(all(R[i, :n] == 0) and R[i, n] == 1
                     for i in range(m))

  if inconsistent:
    raise ValueError("no solutions")

  particular = GF2.Zeros(n)

  for r, c in enumerate(pivots):
      particular[c] = R[r, n]

  return np.array(particular)


def minimum(nullspace, particular):

  nvecs = nullspace.shape[0]

  coef = np.array(list(it.product(np.arange(0, 10), repeat=nvecs)))

  A = np.sum(np.mod(coef@np.array(nullspace) + particular[None,:],2),axis=-1)

  I = np.argmin(A)
  res = np.mod(coef[I]@np.array(nullspace) + particular[None,:],2)

  return np.sum(res)


@timing
def solve_problem1(file_name, verbose=False):

  manual = parse_input(Path(cwd, file_name))
  sum_press = 0

  for ind,(M,target,_) in enumerate(manual):
    M = GF2(M)
    target = GF2(target)
    nullspace = M.null_space()
    if verbose:
      print(f"reduction: {M.shape[1]}->{nullspace.shape[0]}")
    particular = solve(M, target)
    sum_press += minimum(nullspace, particular)

  return sum_press



if __name__ == "__main__":

  assert solve_problem1("test_input") == 7
  assert solve_problem1("input") == 475
