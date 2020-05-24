from abc import abstractmethod
from topoy.arrow import Compose, Id
from topoy.either import Either
from topoy.either_data import LeftOf, RightOf
from topoy.functor import Functor
from topoy.hkt import HKT
from topoy.sum import *
from topoy.typevars import *
from typing import Callable

class Alt(Functor[F]):

  @abstractmethod
  def alt(self, fa1: HKT[F, A], fa2: HKT[F, A]) -> HKT[F, A]: pass

  def altly2(self, fa: HKT[F, A], fb: HKT[F, B],
             f: Callable[[Sum2[A, B]], C]) -> HKT[F, C]:
    return self.map(
      self.alt(
        self.map(fa, lambda x: Either[A, B](F1(x))),
        self.map(fb, lambda x: Either[A, B](F2(x)))),
      lambda x: f(x.run))

  def altly3(self, fa: HKT[F, A], fb: HKT[F, B],
             fc: HKT[F, C],
             f: Callable[[Sum3[A, B, C]], D]) -> HKT[F, D]:
    return self.altly2(fa,
      self.altly2(fb, fc, Id[Sum2[B, C]]()),
      Compose(f, fold2[A, Sum2[B, C], Sum3[A, B, C]]((
        F1, fold2[B, C, Sum3[A, B, C]]((F2, F3))))))

  def altly4(self, fa: HKT[F, A], fb: HKT[F, B],
             fc: HKT[F, C], fd: HKT[F, D],
             f: Callable[[Sum4[A, B, C, D]], E]) -> HKT[F, E]:
    return self.altly2(fa,
      self.altly3(fb, fc, fd, Id[Sum3[B, C, D]]()),
      Compose(f, fold2[A, Sum3[B, C, D], Sum4[A, B, C, D]]((
        F1, fold3[B, C, D, Sum4[A, B, C, D]]((F2, F3, F4))))))

  def altly5(self, fa: HKT[F, A], fb: HKT[F, B],
             fc: HKT[F, C], fd: HKT[F, D],
             fe: HKT[F, E],
             f: Callable[[Sum5[A, B, C, D, E]], G]) -> HKT[F, G]:
    return self.altly2(fa,
      self.altly4(fb, fc, fd, fe, Id[Sum4[B, C, D, E]]()),
      Compose(f, fold2[A, Sum4[B, C, D, E], Sum5[A, B, C, D, E]]((
        F1, fold4[B, C, D, E, Sum5[A, B, C, D, E]]((F2, F3, F4, F5))))))

  def altly6(self, fa: HKT[F, A], fb: HKT[F, B],
             fc: HKT[F, C], fd: HKT[F, D],
             fe: HKT[F, E], fh: HKT[F, H],
             f: Callable[[Sum6[A, B, C, D, E, H]], I]) -> HKT[F, I]:
    return self.altly2(fa,
      self.altly5(fb, fc, fd, fe, fh, Id[Sum5[B, C, D, E, H]]()),
      Compose(f, fold2[A, Sum5[B, C, D, E, H], Sum6[A, B, C, D, E, H]]((
        F1, fold5[B, C, D, E, H, Sum6[A, B, C, D, E, H]]((F2, F3, F4, F5, F6))))))

  def altly7(self, fa: HKT[F, A], fb: HKT[F, B],
             fc: HKT[F, C], fd: HKT[F, D],
             fe: HKT[F, E], fh: HKT[F, H],
             fi: HKT[F, I],
             f: Callable[[Sum7[A, B, C, D, E, H, I]], J]) -> HKT[F, J]:
    return self.altly2(fa,
      self.altly6(fb, fc, fd, fe, fh, fi, Id[Sum6[B, C, D, E, H, I]]()),
      Compose(f, fold2[A, Sum6[B, C, D, E, H, I], Sum7[A, B, C, D, E, H, I]]((
        F1, fold6[B, C, D, E, H, I, Sum7[A, B, C, D, E, H, I]](
        (F2, F3, F4, F5, F6, F7))))))
