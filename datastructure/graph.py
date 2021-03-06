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
			
	def nodes(self):
		return sorted(self._adjlist.keys())
			
	def edges(self):
		edges = set()
		for n1, nbrs in self._adjlist.items():
			for n2 in nbrs:
				if self._is_weighted:
					if self._is_directed:
						edges.add((n1, n2[0], n2[1]))
					else:
						edges.add((min(n1, n2[0]), max(n1, n2[0]), n2[1]))
				else:
					if self._is_directed:
						edges.add((n1, n2))
					else:
						edges.add(min(n1, n2), max(n1, n2))
					
		return sorted(edges)
	
	def ncount(self):
		return len(self._adjlist)

	def ecount(self):
		c = sum(len(x) for x in self._adjlist.values())
		return int(c) if self.is_directed else int(c/2)

	def add_node(self, n):
		assert(n not in self._adjlist), 'node already exists.'
		self._adjlist[n] = set()

	def add_edge(self, n1, n2, weight=None):
		assert(n1 in self._adjlist), 'node does not exist.'
		assert(n2 in self._adjlist), 'node does not exist.'
		self._adjlist[n1].add(n2) if not self._is_weighted else self._adjlist[n1].add((n2, weight))
		if not self._is_directed:
			self._adjlist[n2].add(n1) if not self._is_weighted else self._adjlist[n2].add((n1, weight))
			
	def adjacency_matrix(self):
		class AdjacencyMatrix:
			def __init__(self, nodes):
				self.__matrix = [['-']*len(nodes) for _ in range(len(nodes))]
				self.__reverse_mapping = {node:index for index, node in enumerate(nodes)}
				self.__nodes = list(nodes)
			def __getitem__(self, tup):
				n1, n2 = tup
				return self.__matrix[self.__reverse_mapping[n1]][self.__reverse_mapping[n2]]
			def __setitem__(self, tup, val):
				n1, n2 = tup
				self.__matrix[self.__reverse_mapping[n1]][self.__reverse_mapping[n2]] = val
			def __repr__(self):
				rep = '  ' + ' '.join(self.__nodes)
				for i, row in enumerate(self.__matrix):
					rep += '\n' + str(self.__nodes[i]) + ' ' + ' '.join(str(c) for c in row)
				return rep
		
		ajm = AdjacencyMatrix(self._adjlist.keys())
		for nd, nbrs in self._adjlist.items():
			for nbr in nbrs:
				if self._is_weighted:
					ajm[nd, nbr[0]] = nbr[1]
				else:
					ajm[nd, nbr] = 1
		return ajm
		
	def dfs(self):		
		def search(root, output, visited):
			output.append(root)
			visited[root] = True
			for nbr in self._adjlist[root]:
				if self._is_weighted:
						nbr = nbr[0]
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
					if self._is_weighted:
						nbr = nbr[0]
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
				if self._is_weighted:
						nbr = nbr[0]
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
				if self._is_weighted:
						nbr = nbr[0]
				inbound_count[nbr] -= 1
				if inbound_count[nbr] == 0:
					q.append(nbr)
		return output if len(output) == len(self._adjlist) else False
		
	def dijkstra(self, s, t=None):
		''' 
		It's said that dijkstra does not work with negative weights. It could be because dijkstra cannot find negative cycles 
		and gets stuck in the loop. If this is the reason, we might use topological sort to check if cycles exist and their weights.
		The main diference is that here visit can accept the same node if after relaxing, its path_weight is decreased.
		Also dijstra is used for single pair shortest path. By enabling None target node, I used like single source shortest path.
		'''
		assert (self._is_weighted), 'unweighted graph'
		assert (s in self._adjlist), 's does not exist'
		assert (t in self._adjlist or t is None), 't does not exist'
		path_weights = {x:float('inf') for x in self._adjlist}		
		prev_node = {x: None for x in self._adjlist}
		visit = {}		
		path_weights[s] = 0
		visit[s] = 0
		while len(visit) > 0:			
			curn = min(visit, key=visit.get)			
			curw = visit[curn]			
			gen = ((n, w) for n, w in self._adjlist[curn] if path_weights[n] > curw +  w)
			for n, w in gen:
				# relaxing
				path_weights[n] = curw +  w
				visit[n] = curw +  w
				prev_node[n] = curn
			del(visit[curn])
		if t is None:
			# shortest paths to all nodes from s
			return prev_node, path_weights
		if prev_node[t] is None:
			return False
		path = []
		n = t
		while n is not None:
			path = [n] + path
			n = prev_node[n]		
		return path_weights[t], path

	def bellman_ford(self, s):
		'''
		- single source shortest path with positive and negative edges when there is no negative cycle reachable from source
		- complexity O(EV)
		'''
		assert (s in self._adjlist), 'source does not exist'
		path_weights = {x:float('inf') for x in self._adjlist}
		pred_node = {x:None for x in self._adjlist}
		path_weights[s] = 0
		edges = self.edges()
		for _ in range(self.ncount()-1): # note: relaxing over edges is done N-1 times
			for n1, n2, w in edges:
				# relaxation phase
				if path_weights[n2] > path_weights[n1] + w:
					path_weights[n2] = path_weights[n1] + w
					pred_node[n2] = n1
		for n1, n2, w in edges: # negative cycle is checked at the end
			if path_weights[n2] > path_weights[n1] + w:
				# negative cycle
				return False, False
		return pred_node, path_weights

	def floyed_warshall(self):
		W = self.adjacency_matrix()
		N = self.nodes()
		#initialization
		for n1 in N:
			for n2 in N:
				if n1 == n2:
					W[n1,n2] = 0
				if W[n1, n2] == '-':
					 W[n1, n2] = float('inf')
		import copy		
		for k in N:
			D = copy.deepcopy(W)
			for i in N:
				for j in N:
					D[i, j] = min(W[i, j], W[i, k]+W[k, j])
			W = D
		#converting 'inf' to '-' to better representation
		gen = ((n1, n2) for n1 in N for n2 in N if W[n1, n2] == float('inf'))
		for n1, n2 in gen:			
			W[n1, n2] = '-'
		return W
			
		
	def mst_prime(self):		
		assert(self._is_weighted and not self._is_directed), 'MST is used for undirected weighted graph'
		mst = set()		
		to_cover = set(self.nodes())
		nd = next(iter(self._adjlist))
		pq = {nb:(w,nd) for nb, w in self._adjlist[nd]}
		to_cover.remove(nd)
		while len(pq) > 0 and len(to_cover) > 0:
			cnd = min(pq, key=pq.get)
			for nb, w in self._adjlist[cnd]:								
				if nb in to_cover and (nb not in pq or pq[nb][0] > w):
					pq[nb] = (w, cnd)
			mst.add((pq[cnd][1], cnd, pq[cnd][0]))
			del(pq[cnd])
			to_cover.remove(cnd)
		return sorted(mst, key=lambda x: x[2]) if len(to_cover) == 0 else False
			
		
	def mst_kruskal(self):
		assert(self._is_weighted and not self._is_directed), 'MST is used for undirected weighted graph'
		edges = self.edges()
		edges.sort(key=lambda x: x[2])
		node_to_component = {x:set(x) for x in self._adjlist}
		mst = set()
		for e in edges:
			n1, n2, _ = e			
			if n2 not in node_to_component[n1]:
				u = node_to_component[n1].union(node_to_component[n2])
				for n in u:
					node_to_component[n] = u
				mst.add(e)
			if len(mst) == self.ncount() - 1:
				return sorted(mst, key=lambda x: x[2])
		return False            
	
	def undirected(self):
		if not self._is_directed:
			import copy
			return copy.deepcopy(self)
		
		from random import choice
		edges = {}
		for n, nbrs in self._adjlist.items():
			for nb in nbrs:
				if self._is_weighted:
					edges.setdefault((n, nb[0]), nb[1])					
					w = choice([edges[(n, nb[0])], nb[1]])
					edges[(n, nb[0])] = w
					edges.setdefault((nb[0], n), nb[1])
					edges[(nb[0], n)] = w
				else:
					edges[(n, nb[0])] = None
					edges[(nb[0], n)] = None
		udg = Graph(is_directed=False, is_weighted=self._is_weighted)		
		for e, w in edges.items():
			udg._adjlist.setdefault(e[0], set())
			udg._adjlist[e[0]].add((e[1], w) if w is not None else e[1])
		return udg
		
	def __repr__(self):
		rep = f'G({self.ncount()}, {self.ecount()}, '\
			 f'directed={self._is_directed}, weighted={self._is_weighted}):\n'
		for n, l in self._adjlist.items():
			rep += str(n) + ' --> {' + ', '.join(str(nbr) for nbr in l) + '}\n'
		return rep[:-1]


if __name__ == '__main__':
	g = Graph(is_weighted=True)
	for n in 'abcdefghij':
		g.add_node(n)
	for e in (('a', 'b', 2), ('a', 'c', 8), ('d', 'g', 1), ('c', 'd', 6), ('b', 'd', 4), ('b', 'e', 0), ('e', 'g', 5), ('e', 'j', 3),
				('e', 'f', 1), ('g', 'f', 4), ('h', 'i', 2), ('h', 'j', 2), ('j', 'i', 7), ('i', 'h', 10), ('i', 'g', 2)):
		g.add_edge(*e)
	print(g)
	print(g.adjacency_matrix())	
	print('DFS', g.dfs())
	print('BFS', g.bfs())
	print('Topological sort', g.topological_sort())
	print('Dijkstra(a, g) ', g.dijkstra('a', 'g'))
	print('Dijkstra(a)    ', g.dijkstra('a')[1])
	print('Bellman_ford(a)', g.bellman_ford('a')[1])
	print('Floyed_Warshal()\n', g.floyed_warshall())
	gund = g.undirected()
	print(gund)	
	print(gund.adjacency_matrix())
	print('MST Kruskal', gund.mst_kruskal())
	print('MST Prime  ', gund.mst_prime())