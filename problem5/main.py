
from pathlib import Path
from time import time
from utils import Interval, JoinedIntervals

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

  fresh_ranges, ingredients = data[:(i:=data.index(''))], data[i+1:]

  intervals = JoinedIntervals()

  [intervals.add_interval(Interval(int(fr.split('-')[0]), int(fr.split('-')[1]))) for
   fr in fresh_ranges]

  return intervals, ingredients


@timing
def solve_problem(file_name, return_range=False):

  intervals, ingredients = parse_input(Path(cwd, file_name))

  if return_range:
    return sum([len(i) for i in intervals])

  return len([i for i in ingredients if intervals.contains(int(i))])


if __name__ == "__main__":

  assert solve_problem("test_input") == 3
  assert solve_problem("input1") == 865
  assert solve_problem("test_input", True) == 14
  assert solve_problem("input1", True) == 352556672963116
