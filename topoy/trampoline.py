from topoy.arrow import Compose
from topoy.hkt import HKT
from topoy.monad import Monad
from topoy.sum import fold2, fold3, F1, F2, F3, Sum2, Sum3
from topoy.typevars import *
from typing import Callable, cast, Generic

class Unit: pass

Trampoline = Sum3['Bind[X, A]', A, 'More[A]']
class More(Generic[A]):
  
  def __init__(self, more: Callable[[], 'Trampoline[None, A]']) -> None:
    self.more = more

class Bind(Generic[X, A]):
  
  def __init__(self, sub: 'Trampoline[B, X]', 
               cont: Callable[[X], 'Trampoline[X, A]']) -> None:
    (self.sub, self.cont) = (sub, cont)

class TrampF():
  @staticmethod
  def inj(t: 'Trampoline[X, A]') -> HKT['TrampF', A]:
    return cast(HKT[TrampF, A], t)

  @staticmethod
  def proj(hkt: HKT['TrampF', A]) -> 'Trampoline[Unit, A]':
    return cast('Trampoline[Unit, A]', hkt)

Res = Sum2[Callable[[], HKT[TrampF, A]], A]
def resume(t: HKT[TrampF, A]) -> Res[A]:
  return fold3[Bind[X, A], A, More[A], Res[A]]((
    lambda b: fold3[Bind[B, X], X, More[X], Res[A]]((
      lambda b2: resume(TrampF.inj(Bind[Any, X, A]( # type: ignore
        b2.sub, lambda x: Bind(b2.cont(x), b.cont)))), # type: ignore
      lambda d: resume(TrampF.inj(b.cont(d))),
      lambda m: F1(lambda: TrampF.inj(F1(Bind(m.more(), b.cont))))))( # type: ignore
      b.sub),
    lambda d: F2(d),
    lambda m: F1(cast(Callable[[], HKT[TrampF, A]], 
      Compose(TrampF.inj, m.more)))))( # type: ignore
    TrampF.proj(t))

def go(t: HKT[TrampF, A]) -> 'Trampoline[Unit, A]':
  return fold2[Callable[[], HKT[TrampF, A]], A, 'Trampoline[Unit, A]'](
      (lambda x: go(x()),
     lambda x: F2(x)))(resume(t))

class TrampolineMonad(Monad[TrampF]):
  
  def bind(self, fa: HKT[TrampF, A],
            afb: Callable[[A], HKT[TrampF, B]]) -> HKT[TrampF, B]:
    return TrampF.inj(F1(Bind(fa, Compose(TrampF.proj, afb)))) # type: ignore 

  def map(self, fa: HKT[TrampF, A],
          f: Callable[[A], B]) -> HKT[TrampF, B]:
    return self.bind(fa, Compose(TrampF.inj, Compose(F2, f))) # type: ignore
