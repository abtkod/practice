import unittest

def missing_two(arr):
	n = len(arr) + 2
	sum_linear = lambda n: n * (n+1) /2 
	sum_squared = lambda n: (n * (n+1) * (2*n+1)) / 6
	x = sum_linear(n) - sum(arr)
	y = sum_squared(n) - sum((x**2 for x in arr))
	a = (2*x - (4*(x**2)-8*(x**2-y))**0.5) / 4
	b = x - a
	return a, b


class Test(unittest.TestCase):
	arr = [i for i in range(1, 20) if i != 12 and i != 15]

	def test_missing_two(self):		
		self.assertEqual(missing_two(self.arr), (12, 15))


if __name__ == '__main__':
	unittest.main()
	
	