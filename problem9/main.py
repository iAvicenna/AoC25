from pathlib import Path
from time import time

import numpy as np
import shapely

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
    data = list(map(lambda x: list(map(int,x.split(','))), fp.readlines()))

  return np.array(data)


def construct_shapes(coordinates, threshold):

  Itriu = np.triu_indices(coordinates.shape[0], k=2)
  squares = []

  for i0,i1 in zip(*Itriu):

    c0 = tuple(coordinates[i0,:])
    c1 = tuple(coordinates[i1,:])
    area = np.prod(abs(np.array(c0) - np.array(c1) + np.array([1,1])))

    if area>threshold:
      c2 = (c0[0],c1[1])
      c3 = (c1[0],c0[1])
      squares.append(shapely.Polygon((c0,c3,c1,c2)))

  polygon = shapely.Polygon(coordinates)

  return polygon, squares


@timing
def solve_problem(file_name, redgreen=False, threshold=0):

  coordinates = parse_input(Path(cwd, file_name))

  if not redgreen:
    areas = np.prod(abs(coordinates[None,:] - coordinates[:,None]) +\
                    np.array([1,1])[None,None,:], axis=-1)
    max_area = np.max(areas)

  else:
    polygon, squares = construct_shapes(coordinates, threshold)
    max_area = -np.inf

    for inds,square in enumerate(squares):
      if square.area==0:
        continue

      if polygon.contains(square):
        c = np.array(list(zip(*square.exterior.coords.xy)))
        if (a:=np.prod(abs(c[0] - c[2]) + np.array([1,1])))>max_area:
          max_area = a

  return int(max_area)



if __name__ == "__main__":

  assert solve_problem("test_input") == 50
  assert solve_problem("input") == 4763509452
  assert solve_problem("test_input", True, 1) == 24
  assert solve_problem("input", True, 15000*80000) == 1516897893 # threshold by eyeballing the shape
