import unittest


class Heap:
	class HeapNode:
		def __init__(self, value):
			self.value = value
			self.parent = self.lchild = self.rchild = self.lsib = self.rsib = None

		def __str__(self):
			ltree = rtree = ''
			if self.lchild is not None:
				ltree = str(self.lchild)
			if self.rchild is not None:
				rtree = str(self.rchild)
			return f'({str(self.value)} {ltree} {rtree})'

	def __init__(self, heap_type='min'):
		assert(heap_type == 'min' or heap_type == 'max'), 'invalid type for heap'
		self._op = min if heap_type == 'min' else max
		self._top = self._last = None
		self._size = 0

	@property
	def top(self):
		return None if self._top is None else self._top.value

	def __len__(self):
		return self._size

	def __str__(self):
		return str(self._top)
	
	def insert(self, value):
		self._size += 1
		newnode = self.HeapNode(value)
		if self._top == None:
			self._top = self._last = newnode
			return

		if self._top == self._last:
			self._last.lchild = newnode
			newnode.parent = self._last
		else:
			parent = self._last.parent
			if parent.lchild == self._last:
				parent.rchild = newnode
				newnode.parent = parent
			elif parent.rchild == self._last:
				cur = parent.rsib
				cur.lchild = newnode
				newnode.parent = cur
		newnode.lsib = self._last
		self._last.rsib = newnode
		self._last = newnode
		self._bubble(self._last, 'up')

	def flush(self):
		values = []
		while True:
			v = self.extract_top()
			if not v:
				break
			values.append(v)
		return values

	def extract_top(self):
		if self.top is None:
			return
		self._size -= 1		
		top = self.top
		if self._top == self._last:
			self._top = self._last = None
			return top
		valuetotop = self._last.value
		parent = self._last.parent
		newlast = self._last.lsib
		if parent.rchild == self._last:
			parent.rchild = None
		else:
			parent.lchild = None
		self._last.parent = self._last.lsib = None
		newlast.rsib = None
		self._last = newlast
		self._top.value = valuetotop
		self._bubble(self._top, 'down')
		return top

	def _bubble(self, node, direction):
		assert(direction == 'up' or direction == 'down'), 'bubble \'up\' or bubble \'down\' only'
		def swap_value(n1, n2):
			tmp = n1.value
			n1.value = n2.value
			n2.value = tmp

		if direction == 'up':
			while node.parent is not None:
				if self._op(node.value, node.parent.value) == node.parent.value:
					break
				swap_value(node, node.parent)
				node = node.parent
		else:
			values = [(nd.value, nd) for nd in [node, node.lchild, node.rchild] if nd is not None]			
			while len(values) > 1:
				tp, tpn = self._op(values, key=lambda x: x[0])
				if tp == node.value:
					break
				swap_value(node, tpn)
				node = tpn
				values = [(nd.value, nd) for nd in [node, node.lchild, node.rchild] if nd is not None]
		

from random import randint
class Test(unittest.TestCase):
	def test_Heap(self):
		numbers = [randint(1, 100) for _ in range(39)]
		minh, maxh = Heap('min'), Heap('max')
		for num in numbers:
			minh.insert(num)
			maxh.insert(num)
		self.assertEqual(minh.flush(), sorted(numbers))
		self.assertEqual(maxh.flush(), sorted(numbers, reverse=True))


if __name__ == '__main__':
	unittest.main()