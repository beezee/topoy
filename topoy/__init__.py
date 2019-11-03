from topoy.hkt import HKT
from topoy.list import ListApplicative, ListFunctor
from topoy.list import ListTraverse, ListF, ListMonad

if __name__ == '__main__':
  def x(i: int) -> str:
    return str(i)
  def x2(i: int) -> str:
    return x(i) + x(i)
  print(ListFunctor().map(ListF.inj([1, 2, 3]), x2))
  print(ListApplicative().tuple(ListF.inj([1, 2, 3]), ListF.inj([3, 4, 5])))
  print(ListApplicative().ap(ListF.inj([1, 2, 3]), ListF.inj([x, x2])))
  print(ListTraverse().traverse(ListApplicative(), ListF.inj([1, 2, 3]), 
    lambda x: ListF.inj([str(x), str(x) + str(x)])))
  print(ListMonad().bind(ListF.inj([1, 2, 3]), 
    lambda x: ListF.inj([str(x), str(x) + str(x)])))
