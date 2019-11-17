from abc import abstractmethod
from topoy.arrow import Id
from topoy.contravariant import Contravariant
from topoy.hkt import HKT
from topoy.typevars import *
from typing import Callable, Tuple

class Divide(Contravariant[F]):

  def divide1(self, fa: HKT[F, A], f: Callable[[C], A]) -> HKT[F, C]:
    return self.contramap(fa, f)

  @abstractmethod
  def divide(self, fa: HKT[F, A], fb: HKT[F, B], 
             cab: Callable[[C], Tuple[A, B]]) -> HKT[F, C]: pass

  def tuple2(self, fa: HKT[F, A], fb: HKT[F, B]) -> HKT[F, Tuple[A, B]]:
    return self.divide(fa, fb, Id[Tuple[A, B]]())

  def divide3(self, fa: HKT[F, A], fb: HKT[F, B], fc: HKT[F, C],
              f: Callable[[D], Tuple[A, B, C]]) -> HKT[F, D]:
    def ff(d: D) -> Tuple[A, Tuple[B, C]]:
      (a, b, c) = f(d)
      return (a, (b, c))
    return self.divide(fa, self.tuple2(fb, fc), ff)

  def divide4(self, fa: HKT[F, A], fb: HKT[F, B], fc: HKT[F, C],
              fd: HKT[F, D],
              f: Callable[[E], Tuple[A, B, C, D]]) -> HKT[F, E]:
    def ff(e: E) -> Tuple[A, B, Tuple[C, D]]:
      (a, b, c, d) = f(e)
      return (a, b, (c, d))
    return self.divide3(fa, fb, self.tuple2(fc, fd), ff)

  def divide5(self, fa: HKT[F, A], fb: HKT[F, B], fc: HKT[F, C],
              fd: HKT[F, D], fe: HKT[F, E],
              f: Callable[[H], Tuple[A, B, C, D, E]]) -> HKT[F, H]:
    def ff(h: H) -> Tuple[A, B, C, Tuple[D, E]]:
      (a, b, c, d, e) = f(h)
      return (a, b, c, (d, e))
    return self.divide4(fa, fb, fc, self.tuple2(fd, fe), ff)

  def divide6(self, fa: HKT[F, A], fb: HKT[F, B], fc: HKT[F, C],
              fd: HKT[F, D], fe: HKT[F, E], fh: HKT[F, H],
              f: Callable[[I], Tuple[A, B, C, D, E, H]]) -> HKT[F, I]:
    def ff(i: I) -> Tuple[A, B, C, D, Tuple[E, H]]:
      (a, b, c, d, e, h) = f(i)
      return (a, b, c, d, (e, h))
    return self.divide5(fa, fb, fc, fd, self.tuple2(fe, fh), ff)

  def divide7(self, fa: HKT[F, A], fb: HKT[F, B], fc: HKT[F, C],
              fd: HKT[F, D], fe: HKT[F, E], fh: HKT[F, H],
              fi: HKT[F, I],
              f: Callable[[J], Tuple[A, B, C, D, E, H, I]]) -> HKT[F, J]:
    def ff(j: J) -> Tuple[A, B, C, D, E, Tuple[H, I]]:
      (a, b, c, d, e, h, i) = f(j)
      return (a, b, c, d, e, (h, i))
    return self.divide6(fa, fb, fc, fd, fe, self.tuple2(fh, fi), ff)
