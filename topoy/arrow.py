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
