from topoy.typevars import *
from typing import cast, Generic, Optional, Type, TypeVar

Implicits = {} # type: ignore
class Implicit(Generic[A]):

  def __init__(self, a: A) -> None:
    #tpe: Type[A] =  type(a) if tpe_a == None else tpe_a # type: ignore
    self._a = a

  def register(self, tpe: Type[A]) -> None:
    Implicits[tpe_a] = self._a # type: ignore

  @classmethod
  def resolve(cls, t: Type[A]) -> A:
    return cast(t, Implicits[t]) # type: ignore

from topoy.list import List

from topoy.hkt import HKT
class TCF: pass
class TC(Generic[A], HKT[TCF, A]):
  def __init__(self) -> None:
    pass

Implicit('foo').register(str)
Implicit[HKT[TCF, int]](TC[int]()).register(HKT[TCF, int])
Implicit[HKT[TCF, str]](TC[str]()).register(HKT[TCF, str])

from dataclasses import dataclass
@dataclass
class HasInt:
  num: int
  strs: str

  def __init__(self, ls: List[str]) -> None:
    self._ls = ls
    self._none = None

  def foo(self) -> None: pass

from typing import NamedTuple
NT = NamedTuple('NT', [('num', int), ('str', str)])

def Deriving(tpe: Type[F], a: A) -> None:
  [print(k + str(Implicit.resolve(HKT[tpe, v]))) for (k, v) in a.__dict__['__annotations__'].items()] # type: ignore
Deriving(TCF, HasInt)
Deriving(TCF, NT)
