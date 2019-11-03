from abc import ABC, abstractmethod
from topoy.hkt import HKT
from typing import Callable, Generic, TypeVar

F = TypeVar('F')
A = TypeVar('A')
FA = TypeVar('FA')
B = TypeVar('B')
FB = TypeVar('FB')
FAB = TypeVar('FAB')

class Apply(ABC, Generic[F, A, FA, B, FB, FAB]):

  def __init__(self, fa: HKT[F, A, FA],
            fab: HKT[F, Callable[[A], B], FAB]) -> None:
    (self._fa, self._fab) = (fa, fab)

  @abstractmethod
  def ap(self, fa: HKT[F, A, FA],
       fab: HKT[F, Callable[[A], B], FAB]) -> HKT[F, B, FB]: pass

  def __call__(self) -> HKT[F, B, FB]:
    return self.ap(self._fa, self._fab)
