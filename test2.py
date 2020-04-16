from pkg.heap import MinHeap


b = MinHeap([['a', 12], ['b', 3]])

b.heapify_down()

print(b.display())
