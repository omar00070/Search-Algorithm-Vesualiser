from pkg.heap import MinHeap

graph = {
	'a': {'b': 2, 'd': 6},
	'b': {'c': 1, 'd': 3, 'e': 6},
	'c': {'d': 1},
	'd': {'e': 3},
	'e': {'f': 2},
	'f':{}
}


visited = []
bck_track = {}
start = 'b'
unvisited = {}
infinity = 9999999
end = 'f'
unseen = graph
for node in graph:
	if node == start:
		unvisited[node] = 0
	else:
		unvisited[node] = infinity
print(unvisited)
while unseen:
	min_node = None
	min_val = infinity + 1
	for node in unvisited:
		if node not in visited:
			if unvisited[node] < min_val:
				min_node, min_val = node, unvisited[node]
	for child, weight in graph[min_node].items():
		if unvisited[child]  > min_val + weight:
			unvisited[child] = min_val + weight
			bck_track[child] = min_node
	unseen.pop(min_node)
	visited.append(min_node)
	print(bck_track)
	print(unvisited)
print(bck_track)



node name is gonna be (x, y) coordinates:
unseen are going to be the whole graph
graph = {(x, y): L U R D, if valid default weights are going to be 1 all}
unseen = graph
unvisited = cell and weight 
visted = []
path is going to be self.bck_track

