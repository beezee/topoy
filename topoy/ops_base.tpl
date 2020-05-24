from abc import ABC, abstractmethod
from topoy.hkt import HKT
from topoy.typevars import *
from typing import cast, Callable, Generic, TypeVar
[[[cog
import cog
functor = globals().get("functor")
monad = globals().get("monad")
apply = globals().get("apply")
traverse = globals().get("traverse")

if apply:
  cog.outl("from typing import Tuple")

if traverse:
  cog.outl("from topoy.applicative import Applicative")

cog.out(f"""
import {packagename} as instances

class {classname}(ABC, instances.{superclass}[A]):
  @staticmethod
  def inj(l: '{classname}[A]') -> 'HKT[instances.{tag}, A]':
    return cast(HKT[instances.{tag}, A], l)

  @staticmethod
  def proj(hkt: 'HKT[instances.{tag}, A]') -> '{classname}[A]':
    return cast('{classname}[A]', hkt)
""")
  
if functor:
  cog.out(f"""
  def map(self, f: Callable[[A], B]) -> '{classname}[B]':
    return {classname}.proj(instances.{functor}().map(self, f))
  """)

if monad:
  cog.out(f"""
  def bind(
    self, f: Callable[[A], '{classname}[B]']
  ) -> '{classname}[B]':
    return {classname}.proj(instances.{monad}().bind(self, f))
  """)

if apply:
  cog.out(f"""
  def ap(
    self, fab: '{classname}[Callable[[A], B]]'
  ) -> '{classname}[B]':
    return {classname}.proj(
      instances.{apply}().ap(self, fab))

  def tuple(
    self, fb: '{classname}[B]'
  ) -> '{classname}[Tuple[A, B]]':
    return {classname}.proj(
      instances.{apply}().tuple(self, fb))
  """)

if traverse:
  cog.out(f"""
  def traverse(self, ap: Applicative[G],
    f: Callable[[A], HKT[G, B]]) -> HKT[G, '{classname}[B]']:
      return ap.map(
        instances.{traverse}().traverse(ap, self, f),
        {classname}.proj)
  """)
]]]
[[[end]]]
