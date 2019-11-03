from abc import abstractmethod
from topoy.hkt import HKT
from topoy.semigroup import Semigroup
from topoy.typevars import *
from typing import Generic

class Plus(Generic[F]):

  @abstractmethod
  def plus(self, fa1: HKT[F, A], fa2: HKT[F, A]) -> HKT[F, A]: pass
