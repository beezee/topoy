from topoy.apply import Apply
from topoy.applicative import Applicative
from topoy.hkt import HKT
from topoy.functor import Functor
from topoy.monad import Monad
from topoy.typevars import *
from typing import Callable, cast, Generic, Tuple

State = Callable[[S], Tuple[A, S]]

class StateF(Generic[S]):
  @staticmethod
  def inj(s: State[S, A]) -> 'HKT[StateF[S], A]':
    return cast(HKT[StateF[S], A], s)

  @staticmethod
  def proj(hkt: 'HKT[StateF[S], A]') -> State[S, A]:
    return cast(State[S, A], hkt)

class StateFunctor(Generic[S], Functor[StateF[S]]):

  def map(self, fa: HKT[StateF[S], A], 
          f: Callable[[A], B]) -> HKT[StateF[S], B]:
    def x(s: S) -> Tuple[B, S]:
      (a, s2) = StateF.proj(fa)(s)
      return (f(a), s2)
    return StateF[S].inj(x)

class StateMonad(Generic[S], StateFunctor[S], Monad[StateF[S]]):

  def point(self, a: A) -> HKT[StateF[S], A]:
    return StateF[S].inj(lambda x: (a, x))

  def bind(self, fa: HKT[StateF[S], A],
           f: Callable[[A], HKT[StateF[S], B]]) -> HKT[StateF[S], B]:
    def x(s: S) -> Tuple[B, S]:
      (a, s2) = StateF.proj(fa)(s)
      return StateF.proj(f(a))(s2)
    return StateF.inj(x)
