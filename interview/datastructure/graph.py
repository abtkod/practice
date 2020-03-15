class Graph:
	'''
	Graph represented by adjacency list
	'''
	def __init__(self, is_directed=True, is_weighted=False):
		self._is_directed = is_directed
		self._is_weighted = is_weighted
		self._adjlist = {}

	@property
	def is_directed(self):
		return self._is_directed

	@property
	def is_weighted(self):
		return self._is_weighted
	
	def ncount(self):
		return len(self._adjlist)

	def ecount(self):
		c = sum(len(x) for x in self._adjlist.values())
		return c if self.is_directed else c/2

	def add_node(self, n):
		assert(n not in self._adjlist), 'node already exists.'
		self._adjlist[n] = set()

	def add_edge(self, n1, n2, weight=None):
		assert(n1 in self._adjlist), 'node does not exist.'
		assert(n2 in self._adjlist), 'node does not exist.'
		self._adjlist[n1].add(n2) if not self._is_weighted else self._adjlist[n1].add((n2, weight))
		if not self._is_directed:
			self._adjlist[n2].add(n1) if not self._is_weighted else self._adjlist[n2].add((n1, weight))

	def dfs(self):		
		def search(root, output, visited):
			output.append(root)
			visited[root] = True
			for nbr in self._adjlist[root]:
				if not visited[nbr]:
					search(nbr, output, visited)
		output = []
		visited = {x:False for x in self._adjlist}
		notvisited = (node for node in self._adjlist if not visited[node])
		for root in notvisited:
			search(root, output, visited)
		return output
		
	def bfs(self):		
		def search(root, output, marked):
			from collections import deque
			q = deque()
			q.append(root)
			marked[root] = True
			while len(q) > 0:				
				cur = q.popleft()
				output.append(cur)				
				for nbr in self._adjlist[cur]:
					if not marked[nbr]:
						q.append(nbr)
						marked[nbr] = True
			
		output = []
		marked = {x:False for x in self._adjlist}
		notmarked = (node for node in self._adjlist if not marked[node])
		for root in notmarked:
			search(root, output, marked)
		return output
		
	def topological_sort(self):
		assert(self._is_directed), 'topological sort is for directed graphs'
		inbound_count = {x:0 for x in self._adjlist}
		for node, nbrs in self._adjlist.items():
			for nbr in nbrs:
				inbound_count[nbr] += 1
				
		from collections import deque
		q = deque()		
		while True:
			root = min(inbound_count, key=inbound_count.get)
			if inbound_count[root] != 0:
				break
			q.append(root)
			del(inbound_count[root])
		if len(q) == 0:
			return False
		output = []		
		while len(q) >0 :
			current = q.popleft()
			output.append(current)
			for nbr in self._adjlist[current]:
				inbound_count[nbr] -= 1
				if inbound_count[nbr] == 0:
					q.append(nbr)
		return output if len(output) == len(self._adjlist) else False
		
	def __repr__(self):
		rep = f'G({self.ncount()}, {self.ecount()}, '\
			 f'directed={self._is_directed}, weighted={self._is_weighted}):\n'
		for n, l in self._adjlist.items():
			rep += str(n) + ' --> {' + ', '.join(str(nbr) for nbr in l) + '}\n'
		return rep[:-1]


if __name__ == '__main__':
	g = Graph()
	for n in 'abcdefghij':
		g.add_node(n)
	for e in (('a', 'b'), ('a', 'c'), ('d', 'g'), ('c', 'd'), ('b', 'd'), ('b', 'e'), ('e', 'g'), 
				('e', 'f'), ('g', 'f'), ('h', 'i'), ('h', 'j'), ('j', 'i')):
		g.add_edge(*e)
	print(g)
	print('DFS', g.dfs())
	print('BFS', g.bfs())
	print('Topological sort', g.topological_sort())