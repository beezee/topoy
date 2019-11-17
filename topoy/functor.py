from abc import ABC, abstractmethod
from topoy.hkt import HKT
from topoy.typevars import *
from typing import Callable, Generic, TypeVar

class Functor(ABC, Generic[F]):

  """ All typeclasses defs should use instance methods
      because conformance to abstract interface is 
      not verified by the type-checker until instantiation.
      This will allow mypy to catch attempts to 
      use ill-defined instances before runtime """
  @abstractmethod
  def map(cls, fa: HKT[F, A], 
          f: Callable[[A], B]) -> HKT[F, B]: ...
