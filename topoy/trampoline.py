from topoy.hkt import HKT
from topoy.sum import fold3, F1, F2, F3, Sum2, Sum3
from topoy.typevars import *
from typing import Callable, cast, Generic

class More(Generic[A]):
  
  def __init__(self, more: Callable[[], 'Trampoline[None, A]']) -> None:
    self.more = more

class Bind(Generic[X, A]):
  
  def __init__(self, sub: 'Trampoline[B, X]', 
               cont: Callable[[X], Trampoline[X, A]]) -> None:
    (self.sub, self.cont) = (sub, cont)
  

Trampoline = Sum3[Bind[X, A], A, More[A]]
class TrampF(Generic[X]):
  def inj(self, t: Trampoline[X, A]) -> HKT[TrampF[X], A]:
    return cast(HKT[TrampF[X], A], t)

  def proj(self, hkt: HKT[TrampF[X], A]) -> Trampoline[X, A]:
    return cast(Trampoline[X, A], hkt)

Res = Sum2[Callable[[], Trampoline[X, A]], A]
def resume(t: Trampoline[X, A]) -> Res[X, A]:
  return fold3[Bind[X, A], A, More[A], Res[X, A]]((
    lambda b: fold3[Bind[B, X], X, More[X], Res[X, A]]((
      lambda b2: resume(Bind[Any, X, A]( # type: ignore
        b2.sub, lambda x: Bind(b2.cont(x), b.cont))), # type: ignore
      lambda d: resume(b.cont(d)),
      lambda m: F1(lambda: F1(Bind(m.more(), b.cont)))))(
      b.sub),
    lambda d: F2(d),
    lambda m: F1(cast(Callable[[], Trampoline[X, A]], m.more))))(t)
