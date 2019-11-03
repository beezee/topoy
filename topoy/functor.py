from abc import ABC, abstractmethod
from topoy.hkt import HKT
from topoy.typevars import *
from typing import Callable, Generic

class Functor(ABC, Generic[F]):

  @abstractmethod
  def map(self, fa: HKT[F, A], 
          f: Callable[[A], B]) -> HKT[F, B]: pass
