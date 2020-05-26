from topoy.either import *
from topoy.either_ops import EitherOps
from topoy.semigroup import KeepLeft, Semigroup

class Maybe(Generic[A]):
  @staticmethod
  def inj(s: Either[None, A]) -> 'HKT[EitherF[None], A]':
    return cast(HKT[EitherF[None], A], s)

  @staticmethod
  def proj(hkt: 'HKT[EitherF[None], A]') -> Either[None, A]:
    return cast(Either[None, A], hkt)

  @classmethod
  def just(cls, a: A) -> EitherOps[None, A]:
    return RightOf[None].put(a)

  @classmethod
  def none(cls) -> EitherOps[None, A]:
    return LeftOf[A].put(None)

def MaybeFunctor() -> EitherFunctor[None]:
  return EitherFunctor[None]()

def MaybeMonad() -> EitherMonad[None]:
  return EitherMonad[None]()

def MaybeApply(sg: Semigroup[None] = KeepLeft[None]()) -> EitherApply[None]:
  return EitherApply[None](sg)

def MaybeApplicative(sg: Semigroup[None] = KeepLeft[None]()) -> EitherApplicative[None]:
  return EitherApplicative[None](sg)

def MaybeTraverse() -> EitherTraverse[None]:
  return EitherTraverse[None]()
