from abc import abstractmethod
from topoy.arrow import Id, Compose
from topoy.contravariant import Contravariant
from topoy.hkt import HKT
from topoy.sum import *
from topoy.typevars import *
from typing import Callable

class Decide(Contravariant[F]):

  def choose1(self, fa: HKT[F, A], f: Callable[[C], A]) -> HKT[F, C]:
    return self.contramap(fa, f)

  @abstractmethod
  def choose(self, a: HKT[F, A], b: HKT[F, B],
              f: Callable[[C], Sum2[A, B]]) -> HKT[F, C]: pass

  def choose3(self, a: HKT[F, A], b: HKT[F, B],
              c: HKT[F, C], f: Callable[[D], Sum3[A, B, C]]) -> HKT[F, D]:
    bc = self.choose(b, c, Id[Sum2[B, C]]())
    return self.choose(a, bc, 
      Compose(fold3[A, B, C, Sum2[A, Sum2[B, C]]](
          (F1, lambda b: F2(F1(b)), lambda c: F2(F2(c)))), f))

  def choose4(self, a: HKT[F, A], b: HKT[F, B],
              c: HKT[F, C], d: HKT[F, D],
              f: Callable[[E], Sum4[A, B, C, D]]) -> HKT[F, E]:
    bcd = self.choose3(b, c, d, Id[Sum3[B, C, D]]())
    return self.choose(a, bcd, 
      Compose(fold4[A, B, C, D, Sum2[A, Sum3[B, C, D]]](
          (F1, lambda b: F2(F1(b)), lambda c: F2(F2(c)),
           lambda d: F2(F3(d)))), f))

  def choose5(self, a: HKT[F, A], b: HKT[F, B],
              c: HKT[F, C], d: HKT[F, D], e: HKT[F, E],
              f: Callable[[H], Sum5[A, B, C, D, E]]) -> HKT[F, H]:
    bcde = self.choose4(b, c, d, e, Id[Sum4[B, C, D, E]]())
    return self.choose(a, bcde,
      Compose(fold5[A, B, C, D, E, Sum2[A, Sum4[B, C, D, E]]](
        (F1, lambda b: F2(F1(b)), lambda c: F2(F2(c)),
         lambda d: F2(F3(d)), lambda e: F2(F4(e)))), f))
