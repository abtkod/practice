class MinimumStack:

	def __init__(self, memory_size):
		self.memory = [None] * memory_size
		self.top = 0

	def push(self, value):
		if self.top == len(self.memory):
			raise Exception('Memory is full')
		
		if self.top == 0:
			self.memory[0] = (value, value)
			self.top += 1
			return self
		new_entry = (value, min(value, self.memory[self.top-1][1]))
		self.memory[self.top] = new_entry
		self.top += 1
		return self

	def pop(self):
		if self.top == 0:
			raise Exception('Stack is empty')
		value = self.memory[self.top-1][0]
		self.memory[self.top] = None
		self.top -= 1
		return value

	def min(self):
		return self.memory[self.top-1][1]

	def __str__(self):
		return str(self.memory)


if __name__ == "__main__":
	from random import randint
	stack = MinimumStack(12)
	for i in range(10):
		stack.push(randint(1, 15))
	print(stack)
	values = []
	for i in range(5):
		minv = stack.min()
		val = stack.pop()
		print(f'value:{val}, min:{minv}')
	print(stack)