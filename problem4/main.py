#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  4 09:10:02 2025

@author: avicenna
"""

import itertools as it
from pathlib import Path
from functools import wraps
from time import time

import numpy as np

cwd = Path(__file__).parent.resolve()

def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print(f"{f.__name__} args: {args} took: {te-ts:.4f} sec")

        return result
    return wrap


def parse_input(file_path):
  with file_path.open("r") as fp:
    grid = np.array(list(map(list, list(map(str.strip, fp.readlines())))),
                    dtype=str)
  return grid


@timing
def solve_problem(file_name, single_attempt=True):

  grid = parse_input(Path(cwd, file_name))
  nr, nc = grid.shape
  nacc_total = 0
  stop = False

  while not stop:

    nacc = 0

    for i,j in it.product(range(nr), range(nc)):

      if grid[i,j] != '@':
        continue

      if np.count_nonzero(grid[max(i-1, 0):min(i+2, nr),
                               max(j-1, 0):min(j+2, nc)] == '@')<5:
        nacc += 1

        if not single_attempt:
          grid[i,j] = '.'

    nacc_total += nacc

    if nacc==0 or single_attempt:
      stop = True

  return nacc_total


if __name__ == "__main__":

  assert solve_problem("test_input") == 13
  assert solve_problem("input1") == 1445
  assert solve_problem("test_input", False) == 43
  assert solve_problem("input1", False) == 8317
