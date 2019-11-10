from abc import ABC
from topoy.hkt import HKT
from topoy.typevars import *
from typing import Callable, Generic

class Contravariant(ABC, Generic[F]):

  @classmethod
  def contramap(cls, fa: HKT[F, A], ba: Callable[[B], A]) -> HKT[F, B]: pass
