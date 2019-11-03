from abc import abstractmethod
from topoy.semigroup import Semigroup
from topoy.typevars import *
from typing import Generic

class Monoid(Generic[A], Semigroup[A]):

  @abstractmethod
  def zero(self) -> A: pass
