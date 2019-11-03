from abc import ABC, abstractmethod
from topoy.typevars import *
from typing import Generic, List, Tuple

class Semigroup(Generic[A]):

  @abstractmethod
  def append(self, a1: A, a2: A) -> A: pass

class KeepLeft(Semigroup[A]):
  def append(self, a1: A, a2: A) -> A:
    return a1

class KeepRight(Semigroup[A]):
  def append(self, a1: A, a2: A) -> A:
    return a2

class ListSg(Generic[A], Semigroup[List[A]]):
  def append(self, a1: List[A], a2: List[A]) -> List[A]:
    return a1 + a2

class SwapSg(Generic[A], Semigroup[A]):

  def __init__(self, sg: Semigroup[A]) -> None:
    self._sg = sg

  def append(self, a1: A, a2: A) -> A:
    return self._sg.append(a2, a1)

class ProductSg(Generic[A, B], Semigroup[Tuple[A, B]]):
  
  def __init__(self, sg1: Semigroup[A], sg2: Semigroup[B]) -> None:
    (self._sg1, self._sg2) = (sg1, sg2)

  def append(self, a1: Tuple[A, B], a2: Tuple[A, B]) -> Tuple[A, B]:
    return (self._sg1.append(a1[0], a2[0]), self._sg2.append(a1[1], a2[1]))

