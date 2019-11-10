from abc import ABC, abstractmethod
from topoy.hkt import HKT
from topoy.typevars import *
from typing import Callable, Generic, TypeVar

class Functor(ABC, Generic[F]):

  # all this stuff should be abstract, but
  # its making a nightmare for generic code leveraging these
  # typeclasses
  # https://github.com/python/mypy/issues/7863
  #@abstractmethod
  def map(self, fa: HKT[F, A], 
          f: Callable[[A], B]) -> HKT[F, B]: ...
