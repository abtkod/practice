import unittest
from collections import deque

def kth_multiple(k):
	three, five, seven = deque([1,3]), deque([5]), deque([7])
	output = []
	d = set()
	i = 0
	while i < k:
		if three[0] <= five[0] and three[0] <= seven[0]:
			val = three.popleft()
		elif five[0] <= three[0] and five[0] <= seven[0]:
			val = five.popleft()
		else:
			val = seven.popleft()
		if val not in d:
			three.append(3 * val)
			five.append(5 * val)
			seven.append(7 * val)
			output.append(val)
			d.add(val)
			i += 1
	return output


class Test(unittest.TestCase):
	k = 10
	res = [1,3,5,7,9,15,21,25,27,35]
	def test_kth_multiple(self):
		self.assertEqual(self.res, kth_multiple(self.k))

if __name__ == "__main__":
	unittest.main()