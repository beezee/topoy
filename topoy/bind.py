from abc import ABC, abstractmethod
from topoy.hkt import HKT
from typing import Callable, Generic, TypeVar

F = TypeVar('F')
A = TypeVar('A')
FA = TypeVar('FA')
B = TypeVar('B')
FB = TypeVar('FB')

class Bind(ABC, Generic[F, A, FA, B, FB]):

  def __init__(self, fa: HKT[F, A, FA],
            f: Callable[[A], HKT[F, B, FB]]) -> None:
    (self._fa, self._f) = (fa, f)

  @abstractmethod
  def bind(self, fa: HKT[F, A, FA],
           f: Callable[[A], HKT[F, B, FB]]) -> HKT[F, B, FB]: pass

  def __call__(self) -> HKT[F, B, FB]:
    return self.bind(self._fa, self._f)
