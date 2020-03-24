import unittest
import heapq


class Heap:
	def __init__(self, type='min'):
		assert (type == 'min' or type == 'max'), 'invalid type of heap'
		self._op = 1 if type == 'min' else -1
		self.head = []
	
	def __str__(self):
		return str([self._op * v for v in self.head])

	def __len__(self):
		return len(self.head)

	@property
	def top(self):
		if len(self.head) != 0:
			return self._op * self.head[0]
		else:
			return None

	def insert(self, val):
		assert(len(self.head) == 0 or type(val) == type(self.head[0])), 'invalid type of object'
		heapq.heappush(self.head, self._op * val)

	def extract_top(self):
		return self._op * heapq.heappop(self.head)	


def continuous_median(numbers):	
	assert (len(numbers) > 0), 'empty list'
	if len(numbers) < 3:
		return numbers, numbers[0]

	minh = Heap('min')
	maxh = Heap('max')
	minh.insert(max(numbers[:2]))
	maxh.insert(min(numbers[:2]))
	for num in numbers[2:]:
		if num >= minh.top:
			minh.insert(num)
		else:
			maxh.insert(num)
		if len(minh) - len(maxh) > 1:
			top = minh.extract_top()
			maxh.insert(top)
		elif len(minh) - len(maxh) < -1 :
			top = maxh.extract_top()
			minh.insert(top)
	if len(maxh) == len(minh):
		median = (minh.top + maxh.top)/2
	elif len(maxh) > len(minh):
		median = maxh.top
	else:
		median = minh.top
	return median


import random
class Test(unittest.TestCase):	

	def test_heap(self):
		l = [random.randint(-10, 10) for _ in range(20)]
		minh, maxh = Heap('min'), Heap('max')
		for v in l:
			minh.insert(v)
			maxh.insert(v)		
		self.assertEqual(min(l), minh.top)
		self.assertEqual(max(l), maxh.top)
			

	def test_continuous_median(self):		
		numbers = [random.randint(1, 99) for _ in range(7)]
		median = continuous_median(numbers)
		numbers.sort()
		mm = numbers[len(numbers) // 2] if len(numbers)%2 == 1 else (numbers[len(numbers)//2 - 1] + numbers[len(numbers)//2])/2
		self.assertEqual(median, mm)


if __name__ == '__main__':
	unittest.main()