#!/usr/bin/env python3
import copy
g0={
 1: {3,4},
 3: {4,6,7},
 4: {7},
 6: {7}
}


g1={
 0:{1,4},
 1:{2},
 2:{5},
 5:{8},
 8:{4}
}


g=copy.copy(g0) # needed 


for i in g1:
  g.setdefault(i,set()).add(g1[i])

print(g0)
print(g1)
print(g)
