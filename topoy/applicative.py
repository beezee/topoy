from abc import abstractmethod
from topoy.hkt import HKT
from topoy.apply import Apply
from topoy.typevars import *
from typing import Generic


class Applicative(Generic[F], Apply[F]):

  #@abstractmethod
  def pure(self, a: A) -> HKT[F, A]: pass
