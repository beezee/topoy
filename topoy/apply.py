from abc import abstractmethod
from topoy.functor import Functor
from topoy.hkt import HKT
from topoy.typevars import *
from typing import Callable, Generic, Tuple

class Apply(Functor[F]):

  @abstractmethod
  def ap(self, fa: HKT[F, A],
       fab: HKT[F, Callable[[A], B]]) -> HKT[F, B]: pass

  def apply(self, fa: HKT[F, A], fb: HKT[F, B],
            f: Callable[[A, B], C]) -> HKT[F, C]:   
    return self.map(self.tuple(fa, fb), lambda x: f(x[0], x[1]))

  def apply3(self, fa: HKT[F, A], fb: HKT[F, B], fc: HKT[F, C],
             f: Callable[[A, B, C], D]) -> HKT[F, D]:   
    return self.apply(fa, self.tuple(fb, fc), 
      lambda a, bc: f(a, bc[0], bc[1]))

  def apply4(self, fa: HKT[F, A], fb: HKT[F, B], fc: HKT[F, C],
             fd: HKT[F, D],
             f: Callable[[A, B, C, D], E]) -> HKT[F, E]:
    return self.apply3(fa, fb, self.tuple(fc, fd),
      lambda a, b, cd: f(a, b, cd[0], cd[1]))

  def apply5(self, fa: HKT[F, A], fb: HKT[F, B], fc: HKT[F, C],
             fd: HKT[F, D], fe: HKT[F, E],
             f: Callable[[A, B, C, D, E], H]) -> HKT[F, H]:
    return self.apply4(fa, fb, fc, self.tuple(fd, fe),
      lambda a, b, c, de: f(a, b, c, de[0], de[1]))

  def apply6(self, fa: HKT[F, A], fb: HKT[F, B], fc: HKT[F, C],
             fd: HKT[F, D], fe: HKT[F, E], fh: HKT[F, H],
             f: Callable[[A, B, C, D, E, H], I]) -> HKT[F, I]:
    return self.apply5(fa, fb, fc, fd, self.tuple(fe, fh),
      lambda a, b, c, d, eh: f(a, b, c, d, eh[0], eh[1]))

  def apply7(self, fa: HKT[F, A], fb: HKT[F, B], fc: HKT[F, C],
             fd: HKT[F, D], fe: HKT[F, E], fh: HKT[F, H],
             fi: HKT[F, I],
             f: Callable[[A, B, C, D, E, H, I], J]) -> HKT[F, J]:
    return self.apply6(fa, fb, fc, fd, fe, self.tuple(fh, fi),
      lambda a, b, c, d, e, hi: f(a, b, c, d, e, hi[0], hi[1]))

  def tuple(self, fa: HKT[F, A], 
            fb: HKT[F, B]) -> HKT[F, Tuple[A, B]]:
    def tup(b: B) -> Callable[[A], Tuple[A, B]]:
      def x(a: A) -> Tuple[A, B]:
        return (a, b)
      return x
    return self.ap(fa, self.map(fb, tup))
