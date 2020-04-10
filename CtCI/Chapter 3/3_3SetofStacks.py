import unittest
class SetofStacks:

	def __init__(self, memory_size):
		self.memory_size = memory_size
		self.subs = []
		self.top = [-1, 0]

	def push(self, value):
		if self.top[0] == -1 or self.top[1] == self.memory_size:
			#sub is full
			self.subs.append([None] * self.memory_size)
			self.top[0] += 1
			self.top[1] = 0

		curm = self.subs[self.top[0]]
		curm[self.top[1]] = value
		self.top[1] += 1
		return self

	def pop(self):
		if self.top[0] == -1:
			raise Exception('Empty stack')
		if self.top[1] > 0:
			val = self.subs[self.top[0]][self.top[1]-1]
			self.top[1] -= 1
			self.subs[self.top[0]][self.top[1]] = None
			return val
		else:
			self.top[0] -= 1
			self.top[1] = len(self.subs[self.top[0]]) - 1			
			val = self.subs[self.top[0]][self.top[1]]
			self.subs[self.top[0]][self.top[1]] = None
			return val

	def pop_at(self, index):
		if len(self.subs) < index + 1:
			raise Exception('Substack does not exist')
		val = self.subs[index].pop()
		return val

	def __str__(self):
		l = []
		for sub in self.subs:
			l += sub
		return str(l)


class Test(unittest.TestCase):
	
	def test_push(self):
		stack = SetofStacks(5)
		for i in range(15):
			stack.push(i)
		self.assertEqual(str(stack), str(list(range(15))))

	def test_pop(self):
		stack = SetofStacks(5)
		for i in range(15):
			stack.push(i)
		pops = []
		for _ in range(6):
			pops.append(stack.pop())					
		self.assertEqual(str(pops), str(list(reversed(range(9,15)))))

if __name__ == "__main__":
	unittest.main()