from topoy.applicative import Applicative
from topoy.apply import Apply, tuple
from topoy.monad import Monad
from topoy.hkt import HKT
from topoy.functor import Functor
from topoy.traverse import Traverse
from topoy.typevars import *
from topoy.semigroup import KeepLeft, Semigroup
from topoy.sum import append2sg, bind2, F1, F2, fold2, map2, Sum2
from typing import Callable, cast, Generic, Tuple

class EitherF(Generic[B]): pass

class Either(HKT[EitherF[B], A]):

  @staticmethod
  def inj(e: 'Either[B, A]') -> 'HKT[EitherF[B], A]':
    return cast(HKT[EitherF[B], A], e)

  @staticmethod
  def proj(hkt: 'HKT[EitherF[B], A]') -> 'Either[B, A]':
    return cast('Either[B, A]', hkt)

  def __init__(self, run: Sum2[B, A]) -> None:
    self.run = run

  def left_map(self, f: Callable[[B], C]) -> 'Either[C, A]':
    return fold2[B, A, 'Either[C, A]']((
      lambda l: Either(F1(f(l))),
      lambda r: Either(F2(r))))(self.run)

  def map(self, f: Callable[[A], C]) -> 'Either[B, C]':
    return fold2[B, A, 'Either[B, C]']((
      lambda l: Either(F1(l)),
      lambda r: Either(F2(f(r)))))(self.run)

  def bimap(self, fl: Callable[[B], C], fr: Callable[[A], D]) -> 'Either[C, D]':
    return self.map(fr).left_map(fl)

  def bind(self, afb: Callable[[A], 'Either[B, C]']) -> 'Either[B, C]':
    return fold2[B, A, 'Either[B, C]']((
      lambda l: Either(F1(l)),
      lambda r: afb(r)))(self.run)

  def ap(self, fab: 'Either[B, Callable[[A], C]]', 
         sg: Semigroup[B] = KeepLeft[B]()) -> 'Either[B, C]':
    return Either(append2sg(self.run, fab.run, sg)).map(lambda x: x[1](x[0]))

  def tuple(self, fb: 'Either[B, C]') -> 'Either[B, Tuple[A, C]]':
    return Either.proj(
      tuple(EitherApplicative(), self, fb))

  def traverse(self, 
    ap: Applicative[G], 
    f: Callable[[A], HKT[G, C]]) -> HKT[G, 'Either[B, C]']:
      return fold2[B, A, HKT[G, 'Either[B, C]']]((
        lambda l: ap.pure(LeftOf[C].put(l)),
        lambda r: ap.map(f(r), lambda x: RightOf[B].put(x))))(self.run)

  def __str__(self) -> str:
    return fold2[B, A, str]((
      lambda l: 'Left(' + str(l) + ')',
      lambda r: 'Right(' + str(r) + ')'))(self.run)

class LeftOf(Generic[A]):

  @classmethod
  def put(cls, b: B) -> Either[B, A]:
    return Either[B, A](F1(b))

class RightOf(Generic[A]):

  @classmethod
  def put(cls, b: B) -> Either[A, B]:
    return Either[A, B](F2(b))

class EitherFunctor(Generic[C], Functor[EitherF[C]]):

  def map(self, fa: HKT[EitherF[C], A], 
          f: Callable[[A], B]) -> HKT[EitherF[C], B]:
    return Either.proj(fa).map(f)

class EitherMonad(Generic[C], EitherFunctor[C], Monad[EitherF[C]]):

  def point(self, a: A) -> HKT[EitherF[C], A]:
    return RightOf[C].put(a)

  def bind(self, fa: HKT[EitherF[C], A],
           f: Callable[[A], HKT[EitherF[C], B]]) -> HKT[EitherF[C], B]:
    return Either.proj(fa).bind(lambda x: Either.proj(f(x)))

class EitherApply(Generic[C], Apply[EitherF[C]], EitherFunctor[C]):

  def __init__(self, sg: Semigroup[C] = KeepLeft[C]()) -> None:
    self._sg = sg

  def ap(self, fa: HKT[EitherF[C], A],
       fab: HKT[EitherF[C], Callable[[A], B]]) -> HKT[EitherF[C], B]:
    return Either.proj(fa).ap(Either.proj(fab), self._sg)

class EitherApplicative(Generic[C], 
                        Applicative[EitherF[C]], 
                        EitherApply[C]):

  def pure(self, a: A) -> HKT[EitherF[C], A]:
    return RightOf[C].put(a)

class EitherTraverse(Generic[C], Traverse[EitherF[C]], EitherFunctor[C]):

  def traverse(self, 
    ap: Applicative[G], fa: HKT[EitherF[C], A], 
    f: Callable[[A], HKT[G, B]]) -> HKT[G, HKT[EitherF[C], B]]:
      return ap.map(Either.proj(fa).traverse(ap, f), Either.inj)
