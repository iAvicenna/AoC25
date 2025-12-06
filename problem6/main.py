from pathlib import Path
from time import time

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


def get(x):
  try:
    return int(x)
  except ValueError:
    return {'+':sum, '*':np.prod}[x]


def parse_input(file_path, cephalopod_math):
  with file_path.open("r") as fp:
    if not cephalopod_math:
      data = list(map(lambda x: x.split(' '), fp.readlines()))
      data = np.array([[get(y.strip()) for y in x if y.strip()!='']
                       for x in data])
    else:
      data = list(map(str.rstrip, fp.readlines()))
      maxlen = max(map(len,data))
      data = [row.ljust(maxlen) for row in data]

      I = [ind for ind,x in enumerate(data[-1]) if x in set(['*','+'])]
      I.append(maxlen+1)
      data = np.array([[row[I[i]:I[i+1]-1] for i in range(len(I)-1)]
                       for row in data], dtype=object)

  return data

def compute(op):

  data = [int(''.join(row).replace(' ', ''))
          for row in np.array([list(row) for row in op[:-1]]).T]
  return get(op[-1].strip())(data)


@timing
def solve_problem(file_name, cephalopod_math=False):

  inst = parse_input(Path(cwd, file_name), cephalopod_math)

  if not cephalopod_math:
    return sum(np.apply_along_axis(lambda x: x[-1](x[:-1]), 0, inst))

  return sum(np.apply_along_axis(compute, 0, inst))


if __name__ == "__main__":

  assert solve_problem("test_input")==4277556
  assert solve_problem("input1")==6378679666679
  assert solve_problem("test_input", True) == 3263827
  assert solve_problem("input1", True) == 11494432585168
