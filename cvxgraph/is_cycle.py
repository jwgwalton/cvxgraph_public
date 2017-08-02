#!/usr/bin/env python3

def is_cycle(adjacency_list):
  start_index,end_index=adjacency_list[0]
  initial_index=start_index
  path_length,n=0,len(adjacency_list)
  cycle=False
  #print(path_length,start_index,end_index)
  while path_length<n:

    for edge in adjacency_list:
      edge_found = False
      if edge==(start_index,end_index): continue # if found itself
      if end_index in edge:
        edge_found=True
        k=edge.index(end_index)
        break
    if edge_found:
      start_index,end_index=end_index,edge[1-k] # iterate along cycle
    else: 
      return cycle # edge not in list, no cycle
    #print(path_length,start_index,end_index)
    if end_index==initial_index: 
      cycle=True
      break
    path_length+=1

  return cycle




if __name__ == '__main__':
  A1 = ((0,5),(5,13),(13,14),(14,6),(6,1),(1,7),(7,2),(2,8),(8,11),(11,15),(15,10),(10,9),(9,4),(4,12),(12,3),(3,0),)

  print(is_cycle(A1))

  # CHECK DOESN'T BREAK IF RANDOM NODE WHICH IS OUT OF RANGE IN BEGINNING OF SEQUENCE
  A2 = ((0,25),(5,13),(13,14),(14,6),(6,1),(1,7),(7,2),(2,8),(8,11),(11,15),(15,10),(10,9),(9,4),(4,12),(12,3),(3,0),)

  print(is_cycle(A2))

  # CHECK DOESN'T BREAK IF RANDOM NODE WHICH IS OUT OF RANGE IN END OF SEQUENCE (12,23)
  A3 = ((0,5),(5,13),(13,14),(14,6),(6,1),(1,7),(7,2),(2,8),(8,11),(11,15),(15,10),(10,9),(9,4),(4,12),(12,23),(3,0),)

  print(is_cycle(A3))

  # check works with randomly organised cycle

  A4 = ((5,0),(13,5),(13,14),(14,6),(6,1),(1,7),(7,2),(2,8),(8,11),(11,15),(15,10),(10,9),(9,4),(4,12),(12,3),(3,0),)

  print(is_cycle(A4)) # should be true
