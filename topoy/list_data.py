from functools import reduce
from topoy.applicative import Applicative
from topoy.apply import Apply
from topoy.monad import Monad
from topoy.hkt import HKT
from topoy.functor import Functor
from topoy.plus_empty import PlusEmpty
from topoy.traverse import Traverse
from topoy.typevars import *
from typing import Callable, cast, Generic, List as PyList, Tuple, Type

class ListF(): pass

class ListData(HKT[ListF, A]):

  def __init__(self, run: PyList[A]) -> None:
    self.run = run

  @staticmethod
  def _inj(l: 'ListData[A]') -> 'HKT[ListF, A]':
    return cast(HKT[ListF, A], l)

  @staticmethod
  def _proj(hkt: 'HKT[ListF, A]') -> 'ListData[A]':
    return cast('ListData[A]', hkt)

class ListFunctor(Functor[ListF]):

  def map(self, fa: HKT[ListF, A], f: Callable[[A], B]) -> HKT[ListF, B]:
    return ListData([f(a) for a in ListData._proj(fa).run])

class ListMonad(ListFunctor, Monad[ListF]):

  def point(self, a: A) -> HKT[ListF, A]:
    return ListData([a])

  def bind(self, fa: HKT[ListF, A],
           f: Callable[[A], HKT[ListF, B]]) -> HKT[ListF, B]:
    return ListData(
      [x for y in ListData._proj(fa).run
         for x in ListData._proj(f(y)).run])

class ListApply(Apply[ListF], ListFunctor):

  def ap(self, fa: HKT[ListF, A],
       fab: HKT[ListF, Callable[[A], B]]) -> HKT[ListF, B]:
    return ListData(
      [f(a) for a in ListData._proj(fa).run
            for f in ListData._proj(fab).run])

class ListApplicative(Applicative[ListF], ListApply):

  def pure(self, a: A) -> HKT[ListF, A]:
    return ListData([a])

class ListPlusEmpty(PlusEmpty[ListF]):

  def empty(self, t: Type[A]) -> HKT[ListF, A]:
    return ListData[A]([])

  def plus(self, la1: HKT[ListF, A], la2: HKT[ListF, A]) -> HKT[ListF, A]:
    return ListData(ListData._proj(la1).run + ListData._proj(la2).run)

class ListTraverse(Traverse[ListF], ListFunctor):

  def traverse(self,
    ap: Applicative[G], fa: HKT[ListF, A], 
    f: Callable[[A], HKT[G, B]]) -> HKT[G, HKT[ListF, B]]:
      def reducer(acc: HKT[G, PyList[B]], 
                 e: A) -> HKT[G, PyList[B]]:
        def m(lb: PyList[B]) -> Callable[[B], PyList[B]]:
          def x(b: B) -> PyList[B]:
            return lb + [b]
          return x
        return ap.ap(f(e), ap.map(acc, m))
      z: HKT[G, PyList[B]] = ap.pure([])
      return ap.map(reduce(reducer, ListData._proj(fa).run, z), ListData)

