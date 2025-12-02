
import numpy as np
from pathlib import Path

cwd = Path(__file__).parent.resolve()


def parse_input(file_path):
  with file_path.open("r") as fp:
    data = list(map(str.strip, fp.readlines()))

  assert len(data)==1

  ranges = data[0].split(',')

  return ranges


def check_number(num):
  num = str(num)

  if  len(num)==1:
    return False

  level_set = set(num)

  if (len(num) in [2, 3, 5, 7, 11, 13, 17] and len(level_set)>1) or\
    len(level_set)>len(num)/2:
    return False

  # if some of the integers appear multiple times, number
  # of repeats can be lower than their count inside the number
  max_nreps = min(num.count(num[0]), num.count(num[1]))

  for nreps in range(2, max_nreps+1):

    if len(num)%nreps != 0:
      continue

    chunk = num[:int(len(num)/nreps)]

    if num.count(chunk)==nreps:
      return True

  return False

check_number = np.vectorize(check_number)


def solve_problem(file_name):

  ranges = parse_input(Path(cwd, file_name))
  sum_val = 0

  for r in ranges:
    a,b = list(map(int, r.split('-')))

    vals = np.arange(a,b+1, dtype=int)
    I = check_number(vals)
    sum_val += np.sum(vals[I])

  return sum_val



if __name__ == "__main__":

  assert solve_problem("test_input") == 4174379265
  assert solve_problem("input1") == 45283684555
