from abc import abstractmethod
from topoy.hkt import HKT
from topoy.plus import Plus
from topoy.typevars import *
from typing import Generic, Type

class PlusEmpty(Generic[F], Plus[F]):

  @abstractmethod
  def empty(self, t: Type[A]) -> HKT[F, A]: pass

