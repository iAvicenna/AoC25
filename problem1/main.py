
import numpy as np
from pathlib import Path

cwd = Path(__file__).parent.resolve()


def parse_input(file_path):
  with file_path.open("r") as fp:
    data = list(map(str.strip, fp.readlines()))

  data = [-int(x[1:]) if x[0]=='L' else int(x[1:]) for x in
          data]

  return data


def solve_problem(file_name, click=False):

  rotations = parse_input(Path(cwd, file_name))

  cumulative_rotations = map(lambda x: x%100, np.cumsum(rotations))
  dial_start_position = 50

  dial_positions = [dial_start_position] +\
    [(dial_start_position+i)%100 for i in cumulative_rotations]


  if click:
    return sum([int(np.floor((x+y)/100)) if x+y>99
                else 1*int(x!=0) + int(np.floor(abs(x+y)/100)) if x+y<=0
                else 0 for x,y in zip(dial_positions, rotations)])

  else:
    return dial_positions.count(0)


if __name__ == "__main__":

  assert solve_problem("test_input") == 3
  assert solve_problem("test_input", True) == 6
  assert solve_problem("input1") == 1139
  assert solve_problem("input1", True) == 6684
