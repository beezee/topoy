from topoy.hkt import HKT
from topoy.apply import tuple
from topoy.list import ListApplicative, List
from topoy.maybe import Maybe, MaybeF, MaybeFunctor
from topoy.sum import F1, F2

if __name__ == '__main__':
  def x(i: int) -> str:
    return str(i)
  def x2(i: int) -> str:
    return x(i) + x(i)
  print(List([1, 2, 3]).map(x2).run)
  print(List([1, 2, 3]).tuple(List([3, 4, 5])).run)
  print(List([1, 2, 3]).ap(List([x, x2])).run)
  print(List([1, 2, 3]).traverse(ListApplicative(), 
    lambda x: List([str(x), str(x) + str(x)])).map(lambda x: x.run).run)
  print(List([1, 2, 3]).bind(
    lambda x: List([str(x), str(x) + str(x)])).run)
  a: Maybe[int] = F2(3)
  b: Maybe[int] = F1(None)
  print(MaybeFunctor().map(MaybeF.inj(a), lambda x: x + 1))
  print(MaybeFunctor().map(MaybeF.inj(b), lambda x: x + 1))
