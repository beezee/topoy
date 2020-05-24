from abc import ABC, abstractmethod
from topoy.hkt import HKT
from topoy.typevars import *
from typing import cast, Callable, Generic, TypeVar
from typing import Tuple
from topoy.applicative import Applicative

import topoy.either_data as instances

class Either(ABC, instances.EitherData[X, A]):
  @staticmethod
  def inj(l: 'Either[X, A]') -> 'HKT[instances.EitherF[X], A]':
    return cast('HKT[instances.EitherF[X], A]', l)

  @staticmethod
  def proj(hkt: 'HKT[instances.EitherF[X], A]') -> 'Either[X, A]':
    return cast('Either[X, A]', hkt)

  def map(self, f: Callable[[A], B]) -> 'Either[X, B]':
    return Either.proj(instances.EitherFunctor[X]().map(self, f))
  
  def bind(
    self, f: Callable[[A], 'Either[X, B]']
  ) -> 'Either[X, B]':
    return Either.proj(instances.EitherMonad[X]().bind(self, f))
  
  def ap(
    self, fab: 'Either[X, Callable[[A], B]]'
  ) -> 'Either[X, B]':
    return Either.proj(
      instances.EitherApply[X]().ap(self, fab))

  def apply(self, fb: 'Either[X, B]',
            f: Callable[[A, B], C]) -> 'Either[X, C]':
    return self.tuple(fb).map(lambda x: f(x[0], x[1]))

  def apply3(self, fb: 'Either[X, B]', fc: 'Either[X, C]',
             f: Callable[[A, B, C], D]) -> 'Either[X, D]':   
    return self.apply(fb.tuple(fc), 
      lambda a, bc: f(a, bc[0], bc[1]))

  def apply4(self, fb: 'Either[X, B]', fc: 'Either[X, C]',
             fd: 'Either[X, D]',
             f: Callable[[A, B, C, D], E]) -> 'Either[X, E]':
    return self.apply3(fb, fc.tuple(fd),
      lambda a, b, cd: f(a, b, cd[0], cd[1]))

  def apply5(self, fb: 'Either[X, B]', fc: 'Either[X, C]',
             fd: 'Either[X, D]', fe: 'Either[X, E]',
             f: Callable[[A, B, C, D, E], H]) -> 'Either[X, H]':
    return self.apply4(fb, fc, fd.tuple(fe),
      lambda a, b, c, de: f(a, b, c, de[0], de[1]))

  def apply6(self, fb: 'Either[X, B]', fc: 'Either[X, C]',
             fd: 'Either[X, D]', fe: 'Either[X, E]', fh: 'Either[X, H]',
             f: Callable[[A, B, C, D, E, H], I]) -> 'Either[X, I]':
    return self.apply5(fb, fc, fd, fe.tuple(fh),
      lambda a, b, c, d, eh: f(a, b, c, d, eh[0], eh[1]))

  def apply7(self, fb: 'Either[X, B]', fc: 'Either[X, C]',
             fd: 'Either[X, D]', fe: 'Either[X, E]', fh: 'Either[X, H]',
             fi: 'Either[X, I]',
             f: Callable[[A, B, C, D, E, H, I], J]) -> 'Either[X, J]':
    return self.apply6(fb, fc, fd, fe, fh.tuple(fi),
      lambda a, b, c, d, e, hi: f(a, b, c, d, e, hi[0], hi[1]))

  def tuple(
    self, fb: 'Either[X, B]'
  ) -> 'Either[X, Tuple[A, B]]':
    return Either.proj(
      instances.EitherApply[X]().tuple(self, fb))
  
  def traverse(self, ap: Applicative[G],
    f: Callable[[A], HKT[G, B]]) -> HKT[G, 'Either[X, B]']:
      return ap.map(
        instances.EitherTraverse[X]().traverse(ap, self, f),
        Either.proj)
  

