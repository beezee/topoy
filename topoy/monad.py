from abc import ABC, abstractmethod
from topoy.hkt import HKT
from topoy.typevars import *
from typing import Callable, Generic

class Monad(ABC, Generic[F]):

  @abstractmethod
  def bind(self, fa: HKT[F, A],
           f: Callable[[A], HKT[F, B]]) -> HKT[F, B]: pass
