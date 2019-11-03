from abc import ABC, abstractmethod
from topoy.typevars import *
from typing import Callable, Generic, List

class HKT(Generic[F, A]):
  def __init__(self) -> None:
    assert False
