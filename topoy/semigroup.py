from abc import ABC, abstractmethod
from topoy.typevars import *
from typing import Generic

class Semigroup(Generic[A]):

  @abstractmethod
  def append(self, a1: A, a2: A) -> A: pass
