from functools import reduce
from topoy.applicative import Applicative
from topoy.apply import Apply, tuple
from topoy.monad import Monad
from topoy.hkt import HKT
from topoy.functor import Functor
from topoy.plus_empty import PlusEmpty
from topoy.traverse import Traverse
from topoy.typevars import *
from typing import Callable, cast, Generic, List as PyList, Tuple, Type

class ListF(): pass
class List(Generic[A], HKT[ListF, A]):

  @staticmethod
  def inj(l: 'List[A]') -> 'HKT[ListF, A]':
    return cast(HKT[ListF, A], l)

  @staticmethod
  def proj(hkt: 'HKT[ListF, A]') -> 'List[A]':
    return cast('List[A]', hkt)

  def __init__(self, run: PyList[A]) -> None:
    self.run = run

  def map(self, f: Callable[[A], B]) -> 'List[B]':
    return List(list(map(f, self.run)))

  def bind(self, f: Callable[[A], 'List[B]']) -> 'List[B]':
    return List([x for y in self.map(f).run for x in y.run])

  def ap(self, fab: 'List[Callable[[A], B]]') -> 'List[B]':
    def kleisli(a: A) -> 'List[B]':
      def m(ab: Callable[[A], B]) -> B:
        return ab(a)
      return fab.map(m)
    return self.bind(kleisli)

  def tuple(self, fb: 'List[B]') -> 'List[Tuple[A, B]]':
    return List.proj(
      tuple(ListApplicative(), self, fb))

  def traverse(self,
    ap: Applicative[G], 
    f: Callable[[A], HKT[G, B]]) -> HKT[G, 'List[B]']:
      def reducer(acc: HKT[G, PyList[B]], 
                 e: A) -> HKT[G, PyList[B]]:
        def m(lb: PyList[B]) -> Callable[[B], PyList[B]]:
          def x(b: B) -> PyList[B]:
            return lb + [b]
          return x
        return ap.ap(f(e), ap.map(acc, m))
      z: HKT[G, PyList[B]] = ap.pure([])
      return ap.map(reduce(reducer, self.run, z), List)

class ListFunctor(Functor[ListF]):

  def map(self, fa: HKT[ListF, A], f: Callable[[A], B]) -> HKT[ListF, B]:
    return List.proj(fa).map(f)

class ListMonad(ListFunctor, Monad[ListF]):

  def point(self, a: A) -> HKT[ListF, A]:
    return List([a])

  def bind(self, fa: HKT[ListF, A],
           f: Callable[[A], HKT[ListF, B]]) -> HKT[ListF, B]:
    return List.proj(fa).bind(lambda x: List.proj((f(x))))

class ListApply(Apply[ListF], ListFunctor):

  def ap(self, fa: HKT[ListF, A],
       fab: HKT[ListF, Callable[[A], B]]) -> HKT[ListF, B]:
    return List.proj(fa).ap(List.proj(fab))

class ListApplicative(Applicative[ListF], ListApply):

  def pure(self, a: A) -> HKT[ListF, A]:
    return List([a])

class ListPlusEmpty(PlusEmpty[ListF]):

  def empty(self, t: Type[A]) -> HKT[ListF, A]:
    return List[A]([])

  def plus(self, la1: HKT[ListF, A], la2: HKT[ListF, A]) -> HKT[ListF, A]:
    return List(List.proj(la1).run + List.proj(la2).run)

class ListTraverse(Traverse[ListF], ListFunctor):

  def traverse(self, 
    ap: Applicative[G], fa: HKT[ListF, A], 
    f: Callable[[A], HKT[G, B]]) -> HKT[G, HKT[ListF, B]]:
      return ap.map(List.proj(fa).traverse(ap, f), List.inj)
