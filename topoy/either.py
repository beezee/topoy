from topoy.applicative import Applicative
from topoy.apply import Apply
from topoy.monad import Monad
from topoy.hkt import HKT
from topoy.functor import Functor
from topoy.traverse import Traverse
from topoy.typevars import *
from topoy.semigroup import KeepLeft, Semigroup
from topoy.sum import append2sg, bind2, F1, F2, fold2, map2, Sum2
from typing import Callable, cast, Generic

class EitherF(Generic[B]):
  @staticmethod
  def inj(s: Sum2[B, A]) -> 'HKT[EitherF[B], A]':
    return cast(HKT[EitherF[B], A], s)

  @staticmethod
  def proj(hkt: 'HKT[EitherF[B], A]') -> Sum2[B, A]:
    return cast(Sum2[B, A], hkt)

class EitherFunctor(Generic[C], Functor[EitherF[C]]):

  def map(self, fa: HKT[EitherF[C], A], 
          f: Callable[[A], B]) -> HKT[EitherF[C], B]:
    return EitherF[C].inj(map2(EitherF[B].proj(fa), f))

class EitherMonad(Generic[C], Monad[EitherF[C]]):

  def bind(self, fa: HKT[EitherF[C], A],
           f: Callable[[A], HKT[EitherF[C], B]]) -> HKT[EitherF[C], B]:
    return EitherF[C].inj(bind2(EitherF[C].proj(fa), 
            lambda x: EitherF[C].proj(f(x))))

class EitherApply(Generic[C], Apply[EitherF[C]], EitherFunctor[C]):

  def __init__(self, sg: Semigroup[C] = KeepLeft[C]()) -> None:
    self._sg = sg

  def ap(self, fa: HKT[EitherF[C], A],
       fab: HKT[EitherF[C], Callable[[A], B]]) -> HKT[EitherF[C], B]:
    return self.map(
      EitherF[C].inj(append2sg(
        EitherF[C].proj(fa), EitherF[C].proj(fab), 
        self._sg)), 
      lambda x: x[1](x[0]))

class EitherApplicative(Generic[C], 
                        Applicative[EitherF[C]], 
                        EitherApply[C]):

  def pure(self, a: A) -> HKT[EitherF[C], A]:
    return EitherF[C].inj(F2(a))

class EitherTraverse(Generic[C], Traverse[EitherF[C]], EitherFunctor[C]):

  def traverse(self, 
    ap: Applicative[G], fa: HKT[EitherF[C], A], 
    f: Callable[[A], HKT[G, B]]) -> HKT[G, HKT[EitherF[C], B]]:
      return fold2[C, A, HKT[G, HKT[EitherF[C], B]]]((
        lambda c: ap.pure(EitherF[C].inj(F1(c))),
        lambda a: ap.map(f(a), lambda x: EitherF[C].inj(F2(x)))))(
        EitherF[C].proj(fa))
