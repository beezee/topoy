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

  def apply(self, fb: '{classname}[B]',
            f: Callable[[A, B], C]) -> '{classname}[C]':   
    return self.tuple(fb).map(lambda x: f(x[0], x[1]))

  def apply3(self, fb: '{classname}[B]', fc: '{classname}[C]',
             f: Callable[[A, B, C], D]) -> '{classname}[D]':   
    return self.apply(fb.tuple(fc), 
      lambda a, bc: f(a, bc[0], bc[1]))

  def apply4(self, fb: '{classname}[B]', fc: '{classname}[C]',
             fd: '{classname}[D]',
             f: Callable[[A, B, C, D], E]) -> '{classname}[E]':
    return self.apply3(fb, fc.tuple(fd),
      lambda a, b, cd: f(a, b, cd[0], cd[1]))

  def apply5(self, fb: '{classname}[B]', fc: '{classname}[C]',
             fd: '{classname}[D]', fe: '{classname}[E]',
             f: Callable[[A, B, C, D, E], H]) -> '{classname}[H]':
    return self.apply4(fb, fc, fd.tuple(fe),
      lambda a, b, c, de: f(a, b, c, de[0], de[1]))

  def apply6(self, fb: '{classname}[B]', fc: '{classname}[C]',
             fd: '{classname}[D]', fe: '{classname}[E]', fh: '{classname}[H]',
             f: Callable[[A, B, C, D, E, H], I]) -> '{classname}[I]':
    return self.apply5(fb, fc, fd, fe.tuple(fh),
      lambda a, b, c, d, eh: f(a, b, c, d, eh[0], eh[1]))

  def apply7(self, fb: '{classname}[B]', fc: '{classname}[C]',
             fd: '{classname}[D]', fe: '{classname}[E]', fh: '{classname}[H]',
             fi: '{classname}[I]',
             f: Callable[[A, B, C, D, E, H, I], J]) -> '{classname}[J]':
    return self.apply6(fb, fc, fd, fe, fh.tuple(fi),
      lambda a, b, c, d, e, hi: f(a, b, c, d, e, hi[0], hi[1]))

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
