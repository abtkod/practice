class ThreeStack(object):
	def __init__(self, memory_size):
		self.memory = [None] * memory_size
		self.slb = self.slt = 0
		self.srb = self.srt = len(self.memory) - 1
		self.smb = self.smt = int(len(self.memory) / 1.5)
		self.available_space = memory_size

	def _shift_middle(self, c):
		if c > 0:
			for i in range(self.smt - self.smb + 1):
				self.memory[self.smt - i + 1] = self.memory[self.smt - i]
			self.smb += 1
			self.smt += 1
		elif c < 0:
			for i in range(self.smt - self.smb + 1):
				self.memory[self.smb + i - 1] = self.memory[self.smb + i]
			self.smb -= 1
			self.smt -= 1

	def push(self, stack_number, value):
		if self.is_full():
			raise Exception('Stack is full')

		if stack_number == 1:
			# left stack is filled left to right
			if self.slt == self.smb:
				self._shift_middle(1)						
			self.memory[self.slt] = value
			self.slt += 1

		if stack_number == 2:
			# right stack is filled right to left
			if self.srt < self.smt:
				self._shift_middle(-1)
			self.memory[self.srt] = value
			self.srt -= 1

		if stack_number == 3:
			# middle stack is filled left to right
			if self.smt > self.srt:
				self._shift_middle(-1)
			self.memory[self.smt] = value
			self.smt += 1
		
		self.available_space -= 1
		return self

	def pop(self, stack_number):
		value = None
		if stack_number == 1:
			if self.slt == self.slb:
				raise Exception("Stack is empty")
			self.slt -= 1
			value = self.memory[self.slt]			
			self.memory[self.slt] = None
			
		if stack_number == 2:
			if self.srt == self.srb:
				raise Exception("Stack is empty")
			self.srt += 1
			value = self.memory[self.srt]
			self.memory[self.srt] = None

		if stack_number == 3:
			if self.smt == self.smb:
				raise Exception("Stack is empty")
			self.smt -= 1
			value = self.memory[self.smt]
			self.memory[self.smt] = None
		return value

	def is_full(self):
		return self.available_space < 1

	def __str__(self):
		return str(self.memory)

if __name__ == "__main__":
	stack = ThreeStack(10)
	stack.push(1, 1).push(1,2)\
		.push(2,10).push(2,11)\
		.push(3, 'a').push(3, 'b')\
		.push(2, 12).push(2, 13)\
		.push(3, 'c').push(3, 'd')
	print(stack)
	print(stack.pop(1))
	print(stack.pop(2))
	print(stack.pop(3))
	print(stack)