from abc import abstractmethod
from topoy.hkt import HKT
from topoy.apply import Apply
from topoy.typevars import *


class Applicative(Apply[F]):

  #@abstractmethod
  def pure(self, a: A) -> HKT[F, A]: pass
