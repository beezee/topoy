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
  
