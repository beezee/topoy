from topoy.hkt import HKT
from topoy.functor import Functor
from topoy.monad import Monad
from topoy.typevars import *
from typing import Callable, cast, Generic

class Fn(Generic[A, B]):

  def __init__(self, fn: Callable[[A], B]) -> None:
    self._fn = fn

  def __call__(self, a: A) -> B:
    return self._fn(a)

class Id(Generic[A]):

  def __call__(self, a: A) -> A:
    return a

class Compose(Generic[A, B, C]):
  def __init__(self, c2: Callable[[B], C], 
               c1: Callable[[A], B]) -> None:
    (self.c1, self.c2) = (c1, c2)

  def __call__(self, t1: A) -> C:
    return self.c2(self.c1(t1))
  
class Fn0():
  @staticmethod
  def inj(fn: Callable[[], A]) -> 'HKT[Fn0, A]':
    return cast(HKT[Fn0, A], fn)

  @staticmethod
  def proj(hkt: 'HKT[Fn0, A]') -> Callable[[], A]:
    return cast(Callable[[], A], hkt)

class Fn0Functor(Functor[Fn0]):

  def map(self, fa: HKT[Fn0, A],
          f: Callable[[A], B]) -> HKT[Fn0, B]:
    return Fn0.inj(lambda: f(Fn0.proj(fa)()))

class Fn0Monad(Monad[Fn0]):
  
  def bind(self, fa: HKT[Fn0, A],
           f: Callable[[A], HKT[Fn0, B]]) -> HKT[Fn0, B]:
    return f(Fn0.proj(fa)())
