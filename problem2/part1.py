
import numpy as np
from pathlib import Path

cwd = Path(__file__).parent.resolve()


def parse_input(file_path):
  with file_path.open("r") as fp:
    data = list(map(str.strip, fp.readlines()))

  assert len(data)==1

  ranges = data[0].split(',')

  return ranges


def solve_range(a,b):
  '''
  given a range a-b with a<b find all numbers with repeating
  sequence of digits such as 1212. The point is to not iterate through every
  number and use next_symmetric for iterating.
  '''

  if a==b and len(str(a))%2!=0:
    return []

  if len(str(a))%2!=0:
    a = 10**(np.floor(np.log10(a)))

  if len(str(b))%2!=0:
    b = 10**(np.floor(np.log10(b))+1)


  current = a if is_symmetric(a) else next_symmetric(a)

  while current <= b:
    yield current

    current = next_symmetric(current)


def next_symmetric(a):
  '''
  find the next integer with repeated indices
  '''

  p1 = np.floor(np.log10(a))

  # if odd number of integers jump to next power, for instance
  # 100->1010
  if (p1+1)%2 != 0:
    return next_symmetric(10**(p1+1))

  # if symmetrized version of a is larger than a that is the next one
  if (sa:=symmetrize(a))>a:
    return sa

  # if not increment it
  a_next = a + 10**((p1+1)/2)
  p2 = np.floor(np.log10(a_next))

  # if p1 != p2 happens we are npw on a number with odd number of integers
  # so jump
  if p1 != p2:
    return next_symmetric(10**(p2+1))

  return symmetrize(a_next)


def symmetrize(a):
  '''
  if the code above is working as intended this should only be called
  when a has even number of integers
  '''

  p = np.floor(np.log10(a))

  assert (p+1)%2 == 0

  return int(str(a)[:int((p+1)/2)]*2)


def is_symmetric(a):

  p = np.floor(np.log10(a))

  if (p+1)%2 != 0:
    return False

  if str(a)[:int((p+1)/2)]==str(a)[-int((p+1)/2):]:
    return True

  return False


def solve_problem(file_name):

  ranges = parse_input(Path(cwd, file_name))

  sum_val = 0

  for r in ranges:
    a,b = list(map(int, r.split('-')))
    for val in solve_range(a,b):
      sum_val += val

  return sum_val

if __name__ == "__main__":

  assert solve_problem("test_input") == 1227775554

  assert solve_problem("input1") == 38158151648
