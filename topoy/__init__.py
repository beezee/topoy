from topoy.hkt import HKT
from topoy.list import BindList, HKList, ListApply, ListFunctor

if __name__ == '__main__':
  def x(i: int) -> str:
    return str(i)
  def x2(i: int) -> str:
    return x(i) + x(i)
  print(ListFunctor(HKList([1, 2, 3]), x2)())
  print(ListApply(HKList([1, 2, 3]), HKList([x, x2]))())
  print(BindList(HKList([1, 2, 3]), lambda x: HKList([str(x), str(x) + str(x)]))())
