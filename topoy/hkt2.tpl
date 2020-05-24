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

class {classname}(ABC, instances.{superclass}[X, A]):
  @staticmethod
  def inj(l: '{classname}[X, A]') -> 'HKT[instances.{tag}[X], A]':
    return cast('HKT[instances.{tag}[X], A]', l)

  @staticmethod
  def proj(hkt: 'HKT[instances.{tag}[X], A]') -> '{classname}[X, A]':
    return cast('{classname}[X, A]', hkt)
""")
  
if functor:
  cog.out(f"""
  def map(self, f: Callable[[A], B]) -> '{classname}[X, B]':
    return {classname}.proj(instances.{functor}[X]().map(self, f))
  """)

if monad:
  cog.out(f"""
  def bind(
    self, f: Callable[[A], '{classname}[X, B]']
  ) -> '{classname}[X, B]':
    return {classname}.proj(instances.{monad}[X]().bind(self, f))
  """)

if apply:
  cog.out(f"""
  def ap(
    self, fab: '{classname}[X, Callable[[A], B]]'
  ) -> '{classname}[X, B]':
    return {classname}.proj(
      instances.{apply}[X]().ap(self, fab))

  def apply(self, fb: '{classname}[X, B]',
            f: Callable[[A, B], C]) -> '{classname}[X, C]':
    return self.tuple(fb).map(lambda x: f(x[0], x[1]))

  def apply3(self, fb: '{classname}[X, B]', fc: '{classname}[X, C]',
             f: Callable[[A, B, C], D]) -> '{classname}[X, D]':   
    return self.apply(fb.tuple(fc), 
      lambda a, bc: f(a, bc[0], bc[1]))

  def apply4(self, fb: '{classname}[X, B]', fc: '{classname}[X, C]',
             fd: '{classname}[X, D]',
             f: Callable[[A, B, C, D], E]) -> '{classname}[X, E]':
    return self.apply3(fb, fc.tuple(fd),
      lambda a, b, cd: f(a, b, cd[0], cd[1]))

  def apply5(self, fb: '{classname}[X, B]', fc: '{classname}[X, C]',
             fd: '{classname}[X, D]', fe: '{classname}[X, E]',
             f: Callable[[A, B, C, D, E], H]) -> '{classname}[X, H]':
    return self.apply4(fb, fc, fd.tuple(fe),
      lambda a, b, c, de: f(a, b, c, de[0], de[1]))

  def apply6(self, fb: '{classname}[X, B]', fc: '{classname}[X, C]',
             fd: '{classname}[X, D]', fe: '{classname}[X, E]', fh: '{classname}[X, H]',
             f: Callable[[A, B, C, D, E, H], I]) -> '{classname}[X, I]':
    return self.apply5(fb, fc, fd, fe.tuple(fh),
      lambda a, b, c, d, eh: f(a, b, c, d, eh[0], eh[1]))

  def apply7(self, fb: '{classname}[X, B]', fc: '{classname}[X, C]',
             fd: '{classname}[X, D]', fe: '{classname}[X, E]', fh: '{classname}[X, H]',
             fi: '{classname}[X, I]',
             f: Callable[[A, B, C, D, E, H, I], J]) -> '{classname}[X, J]':
    return self.apply6(fb, fc, fd, fe, fh.tuple(fi),
      lambda a, b, c, d, e, hi: f(a, b, c, d, e, hi[0], hi[1]))

  def tuple(
    self, fb: '{classname}[X, B]'
  ) -> '{classname}[X, Tuple[A, B]]':
    return {classname}.proj(
      instances.{apply}[X]().tuple(self, fb))
  """)

if traverse:
  cog.out(f"""
  def traverse(self, ap: Applicative[G],
    f: Callable[[A], HKT[G, B]]) -> HKT[G, '{classname}[X, B]']:
      return ap.map(
        instances.{traverse}[X]().traverse(ap, self, f),
        {classname}.proj)
  """)
]]]
[[[end]]]

