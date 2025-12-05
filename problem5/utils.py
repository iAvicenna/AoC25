#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  5 05:06:31 2025

@author: avicenna
"""


class Interval():

    def __init__(self,a0,a1):
      self.a0 = a0
      self.a1 = a1

    def intersects(self, interval):
      return not(self.a1<interval.a0 or self.a0>interval.a1)

    def contains(self, num):
      return self.a0<=num and self.a1>=num

    def __len__(self):
      return self.a1-self.a0+1


class JoinedIntervals():

  def __init__(self):
    self.intervals = []

  def add_interval(self, new_interval):

    intersected = [new_interval]
    nonintersected = []

    for ind, interval in enumerate(self.intervals):
      if interval.intersects(new_interval):
        intersected.append(interval)
      else:
        nonintersected.append(interval)

    min_a0 = min([i.a0 for i in intersected])
    max_a1 = max([i.a1 for i in intersected])

    self.intervals = nonintersected + [Interval(min_a0, max_a1)]
    self.intervals = sorted(self.intervals, key=lambda x: x.a1)

  def contains(self, num):
    return any([x.contains(num) for x in self.intervals])

  def __iter__(self):
    return iter(self.intervals)
