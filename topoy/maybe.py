from topoy.either import *
from topoy.semigroup import KeepLeft

Maybe = Sum2[None, A]

class MaybeF(EitherF[None]):
  @staticmethod
  def inj(s: Sum2[None, A]) -> 'HKT[EitherF[None], A]':
    return cast(HKT[EitherF[None], A], s)

  @staticmethod
  def proj(hkt: 'HKT[EitherF[None], A]') -> Sum2[None, A]:
    return cast(Sum2[None, A], hkt)

class MaybeFunctor(EitherFunctor[None]): pass

class MaybeMonad(EitherMonad[None]): pass

class MaybeApply(EitherApply[None]):

  def __init__(self) -> None:
    self._sg = KeepLeft[None]()

class MaybeApplicative(MaybeApply, EitherApply[None]): pass

class MaybeTraverse(EitherTraverse[None]): pass
