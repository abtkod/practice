import unittest

def recursive_multiply(smaller, bigger):
	if smaller == 0:
		return 0
	if smaller == 1:
		return bigger
	
	rightmost = 0 if smaller == (smaller >> 1 << 1) else bigger
	rest = recursive_multiply(smaller >> 1, bigger)
	return rest + rest + rightmost

def recursive_multiply_faster(num1, num2):
	(sm, bg) = (num1, num2) if num1 < num2 else (num2, num1)
	return recursive_multiply(sm, bg)


class Test(unittest.TestCase):
	data = [(3, 5, 15), (101, 1001, 101101), (2500, 10, 25000)]
	
	def test_multiply(self):
		for (num1, num2, actual) in self.data:
			print(f"{num1:b}, {num2:b}, {actual:b}")
			self.assertEqual(actual, recursive_multiply(num1, num2))
			self.assertEqual(actual, recursive_multiply_faster(num1, num2))

if __name__ == "__main__":
	unittest.main()