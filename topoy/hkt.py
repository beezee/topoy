from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar, List

F = TypeVar('F')
A = TypeVar('A')
FA = TypeVar('FA')

@dataclass
class HKT(Generic[F, A, FA]):
  run: FA
