from topoy.typevars import *
from typing import Callable, Generic

class Fn(Generic[A, B]):

  def __init__(self, fn: Callable[[A], B]) -> None:
    self._fn = fn

  def __call__(self, a: A) -> B:
    return self._fn(a)

class Id(Generic[A]):

  def __call__(self, a: A) -> A:
    return a

class Compose(Generic[A, B, C]):
  def __init__(self, c2: Callable[[B], C], 
               c1: Callable[[A], B]) -> None:
    (self.c1, self.c2) = (c1, c2)

  def __call__(self, t1: A) -> C:
    return self.c2(self.c1(t1))
  
