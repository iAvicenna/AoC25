import numpy as np
from pathlib import Path

cwd = Path(__file__).parent


def parse_input(file_path):

  with file_path.open("r") as fp:
    banks = map(str.strip, fp.readlines())

  return map(lambda x: list(map(int, list(x))), banks)


def max_jolt(bank, length):

  if length==1:
    return max(bank)

  amax = np.argmax(bank[:-(length-1)])

  return 10**(length-1)*bank[amax] + max_jolt(bank[amax+1:], length-1)


def solve_problem(file_name, length):

  banks = parse_input(Path(cwd, file_name))
  sumj = 0

  for bank in banks:
    sumj += max_jolt(bank, length)

  return sumj


if __name__ == "__main__":

  assert solve_problem("test_input", 2) == 357

  assert solve_problem("input", 2) == 17408

  assert solve_problem("test_input", 12) == 3121910778619

  assert solve_problem("input", 12) == 172740584266849
