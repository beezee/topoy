from topoy.hkt import HKT
from topoy.list import ListApply, ListFunctor, ListF, ListMonad

if __name__ == '__main__':
  def x(i: int) -> str:
    return str(i)
  def x2(i: int) -> str:
    return x(i) + x(i)
  print(ListFunctor().map(ListF.inj([1, 2, 3]), x2))
  print(ListApply().tuple(ListF.inj([1, 2, 3]), ListF.inj([3, 4, 5])))
  print(ListApply().ap(ListF.inj([1, 2, 3]), ListF.inj([x, x2])))
  print(ListMonad().bind(ListF.inj([1, 2, 3]), 
    lambda x: ListF.inj([str(x), str(x) + str(x)])))
