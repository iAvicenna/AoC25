
import numpy as np
import itertools as it
from pathlib import Path
from time import time

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

  objects = []
  for i in range(6):
    i0 = data.index(f"{i}:")
    obj = np.array(list(map(list, data[i0+1:i0+4])))
    obj[obj=='#']=1
    obj[obj=='.']=0
    objects.append(obj.astype(int))

  i0 = data.index("5:")+5
  placements = []

  for line in data[i0:]:
    dims = list(map(int, line.split(':')[0].split('x')))
    nobjs = list(map(int, line.split(': ')[-1].split(' ')))
    placements.append((dims, nobjs))

  return objects, placements

@timing
def solve_problem(file_name):

  ref_objects, placements = parse_input(Path(cwd, file_name))
  areas = [np.count_nonzero(obj==1) for obj in ref_objects]

  counter_succesful = 0

  for grid_shape, nobjs in placements:

    obj_area = np.sum(np.array(nobjs)*areas)
    grid_area = np.prod(grid_shape)
    worse_area =  np.sum(np.array(nobjs)*9)

    if worse_area<=grid_area:
      counter_succesful += 1
      continue

    if obj_area>grid_area:
      continue

  return counter_succesful


if __name__ == "__main__":

  assert solve_problem("input") == 583
