class LRU(object):
	
	def __init__(self, max_size):
		self.max_size = max_size
		self.array = []
		self.key2value = {}		

	def add(self, key, value):
		if len(self.array) == self.max_size:
			self.evict()
		self.key2value[key] = value
		self.array.append(key)		

	def evict(self):				
		key = self.array[0]
		self.array.remove(key)			
		val = self.key2value[key]
		del(self.key2value[key])
		return key, val

	def __getitem__(self, key):
		if key in self.array[-1::-1]:
			self.array.remove(key)
		self.array.append(key)
		return self.key2value.get(key, -1)

	def __str__(self):
		return f'array:\n{str(self.array)}\nvalues:\n{self.key2value}\n'


class LRUFast:
	class Node:
		def __init__(self, val, prevNode=None, nextNode=None):
			self.value = val			
			self.prev = prevNode
			self.next = nextNode

		def __str__(self):
			return str(self.value)

	def __init__(self, max_size):
		self.max_size = max_size
		self.size = 0
		self.map = {}
		self.head = None
		self.tail = None

	def add(self, key, value):
		if self.size == self.max_size:
			self.evict()
		self.size += 1
		n = self.Node(key, self.tail)		
		if self.head is None:
			self.head = self.tail = n
			n.prev = n
		else:
			self.tail.next = n
			self.tail = n
		if self.map.get(key, -1) != -1:
			self.update(key, value)
		else:
			self.map[key] = [value, n]		

	def evict(self):
		self.size -= 1
		key = self.head.value
		value, n = self.map[key]
		self.head = n.next
		n.next.prev = self.head
		n.prev = n.next = None
		del(self.map[key])
		return value

	def __getitem__(self, key):
		value = self.map[key][0]
		self.update(key)
		return value

	def update(self, key, value=None):
		_, node = self.map[key]
		prevNode = node.prev
		nextNode = node.next
		prevNode.next = nextNode
		nextNode.prev = prevNode
		node.next = None
		node.prev = self.tail
		self.tail.next = node
		self.tail = node
		if value is not None:
			self.map[key][0] = value

	def __str__(self):
		array = "["
		current = self.head
		while current is not None:
			array += str(current) + ", "
			current = current.next
		array = array[:-2] + "]"
		mapping = [(k, v[0]) for k, v in self.map.items()]
		return f'array:\n{array}\nvalues:\n{mapping}\n'

lru = LRU(7)
for i in range(12):
	lru.add(i, str(i))
print(lru[9])
print(lru)
print('*' * 10)
lrufast = LRUFast(7)
for i in range(12):
	lrufast.add(i, str(i))
print(lrufast[9])
print(lru)