class Node:
	def __init__(self, data):
		self.data = data
		self.ngbrV = set()
		
	def add_nbr(self, node):
		self.ngbrV.add(node)
		
	def __repr__(self):
		return str(self.data)


class Graph:
	def __init__(self, name):
		self.name = name
		self.nodes = set()

	def __repr__(self):
		return str([f'{nd.data}: {nd.ngbrV}' for nd in self.nodes])
	
	def add_node(self, node:Node):
		assert (type(node) is Node), 'invalid node'
		self.nodes.add(node)
	
	def add_edge(self, n1:Node, n2:Node, is_directed=True):
		assert (type(n1) is Node and type(n2) is Node), 'invalid edge'
		assert (n1 in self.nodes), 'n1 does not exist'
		assert (n2 in self.nodes), 'n2 does not exist'
		n1.add_nbr(n2)
		if not is_directed:
			n2.add_nbr(n1)

	def topological_sort(self):
		from collections import deque
		inbound_counts = {}
		for nd in self.nodes:
			inbound_counts.setdefault(nd, 0)
			for nbr in nd.ngbrV:
				inbound_counts.setdefault(nbr, 0)
				inbound_counts[nbr] += 1				
		process_next = deque([nd for nd in inbound_counts if inbound_counts[nd] == 0])
		order = []
		while len(process_next) > 0 and len(order) < len(self.nodes):
			cur = process_next.popleft()			
			for nd in cur.ngbrV:
				inbound_counts[nd] -= 1
				if inbound_counts[nd] == 0:
					process_next.append(nd)
			order.append(cur)
		
		return order if len(process_next) == 0 else False				
	
	
	
import unittest
class Test(unittest.TestCase):		
	def test_topological_sort(self):
		graph = Graph('TestGraph')
		nodes = [Node(i) for i in range(6)]
		for nd in nodes:
			graph.add_node(nd)
		graph.add_edge(nodes[0], nodes[1])
		graph.add_edge(nodes[2], nodes[1])
		graph.add_edge(nodes[1], nodes[3])
		graph.add_edge(nodes[4], nodes[3])		
		graph.add_edge(nodes[1], nodes[5])
		graph.add_edge(nodes[3], nodes[5])
		graph.add_edge(nodes[4], nodes[5])		
		self.assertEqual(str(graph.topological_sort()[3:]), '[1, 3, 5]')


if __name__ == '__main__':
	unittest.main()