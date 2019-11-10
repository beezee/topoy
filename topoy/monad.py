from abc import ABC, abstractmethod
from topoy.hkt import HKT
from topoy.functor import Functor
from topoy.typevars import *
from typing import Callable, Generic

class Monad(Functor[F]):

  #@abstractmethod
  def point(self, a: A) -> HKT[F, A]: pass

  #@abstractmethod
  def bind(self, fa: HKT[F, A],
           f: Callable[[A], HKT[F, B]]) -> HKT[F, B]: pass
