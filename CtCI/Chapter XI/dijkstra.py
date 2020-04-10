import unittest

class Graph:
	def __init__(self, name):
		self.name = name
		self.nodes = {}
		self.ew = {}
	
	def __repr__(self):
		rep = [repr(nd) for nd in self.nodes.values()]		
		return f'[{self.name}]\n' + '\n'.join(rep)

	def add_node(self, n):
		self.nodes[n] = self.Node(n)

	def add_edge(self, n1, n2, weight):
		assert (n1 in self.nodes), 'not existing node'
		assert (n2 in self.nodes), 'not existing node'
		self.nodes[n1].add_nbr(self.nodes[n2])
		self.ew[(n1, n2)] = weight
	
	def dijkstra(self, s, t):
		assert (s in self.nodes), 'not existing node'
		assert (t in self.nodes), 'not existing node'

		path_weights = {n:float('inf') for n in self.nodes}
		prev_node = {n:-1 for n in self.nodes}
		pw, pn = path_weights, prev_node
		pw[s] = 0
		
		visit_queue = {s:0}
		while len(visit_queue) > 0:
			cur = min(visit_queue, key=visit_queue.get)
			for nbr in self.nodes[cur].children:
				nbr = nbr.data
				if pw[nbr] > pw[cur] + self.ew[(cur, nbr)]:
					pw[nbr] = pw[cur] + self.ew[(cur, nbr)]
					pn[nbr] = cur
					visit_queue[nbr] = pw[nbr]
			del(visit_queue[cur])
		
		path = []
		n = t
		while n in pn:
			path.append(n)
			n = pn[n]
		
		return path[::-1] #reversing to build path from start to target
		
	
	class Node:
		def __init__(self, data):
			self.data = data
			self.children = set()

		def __repr__(self):
			return str(self.data) + str([nd.data for nd in self.children])

		def add_nbr(self, node):			
			assert (type(node) is type(self)), 'invalid neighbour'
			self.children.add(node)			



class Test(unittest.TestCase):
	def test_dijkstra(self):
		g = Graph('MyGraph')
		for i in 'abcdefghi':
			g.add_node(i)
		g.add_edge('a', 'b', 5)
		g.add_edge('a', 'c', 3)
		g.add_edge('a', 'e', 2)
		g.add_edge('b', 'd', 2)
		g.add_edge('c', 'b', 1)
		g.add_edge('c', 'd', 1)
		g.add_edge('d', 'a', 1)
		g.add_edge('d', 'g', 2)
		g.add_edge('d', 'h', 1)
		g.add_edge('e', 'a', 1)
		g.add_edge('e', 'h', 4)
		g.add_edge('e', 'i', 7)
		g.add_edge('f', 'b', 3)
		g.add_edge('f', 'g', 1)
		g.add_edge('g', 'c', 3)
		g.add_edge('g', 'i', 2)
		g.add_edge('h', 'c', 2)
		g.add_edge('h', 'f', 2)
		g.add_edge('h', 'g', 2)
		self.assertEqual(list('acdgi'), g.dijkstra('a', 'i'))


if __name__ == "__main__":
	unittest.main()