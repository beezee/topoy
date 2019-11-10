from topoy.arrow import Id
from topoy.contravariant import Contravariant
from topoy.hkt import HKT
from topoy.typevars import *
from typing import Callable, Tuple

class Divide(Contravariant[F]):

  @classmethod
  def divide(cls, fa: HKT[F, A], fb: HKT[F, B], 
             cab: Callable[[C], Tuple[A, B]]) -> HKT[F, C]: pass

  @classmethod
  def tuple2(cls, fa: HKT[F, A], fb: HKT[F, B]) -> HKT[F, Tuple[A, B]]:
    return cls.divide(fa, fb, Id[Tuple[A, B]]())
    
