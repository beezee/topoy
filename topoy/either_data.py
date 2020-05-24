from topoy.applicative import Applicative
from topoy.apply import Apply
from topoy.monad import Monad
from topoy.hkt import HKT
from topoy.functor import Functor
from topoy.traverse import Traverse
from topoy.typevars import *
from topoy.semigroup import KeepLeft, Semigroup
from topoy.sum import append2sg, bind2, F1, F2, fold2, map2, Sum2
from typing import Callable, cast, Generic, Tuple

class EitherF(Generic[B]): pass

class EitherData(HKT[EitherF[B], A]):

  @staticmethod
  def inj(e: 't.Either[B, A]') -> 'HKT[EitherF[B], A]':
    return cast(HKT[EitherF[B], A], e)

  @staticmethod
  def proj(hkt: 'HKT[EitherF[B], A]') -> 't.Either[B, A]':
    return cast('t.Either[B, A]', hkt)

  def __init__(self, run: Sum2[B, A]) -> None:
    self.run = run

  """
  def left_map(self, f: Callable[[B], C]) -> 't.Either[C, A]':
    return fold2[B, A, 't.Either[C, A]']((
      lambda l: t.Either(F1(f(l))),
      lambda r: t.Either(F2(r))))(self.run)

  def bimap(self, fl: Callable[[B], C], fr: Callable[[A], D]) -> 't.Either[C, D]':
    return self.map(fr).left_map(fl)

  def fold(self, fl: Callable[[B], C], fr: Callable[[A], C]) -> C:
    return fold2((fl, fr))(self.run)
  """

  def __str__(self) -> str:
    return fold2[B, A, str]((
      lambda l: 'Left(' + str(l) + ')',
      lambda r: 'Right(' + str(r) + ')'))(self.run)

import topoy.either as t

class LeftOf(Generic[A]):

  @classmethod
  def put(cls, b: B) -> t.Either[B, A]:
    return t.Either[B, A](F1(b))

class RightOf(Generic[A]):

  @classmethod
  def put(cls, b: B) -> t.Either[A, B]:
    return t.Either[A, B](F2(b))

class EitherFunctor(Generic[C], Functor[EitherF[C]]):

  def map(self, fa: 'HKT[EitherF[C], A]',
          f: Callable[[A], B]) -> 'HKT[EitherF[C], B]':
    return fold2[C, A, 't.Either[C, B]']((
      lambda l: t.Either(F1(l)),
      lambda r: t.Either(F2(f(r)))))(t.Either.proj(fa).run)

class EitherMonad(Generic[C], EitherFunctor[C], Monad[EitherF[C]]):

  def point(self, a: A) -> HKT[EitherF[C], A]:
    return RightOf[C].put(a)

  def bind(self, fa: 'HKT[EitherF[C], A]',
           afb: Callable[[A], 'HKT[EitherF[C], B]']
  ) -> 'HKT[EitherF[C], B]':
    return fold2[C, A, 'HKT[EitherF[C], B]']((
      lambda l: t.Either(F1(l)),
      lambda r: afb(r)))(t.Either.proj(fa).run)


class EitherApply(Generic[C], Apply[EitherF[C]], EitherFunctor[C]):

  def __init__(self, sg: Semigroup[C] = KeepLeft[C]()) -> None:
    self._sg = sg

  def ap(self, fa: 'HKT[EitherF[C], A]',
       fab: 'HKT[EitherF[C], Callable[[A], B]]') -> 'HKT[EitherF[C], B]':
    return t.Either(append2sg(
      t.Either.proj(fa).run, 
      t.Either.proj(fab).run, 
      KeepLeft[C]())).map(lambda x: x[1](x[0]))


class EitherApplicative(Generic[C], 
                        Applicative[EitherF[C]], 
                        EitherApply[C]):

  def pure(self, a: A) -> HKT[EitherF[C], A]:
    return RightOf[C].put(a)

class EitherTraverse(Generic[C], Traverse[EitherF[C]], EitherFunctor[C]):

  def traverse(self, 
    ap: Applicative[G], fa: 'HKT[EitherF[C], A]',
    f: Callable[[A], HKT[G, B]]) -> 'HKT[G, HKT[EitherF[C], B]]':
      return fold2[C, A, 'HKT[G, HKT[EitherF[C], B]]']((
        lambda l: ap.pure(LeftOf[B].put(l)),
        lambda r: ap.map(f(r), lambda x: RightOf[C].put(x))))(
        t.Either.proj(fa).run)
