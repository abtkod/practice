import unittest

def triple_step(n, m={}):
	if n == 1:
		return 1
	if n == 2: 
		return 2
	if n == 3:
		return 4
	for i in range(1, 4):
		if m.get(n-i, 0) == 0:
			m[n-i] = triple_step(n-i, m)	
	return m[n-1] + m[n-2] + m[n-3]

class Test(unittest.TestCase):
	data = [(1, 1), (2, 2), (3, 4), (4, 7), (5, 13), (6, 24)]
	def test_triple_step(self):
		for n, actual in self.data:
			self.assertEqual(triple_step(n), actual)

if __name__ == '__main__':
	unittest.main()
