from dataclasses import dataclass
from topoy.apply import Apply
from topoy.monad import Monad
from topoy.hkt import HKT
from topoy.functor import Functor
from topoy.typevars import *
from typing import Callable, cast, Generic, List

class ListF():
  @staticmethod
  def inj(l: List[A]) -> 'HKT[ListF, A]':
    return cast(HKT[ListF, A], l)

  @staticmethod
  def proj(hkt: 'HKT[ListF, A]') -> List[A]:
    return cast(List[A], hkt)

class ListFunctor(Functor[ListF]):

  def map(self, fa: HKT[ListF, A], f: Callable[[A], B]) -> HKT[ListF, B]:
    return ListF.inj(list(map(f, ListF.proj(fa))))

class ListMonad(Monad[ListF]):

  def bind(self, fa: HKT[ListF, A],
           f: Callable[[A], HKT[ListF, B]]) -> HKT[ListF, B]:
    return ListF.inj(
      [x for y in ListF.proj(ListFunctor().map(fa, f)) 
        for x in ListF.proj(y)])

class ListApply(Apply[ListF], ListFunctor):

  def ap(self, fa: HKT[ListF, A],
       fab: HKT[ListF, Callable[[A], B]]) -> HKT[ListF, B]:
    def kleisli(a: A) -> HKT[ListF, B]:
      def m(ab: Callable[[A], B]) -> B:
        return ab(a)
      return ListF.inj(list(map(m, ListF.proj(fab))))
    return ListMonad().bind(fa, kleisli)
