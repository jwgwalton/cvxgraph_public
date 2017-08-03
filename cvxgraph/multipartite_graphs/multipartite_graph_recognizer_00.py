#!/usr/bin/env python3
# Keith Briggs 2017-08-02 was try_set_partitions_00.py 

from itertools import combinations

class Multipartite_graph_recognizer:

  def __init__(s,p,g):
    # given a partition p (e.g. (2,5,3)) and a graph g,
    # text whether g is p-multipartite
    s.p,s.g=p,g
    s.n,s.k=sum(p),len(p)
    s.a=[0]+[i-1 for i in range(1,s.n+1)]
    s.match=None
    
  def check(s):
    s.S_4_23a(s.n,s.k)
    return s.match is not None

  def check_graph(s,a):
    # recognize a multipartite graph
    for i in s.g:
      ai=s.a[i] # block to which node i belongs
      for j in s.g[i]:
        if s.a[j]==ai: return # neighbour is in same block
    s.match=a[:]

  def S_4_23a(s,n,k): # set partitions with exactly k blocks
    if n==k: # got a new partition
      c=tuple(s.a[1:].count(y) for y in range(len(s.p)))
      if c==s.p: # blocksizes match p tuple
        s.check_graph(s.a[1:])
    else:
      for i in range(k):
        s.a[n]=i
        s.S_4_23a(n-1,k)
        s.a[n]=n-1
      if k>1:
        s.a[n]=k-1
        s.S_4_23a(n-1,k-1)
        s.a[n]=n-1

def generate_complete_multipartite_graph(p):
  n=sum(p)
  g=dict((i,[]) for i in range(n))
  i,spans=0,[]
  for pi in p:
    spans.append((i,i+pi))
    i+=pi
  for c0,c1 in combinations(spans,2):
    for i in range(*c0):
      for j in range(*c1):
        g[i].append(j)
        g[j].append(i)
  return g

if __name__=='__main__':
  for p in [(3,4),(3,3,3),(2,5,3,),(2,2,4,5),]:
    g=generate_complete_multipartite_graph(p)
    print('p=',p,'\ng=',g)
    multipartite_graph_recognizer=Multipartite_graph_recognizer(p,g)
    ok=multipartite_graph_recognizer.check()
    if ok:
      print('match found:',multipartite_graph_recognizer.match)
