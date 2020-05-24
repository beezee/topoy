from abc import ABC, abstractmethod
from topoy.hkt import HKT
from topoy.typevars import *
from typing import cast, Callable, Generic, TypeVar
from typing import Tuple
from topoy.applicative import Applicative

import topoy.list_data as instances

class List(ABC, instances.ListData[A]):
  @staticmethod
  def inj(l: 'List[A]') -> 'HKT[instances.ListF, A]':
    return cast(HKT[instances.ListF, A], l)

  @staticmethod
  def proj(hkt: 'HKT[instances.ListF, A]') -> 'List[A]':
    return cast('List[A]', hkt)

  def map(self, f: Callable[[A], B]) -> 'List[B]':
    return List.proj(instances.ListFunctor().map(self, f))
  
  def bind(
    self, f: Callable[[A], 'List[B]']
  ) -> 'List[B]':
    return List.proj(instances.ListMonad().bind(self, f))
  
  def ap(
    self, fab: 'List[Callable[[A], B]]'
  ) -> 'List[B]':
    return List.proj(
      instances.ListApply().ap(self, fab))

  def apply(self, fb: 'List[B]',
            f: Callable[[A, B], C]) -> 'List[C]':   
    return self.tuple(fb).map(lambda x: f(x[0], x[1]))

  def apply3(self, fb: 'List[B]', fc: 'List[C]',
             f: Callable[[A, B, C], D]) -> 'List[D]':   
    return self.apply(fb.tuple(fc), 
      lambda a, bc: f(a, bc[0], bc[1]))

  def apply4(self, fb: 'List[B]', fc: 'List[C]',
             fd: 'List[D]',
             f: Callable[[A, B, C, D], E]) -> 'List[E]':
    return self.apply3(fb, fc.tuple(fd),
      lambda a, b, cd: f(a, b, cd[0], cd[1]))

  def apply5(self, fb: 'List[B]', fc: 'List[C]',
             fd: 'List[D]', fe: 'List[E]',
             f: Callable[[A, B, C, D, E], H]) -> 'List[H]':
    return self.apply4(fb, fc, fd.tuple(fe),
      lambda a, b, c, de: f(a, b, c, de[0], de[1]))

  def apply6(self, fb: 'List[B]', fc: 'List[C]',
             fd: 'List[D]', fe: 'List[E]', fh: 'List[H]',
             f: Callable[[A, B, C, D, E, H], I]) -> 'List[I]':
    return self.apply5(fb, fc, fd, fe.tuple(fh),
      lambda a, b, c, d, eh: f(a, b, c, d, eh[0], eh[1]))

  def apply7(self, fb: 'List[B]', fc: 'List[C]',
             fd: 'List[D]', fe: 'List[E]', fh: 'List[H]',
             fi: 'List[I]',
             f: Callable[[A, B, C, D, E, H, I], J]) -> 'List[J]':
    return self.apply6(fb, fc, fd, fe, fh.tuple(fi),
      lambda a, b, c, d, e, hi: f(a, b, c, d, e, hi[0], hi[1]))

  def tuple(
    self, fb: 'List[B]'
  ) -> 'List[Tuple[A, B]]':
    return List.proj(
      instances.ListApply().tuple(self, fb))
  
  def traverse(self, ap: Applicative[G],
    f: Callable[[A], HKT[G, B]]) -> HKT[G, 'List[B]']:
      return ap.map(
        instances.ListTraverse().traverse(ap, self, f),
        List.proj)
  
