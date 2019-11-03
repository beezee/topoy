from dataclasses import dataclass
from topoy.apply import Apply
from topoy.bind import Bind
from topoy.hkt import HKT
from topoy.functor import Functor
from typing import Callable, Generic, List, TypeVar

F = TypeVar('F')
A = TypeVar('A')
FA = TypeVar('FA')
B = TypeVar('B')
FB = TypeVar('FB')
FAB = TypeVar('FAB')

class ListF(): pass
@dataclass
class HKList(Generic[A], HKT[ListF, A, List[A]]):
  run: List[A]

class ListFunctor(Generic[A, B], 
                  Functor[ListF, A, List[A], B, List[B]]):

  def map(self, fa: HKT[ListF, A, List[A]], 
          f: Callable[[A], B]) -> HKList[B]:
    return HKList(list(map(f, fa.run)))

class BindList(Generic[A, B],
               Bind[ListF, A, List[A], B, List[B]]):

  def bind(self, fa: HKT[ListF, A, List[A]], 
           f: Callable[[A], HKT[ListF, B, List[B]]]) -> HKList[B]:
    return HKList([x for y in ListFunctor(fa, f)().run for x in y.run])

class ListApply(Generic[A, B],
                Apply[ListF, A, List[A], B, List[B],
                      List[Callable[[A], B]]]):

  def ap(self, fa: HKT[ListF, A, List[A]],
       fab: HKT[ListF, Callable[[A], B], 
                List[Callable[[A], B]]]) -> HKT[ListF, B, List[B]]:
    def kleisli(a: A) -> HKList[B]:
      def m(ab: Callable[[A], B]) -> B:
        return ab(a)
      return HKList(list(map(m, fab.run)))
    return BindList(fa, kleisli)()
