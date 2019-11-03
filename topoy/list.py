from dataclasses import dataclass
from functools import reduce
from topoy.applicative import Applicative
from topoy.apply import Apply
from topoy.arrow import Id
from topoy.monad import Monad
from topoy.hkt import HKT
from topoy.functor import Functor
from topoy.plus_empty import PlusEmpty
from topoy.traverse import Traverse
from topoy.typevars import *
from typing import Callable, cast, Generic, List, Type

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

class ListApplicative(Applicative[ListF], ListApply):

  def pure(self, a: A) -> HKT[ListF, A]:
    return ListF.inj([a])

class ListPlusEmpty(PlusEmpty[ListF]):

  def empty(self, t: Type[A]) -> HKT[ListF, A]:
    return ListF.inj([])

  def plus(self, la1: HKT[ListF, A], la2: HKT[ListF, A]) -> HKT[ListF, A]:
    return ListF.inj(ListF.proj(la1) + ListF.proj(la2))

class ListTraverse(Traverse[ListF], ListFunctor):

  def traverse(self, 
    ap: Applicative[G], fa: HKT[ListF, A], 
    f: Callable[[A], HKT[G, B]]) -> HKT[G, HKT[ListF, B]]:
      def reducer(acc: HKT[G, List[B]], 
                 e: A) -> HKT[G, List[B]]:
        def m(lb: List[B]) -> Callable[[B], List[B]]:
          def x(b: B) -> List[B]:
            return lb + [b]
          return x
        return ap.ap(f(e), ap.map(acc, m)) #type: ignore
      return ap.map(
        reduce(reducer, ListF.proj(fa), #type: ignore
          ap.pure([])), ListF.inj) # type: ignore
