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

ops_class = f"{classname}Ops"
data_class = f"instances.{classname}"

cog.out(f"""
import {packagename} as instances

class {ops_class}(ABC, Generic[X, A]):

  def __init__(self, run: {data_class}[X, A]) -> None:
    self.run = run

  def map_data(
    self, fn: Callable[[{data_class}[X, A]], {data_class}[B, Y]]
  ) -> '{ops_class}[B, Y]':
    return {ops_class}(fn(self.run))
    
  @staticmethod
  def inj(l: '{data_class}[X, A]') -> 'HKT[instances.{tag}[X], A]':
    return cast('HKT[instances.{tag}[X], A]', l)

  @staticmethod
  def proj(hkt: 'HKT[instances.{tag}[X], A]') -> '{data_class}[X, A]':
    return cast('{data_class}[X, A]', hkt)

  @staticmethod
  def lift(hkt: 'HKT[instances.{tag}[X], A]') -> '{ops_class}[X, A]':
    return {ops_class}({ops_class}.proj(hkt))

  def __str__(self) -> str:
    return str(self.run)
""")
  
if functor:
  cog.out(f"""
  def map(self, f: Callable[[A], B]) -> '{ops_class}[X, B]':
    return {ops_class}.lift(instances.{functor}[X]().map(self.run, f))
  """)

if monad:
  cog.out(f"""
  def bind(
    self, f: Callable[[A], '{data_class}[X, B]']
  ) -> '{ops_class}[X, B]':
    return {ops_class}.lift(instances.{monad}[X]().bind(self.run, f))
  """)

if apply:
  cog.out(f"""
  def ap(
    self, fab: '{data_class}[X, Callable[[A], B]]'
  ) -> '{ops_class}[X, B]':
    return {ops_class}.lift(
      instances.{apply}[X]().ap(self.run, fab))

  def apply(self, fb: '{data_class}[X, B]',
            f: Callable[[A, B], C]) -> '{ops_class}[X, C]':
    return self.tuple(fb).map(lambda x: f(x[0], x[1]))

  def apply3(self, fb: '{data_class}[X, B]', fc: '{data_class}[X, C]',
             f: Callable[[A, B, C], D]) -> '{ops_class}[X, D]':   
    return self.apply({ops_class}(fb).tuple(fc).run, 
      lambda a, bc: f(a, bc[0], bc[1]))

  def apply4(self, fb: '{data_class}[X, B]', fc: '{data_class}[X, C]',
             fd: '{data_class}[X, D]',
             f: Callable[[A, B, C, D], E]) -> '{ops_class}[X, E]':
    return self.apply3(fb, {ops_class}(fc).tuple(fd).run,
      lambda a, b, cd: f(a, b, cd[0], cd[1]))

  def apply5(self, fb: '{data_class}[X, B]', fc: '{data_class}[X, C]',
             fd: '{data_class}[X, D]', fe: '{data_class}[X, E]',
             f: Callable[[A, B, C, D, E], H]) -> '{ops_class}[X, H]':
    return self.apply4(fb, fc, {ops_class}(fd).tuple(fe).run,
      lambda a, b, c, de: f(a, b, c, de[0], de[1]))

  def apply6(self, fb: '{data_class}[X, B]', fc: '{data_class}[X, C]',
             fd: '{data_class}[X, D]', fe: '{data_class}[X, E]', fh: '{data_class}[X, H]',
             f: Callable[[A, B, C, D, E, H], I]) -> '{ops_class}[X, I]':
    return self.apply5(fb, fc, fd, {ops_class}(fe).tuple(fh).run,
      lambda a, b, c, d, eh: f(a, b, c, d, eh[0], eh[1]))

  def apply7(self, fb: '{data_class}[X, B]', fc: '{data_class}[X, C]',
             fd: '{data_class}[X, D]', fe: '{data_class}[X, E]', fh: '{data_class}[X, H]',
             fi: '{data_class}[X, I]',
             f: Callable[[A, B, C, D, E, H, I], J]) -> '{ops_class}[X, J]':
    return self.apply6(fb, fc, fd, fe, {ops_class}(fh).tuple(fi).run,
      lambda a, b, c, d, e, hi: f(a, b, c, d, e, hi[0], hi[1]))

  def tuple(
    self, fb: '{data_class}[X, B]'
  ) -> '{ops_class}[X, Tuple[A, B]]':
    return {ops_class}.lift(
      instances.{apply}[X]().tuple(self.run, fb))
  """)

if traverse:
  cog.out(f"""
  def traverse(self, ap: Applicative[G],
    f: Callable[[A], HKT[G, B]]) -> HKT[G, '{ops_class}[X, B]']:
      return ap.map(
        instances.{traverse}[X]().traverse(ap, self.run, f),
        {ops_class}.lift)
  """)
]]]
[[[end]]]

