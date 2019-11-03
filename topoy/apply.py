from abc import ABC, abstractmethod
from topoy.functor import Functor
from topoy.hkt import HKT
from topoy.typevars import *
from typing import Callable, Generic, Tuple

class Apply(Generic[F], Functor[F]):

  @abstractmethod
  def ap(self, fa: HKT[F, A],
       fab: HKT[F, Callable[[A], B]]) -> HKT[F, B]: pass

  def tuple(self, fa: HKT[F, A], 
            fb: HKT[F, B]) -> HKT[F, Tuple[A, B]]:
    def tup(b: B) -> Callable[[A], Tuple[A, B]]:
      def x(a: A) -> Tuple[A, B]:
        return (a, b)
      return x
    return self.ap(fa, self.map(fb, tup))
