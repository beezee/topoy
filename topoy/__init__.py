from topoy.either import LeftOf, RightOf
from topoy.either_ops import EitherOps
from topoy.list_data import ListApplicative
from topoy.list import List
from topoy.maybe import Maybe, MaybeApplicative
from typing import Callable

if __name__ == '__main__':
  def x(i: int) -> str:
    return str(i)
  def x2(i: int) -> str:
    return x(i) + x(i)
  print(List([1, 2, 3]).map(x2).run)
  print(List([1, 2, 3]).tuple(List([3, 4, 5])).run)
  print(List([1, 2, 3]).apply3(
    List([3, 4, 5]), 
    List[Callable[[int, int], str]](
      [lambda x, y: f"({x}, {y})", lambda x, y: str(x - y), 
       lambda x, y: str(x + y)]),
    lambda x, y, f: f(x, y)).run)
  print(List([1, 2, 3]).ap(List([x, x2])).run)
  print(List.proj(List([1, 2, 3])
    .traverse(ListApplicative(), lambda x: List([str(x), str(x) + str(x)])))
    .map(lambda x: x.run).run)
  print(List([1, 2, 3]).bind(
    lambda x: List([str(x), str(x) + str(x)])).run)
  print(RightOf[str].put(2).map_data(
    lambda x: x.bimap(lambda x: x + '!', lambda y: y + 2)))
  print(LeftOf[int].put('foo').map_data(
    lambda x: x.bimap(lambda x: x + '!', lambda y: y + 2)))
  print(RightOf[str].put(2).tuple(LeftOf[str].put('error').run))
  print(RightOf[str].put(2).tuple(RightOf[str].put('foo').run))
  print(LeftOf[int].put('error').tuple(RightOf[str].put('foo').run))
  print(List.proj(RightOf[str].put(2)
    .traverse(ListApplicative(), lambda x: List([x, x + 5])))
    .map(str).run)
  print(List.proj(LeftOf[int].put('foo')
    .traverse(ListApplicative(), lambda x: List([x, x + 5])))
    .map(str).run)
  print(Maybe.just(2))
  print(Maybe[int].none())
  print(Maybe.just(2).tuple(Maybe[str].none().run))
  print(Maybe.just(2).tuple(Maybe.just('foo').run))
  print(Maybe[int].none().tuple(Maybe.just('foo').run))
  print(EitherOps(Maybe.proj(RightOf[str].put(2)
    .traverse(MaybeApplicative(), lambda x: Maybe.just(x + 3).run)))
    .map(lambda x: x.map(lambda y: y + 2)))
  print(List.proj(Maybe.just(2)
    .traverse(ListApplicative(), lambda x: List([x, x + 5])))
    .map(str).run)
