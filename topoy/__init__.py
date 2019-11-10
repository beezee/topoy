from topoy.hkt import HKT
from topoy.apply import tuple
from topoy.either import LeftOf, RightOf
from topoy.list import ListApplicative, List
from topoy.maybe import Maybe, MaybeApplicative
from topoy.sum import F1, F2

if __name__ == '__main__':
  def x(i: int) -> str:
    return str(i)
  def x2(i: int) -> str:
    return x(i) + x(i)
  print(List([1, 2, 3]).map(x2).run)
  print(List([1, 2, 3]).tuple(List([3, 4, 5])).run)
  print(List([1, 2, 3]).ap(List([x, x2])).run)
  print(List.proj(List([1, 2, 3])
    .traverse(ListApplicative(), lambda x: List([str(x), str(x) + str(x)])))
    .map(lambda x: x.run).run)
  print(List([1, 2, 3]).bind(
    lambda x: List([str(x), str(x) + str(x)])).run)
  print(RightOf[str].put(2).bimap(lambda x: x + '!', lambda y: y + 2))
  print(LeftOf[int].put('foo').bimap(lambda x: x + '!', lambda y: y + 2))
  print(List.proj(RightOf[str].put(2)
    .traverse(ListApplicative(), lambda x: List([x, x + 5])))
    .map(str).run)
  print(List.proj(LeftOf[int].put('foo')
    .traverse(ListApplicative(), lambda x: List([x, x + 5])))
    .map(str).run)
  print(Maybe.just(2))
  print(Maybe[int].none())
  print(Maybe.proj(RightOf[str].put(2)
    .traverse(MaybeApplicative(), lambda x: Maybe.just(x + 3)))
    .map(lambda x: x.map(lambda y: y + 2)))
  print(List.proj(Maybe.just(2)
    .traverse(ListApplicative(), lambda x: List([x, x + 5])))
    .map(str).run)
