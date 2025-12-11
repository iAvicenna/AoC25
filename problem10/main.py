
import itertools as it
import numpy as np
import galois
from pathlib import Path
from time import time
from sympy import Matrix, symbols, linsolve

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
  jolts = line.split('] ')[1].split(' ')[-1].strip()

  ndims = len(target)

  target = np.array([0 if l=='.' else 1 for l in target], dtype=int)
  jolts = np.array(list(map(int,jolts[1:-1].split(','))))

  M = []

  for v in vectors:
    coords = [int(x) for x in v if x.isnumeric()]
    vec = np.zeros(ndims, dtype=int)
    vec[coords] = 1
    M.append(vec)

  return np.array(M).T,target,jolts


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


def solve_GF2(A, x):

  nullspace = A.null_space()

  M = GF2(np.hstack([np.array(A), np.array(x)[:,None]]))
  R = M.row_reduce()

  pivots = find_pivots(R)

  m, n = R.shape
  n -= 1

  particular = GF2.Zeros(n)

  for r, c in enumerate(pivots):
      particular[c] = R[r, n]

  return np.array(particular), nullspace


def solve_Q(M, x):
  b = symbols(" ".join([f"b{i}" for i in range(M.shape[1])]))
  solution = list(linsolve((M, x), b))[0]
  syms = list(solution.free_symbols)
  func = Matrix(solution)

  particular = np.array(func.subs({s:0 for s in syms}).tolist()).flatten().astype(float)
  nullspace = np.array([np.array(x.tolist()).flatten() for x in M.nullspace()]).astype(float)

  return particular, nullspace


def minimize(nullspace, particular, jolt):

  nvecs = nullspace.shape[0]

  if not jolt:
    coef = np.array(list(it.product(np.arange(0, 2), repeat=nvecs)))
    A = np.sum(np.mod(coef@np.array(nullspace) + particular[None,:],2),axis=-1)
    I = np.argmin(A)
    res = np.mod(coef[I]@np.array(nullspace) + particular[None,:],2)

    return np.sum(res)
  else:
    N = 100
    I = []

    while len(I)==0: # look for a positive integer solution, if does not exist increase N

      coef = np.array(list(it.product(np.arange(-N, N), repeat=nvecs)))
      A = coef@np.array(nullspace) + particular[None,:]
      mask = (A >= 0) & np.isclose(A, A.astype(int))
      I = np.where(mask.all(axis=1))[0]
      N += 500

    return np.min(np.sum(A[I,:],axis=-1))


@timing
def solve_problem(file_name, jolt=False):

  manual = parse_input(Path(cwd, file_name))
  sum_press = 0

  for ind,(M, light_target, jolt_target) in enumerate(manual):

    if not jolt:
      #part1 solve over GF2, looks for minimal solution of the form particular + null
      M = GF2(M)
      target = GF2(light_target)
      particular, nullspace = solve_GF2(M, target)

    else:
      #part2 solve over Q, look for minimal integer, positive solution of the form particular + null
      target = Matrix(jolt_target.astype(int))
      M = Matrix(M.astype(int))
      particular, nullspace = solve_Q(M, target)

    sum_press += minimize(nullspace, particular, jolt)

  return sum_press


if __name__ == "__main__":

  assert solve_problem("test_input") == 7
  assert solve_problem("input") == 475
  assert solve_problem("test_input", True) == 33
  assert solve_problem("input", True) == 18273
