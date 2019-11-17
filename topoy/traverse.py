from abc import abstractmethod
from topoy.hkt import HKT
from topoy.applicative import Applicative
from topoy.functor import Functor
from topoy.typevars import *
from typing import Callable

class Traverse(Functor[F]):

  @abstractmethod
  def traverse(self, 
    ap: Applicative[G], fa: HKT[F, A], 
    f: Callable[[A], HKT[G, B]]) -> HKT[G, HKT[F, B]]: pass

