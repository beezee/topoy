from abc import ABC, abstractmethod
from topoy.hkt import HKT
from topoy.typevars import *
from typing import Callable, Generic

class Contravariant(ABC, Generic[F]):

  @abstractmethod
  def contramap(self, fa: HKT[F, A], ba: Callable[[B], A]) -> HKT[F, B]: pass
