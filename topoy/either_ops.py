from abc import ABC, abstractmethod
from topoy.hkt import HKT
from topoy.typevars import *
from typing import cast, Callable, Generic, TypeVar
from typing import Tuple
from topoy.applicative import Applicative

import topoy.either as instances

class EitherOps(ABC, Generic[X, A]):

  def __init__(self, run: instances.Either[X, A]) -> None:
    self.run = run

  def map_data(
    self, fn: Callable[[instances.Either[X, A]], instances.Either[B, Y]]
  ) -> 'EitherOps[B, Y]':
    return EitherOps(fn(self.run))
    
  @staticmethod
  def inj(l: 'instances.Either[X, A]') -> 'HKT[instances.EitherF[X], A]':
    return cast('HKT[instances.EitherF[X], A]', l)

  @staticmethod
  def proj(hkt: 'HKT[instances.EitherF[X], A]') -> 'instances.Either[X, A]':
    return cast('instances.Either[X, A]', hkt)

  @staticmethod
  def lift(hkt: 'HKT[instances.EitherF[X], A]') -> 'EitherOps[X, A]':
    return EitherOps(EitherOps.proj(hkt))

  def __str__(self) -> str:
    return str(self.run)

  def map(self, f: Callable[[A], B]) -> 'EitherOps[X, B]':
    return EitherOps.lift(instances.EitherFunctor[X]().map(self.run, f))
  
  def bind(
    self, f: Callable[[A], 'instances.Either[X, B]']
  ) -> 'EitherOps[X, B]':
    return EitherOps.lift(instances.EitherMonad[X]().bind(self.run, f))
  
  def ap(
    self, fab: 'instances.Either[X, Callable[[A], B]]'
  ) -> 'EitherOps[X, B]':
    return EitherOps.lift(
      instances.EitherApply[X]().ap(self.run, fab))

  def apply(self, fb: 'instances.Either[X, B]',
            f: Callable[[A, B], C]) -> 'EitherOps[X, C]':
    return self.tuple(fb).map(lambda x: f(x[0], x[1]))

  def apply3(self, fb: 'instances.Either[X, B]', fc: 'instances.Either[X, C]',
             f: Callable[[A, B, C], D]) -> 'EitherOps[X, D]':   
    return self.apply(EitherOps(fb).tuple(fc).run, 
      lambda a, bc: f(a, bc[0], bc[1]))

  def apply4(self, fb: 'instances.Either[X, B]', fc: 'instances.Either[X, C]',
             fd: 'instances.Either[X, D]',
             f: Callable[[A, B, C, D], E]) -> 'EitherOps[X, E]':
    return self.apply3(fb, EitherOps(fc).tuple(fd).run,
      lambda a, b, cd: f(a, b, cd[0], cd[1]))

  def apply5(self, fb: 'instances.Either[X, B]', fc: 'instances.Either[X, C]',
             fd: 'instances.Either[X, D]', fe: 'instances.Either[X, E]',
             f: Callable[[A, B, C, D, E], H]) -> 'EitherOps[X, H]':
    return self.apply4(fb, fc, EitherOps(fd).tuple(fe).run,
      lambda a, b, c, de: f(a, b, c, de[0], de[1]))

  def apply6(self, fb: 'instances.Either[X, B]', fc: 'instances.Either[X, C]',
             fd: 'instances.Either[X, D]', fe: 'instances.Either[X, E]', fh: 'instances.Either[X, H]',
             f: Callable[[A, B, C, D, E, H], I]) -> 'EitherOps[X, I]':
    return self.apply5(fb, fc, fd, EitherOps(fe).tuple(fh).run,
      lambda a, b, c, d, eh: f(a, b, c, d, eh[0], eh[1]))

  def apply7(self, fb: 'instances.Either[X, B]', fc: 'instances.Either[X, C]',
             fd: 'instances.Either[X, D]', fe: 'instances.Either[X, E]', fh: 'instances.Either[X, H]',
             fi: 'instances.Either[X, I]',
             f: Callable[[A, B, C, D, E, H, I], J]) -> 'EitherOps[X, J]':
    return self.apply6(fb, fc, fd, fe, EitherOps(fh).tuple(fi).run,
      lambda a, b, c, d, e, hi: f(a, b, c, d, e, hi[0], hi[1]))

  def tuple(
    self, fb: 'instances.Either[X, B]'
  ) -> 'EitherOps[X, Tuple[A, B]]':
    return EitherOps.lift(
      instances.EitherApply[X]().tuple(self.run, fb))
  
  def traverse(self, ap: Applicative[G],
    f: Callable[[A], HKT[G, B]]) -> HKT[G, 'EitherOps[X, B]']:
      return ap.map(
        instances.EitherTraverse[X]().traverse(ap, self.run, f),
        EitherOps.lift)
  

