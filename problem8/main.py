#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  8 08:39:02 2025

@author: avicenna
"""

from pathlib import Path
from time import time

import numpy as np
import networkx as nx

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
    coords = list(map(lambda x: list(map(int, x.split(','))), fp.readlines()))

  return np.array(coords)


def binary_search(G, dist):

  Itriu = np.triu_indices(dist.shape[0], k=1)
  dist = dist[Itriu]

  components = list(nx.connected_components(G))
  Isort = [(Itriu[0][i], Itriu[1][i]) for i in np.argsort(dist)]

  icurrent =  0
  ihist = []
  nhist =  []

  while len(ihist)<2 or ihist[-1]!=ihist[-2]:

    ihist.append(icurrent)
    G.add_edges_from(Isort[:icurrent])
    components = list(nx.connected_components(G))
    nhist.append(len(components))

    G.remove_edges_from(Isort[:icurrent])

    if len(components)>1:
      # if >1 components, go between this and closest next index with 1 component

      I = [ind for ind,n in enumerate(nhist) if n==1]

      if len(I)==0:
        inext = len(Isort)
      else:
        inext = min(np.array(ihist)[I])

      icurrent = icurrent + int(np.ceil((inext-icurrent)/2))

    else: # if 1 component, go between nearest previous >1 components and this index
      I = [ind for ind,n in enumerate(nhist) if n>1]

      if len(I)==0:
        iprev = 0
      else:
        iprev = max(np.array(ihist)[I])

      icurrent = iprev + int(np.ceil((icurrent-iprev)/2))

  return Isort[icurrent-1]


@timing
def solve_problem(file_name, nconnect):

  coordinates = parse_input(Path(cwd, file_name))
  G = nx.Graph()
  G.add_nodes_from(range(coordinates.shape[0]))

  dist = np.sqrt(np.sum((coordinates[None,:] - coordinates[:,None])**2,
                        axis=-1))

  if nconnect != -1: # part 1
    Itriu = np.triu_indices(dist.shape[0], k=1)
    dist = dist[Itriu]
    Isort = [(Itriu[0][i], Itriu[1][i]) for i in np.argsort(dist)[:nconnect]]

    G.add_edges_from(Isort)
    components = sorted(list(nx.connected_components(G)), key=len)[::-1]

    return np.prod(list(map(len, components[:3])))
  else: # part 2
    indices = binary_search(G, dist)
    return np.prod(coordinates[indices,:],axis=0)[0]


if __name__ == "__main__":

  assert solve_problem("test_input", 10) == 40
  assert solve_problem("input", 1000) == 115885
  assert solve_problem("test_input", -1) == 25272
  assert solve_problem("input", -1) == 274150525
