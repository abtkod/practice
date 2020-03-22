import unittest

class Heap:
	class Node:
		def __init__(self, data=None):
			self.data = data
			self.lnode = self.rnode = self.parent = None

		def __str__(self):
			left = right = ''
			if self.lnode is not None:
				left = str(self.lnode)
			if self.rnode is not None:
				right = str(self.rnode)
			return f'({str(self.data)} {left} {right})'

	def __init__(self, values=[], type='min'):
		assert(type == 'min' or type == 'max'), 'invalid type of heap'
		self.comparator = min if type == 'min' else max
		self.root = self.last = None
		for v in values:
			self.insert(v)

	def __str__(self):
		return str(self.root)
	
	@property
	def top(self):
		return self.root.data
	
	def heapify(self, node, direction):
		assert (direction == 'up' or direction == 'down'), 'invalid direction'
		def swap(n1, n2):
			temp = n1.data
			n1.data = n2.data
			n2.data = temp

		if direction == 'up':
			while node.parent is not None and self.comparator((node.parent.data, node.data)) == node.data:
				swap(node, node.parent)				
				node = node.parent
		else:
			while node.lnode is not None or node.rnode is not None:
				cmp = {nd.data: nd for nd in [node, node.lnode, node.rnode] if nd is not None}
				sw = self.comparator(cmp.keys())
				if cmp[sw] is node:
					return			
				swap(node, cmp[sw])
				node = cmp[sw]

	def insert(self, v):
		assert not(v > v) and not(v < v), 'value is not comparable'
		newnode = self.Node(v)
		if self.root is None:
			self.root = self.last = newnode
			return
		if self.last.parent is None:
			self.last.lnode = newnode
			newnode.parent = self.last
		else:
			nextnode = self.seek(self.last, direction='next')
			if nextnode.lnode is None:
				nextnode.lnode = newnode
			else:			
				nextnode.rnode = newnode
			newnode.parent = nextnode
		self.last = newnode
		self.heapify(self.last, 'up')

	def seek(self, node, direction='previous'):
		assert (direction == 'previous' or direction == 'next'), 'invalid direction'
		if direction == 'next' and node.parent.lnode is node:
			return node.parent
		elif direction == 'previous' and node.parent.rnode is node:
			return node.parent.lnode
		elif direction == 'next' and node.parent.rnode is node:
			while node.parent is not None and node.parent.rnode is node:
				node = node.parent
			if node.parent is not None:
				node = node.parent.rnode
			while node.lnode is not None:
				node = node.lnode
			return node
		elif direction == 'previous' and node.parent.lnode is node:			
			while node.parent is not None and node.parent.lnode is node:
				node = node.parent
			if node.parent is not None:
				node = node.parent.lnode
			while node.rnode is not None:
				node = node.rnode
			return node

	def extract_top(self):
		if self.root == None:
			return False
		top = self.root.data
		if self.last is self.root:
			self.last = self.root = None
			return top
		
		self.root.data = self.last.data
		previous = self.seek(self.last, 'previous')
		if self.last.parent is previous.parent:
			self.last.parent.rnode = None
		else:
			self.last.parent.lnode = None
		self.last.parent = None
		self.last = previous		
		self.heapify(self.root, 'down')
		return top

	def items(self):
		items = []
		v = self.extract_top()
		while v:
			items.append(v)
			v = self.extract_top()
		return items

def smallest_k(A, k): #nlog(k)
	mxh = Heap(A[:k], type='max') # O(k)
	for i in range(k, len(A)):
		if A[i] < mxh.top:
			mxh.extract_top()
			mxh.insert(A[i])
	return mxh.items()


class Test(unittest.TestCase):
	data = [16,7,3,9,10,5,2,1,17]
	
	def test_heap(self):
		minheap = Heap(self.data, 'min')
		print(minheap)
		self.assertEqual(minheap.items(), sorted(self.data))

	def test_smallest_k(self):
		self.assertEqual(smallest_k(self.data, 4), [5,3,2,1])

if __name__ == '__main__':
	unittest.main()