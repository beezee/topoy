from abc import abstractmethod
from topoy.arrow import Id
from topoy.contravariant import Contravariant
from topoy.hkt import HKT
from topoy.typevars import *
from typing import Callable, Tuple

class Divide(Contravariant[F]):

  @abstractmethod
  def divide(self, fa: HKT[F, A], fb: HKT[F, B], 
             cab: Callable[[C], Tuple[A, B]]) -> HKT[F, C]: pass

  def tuple2(self, fa: HKT[F, A], fb: HKT[F, B]) -> HKT[F, Tuple[A, B]]:
    return self.divide(fa, fb, Id[Tuple[A, B]]())
    
