import unittest

def add_without_plus(num1, num2):
	assert type(num1) is int and type(num2) is int, 'Non int numbers'
	assert num1 * num2 >= 0, "subtraction"

	carry = num2
	added = num1
	while carry:
		prev = added
		added = added ^ carry
		carry = prev & carry
		carry = carry << 1

	return added

class Test(unittest.TestCase):
	data = [(10, 15, 25), (1, 2, 3), (10000, 1, 10001), (4, 512, 516), (-48127, -924, -49051)]

	def test_add_without_plus(self):
		for num1, num2, actual in self.data:
			self.assertEqual(add_without_plus(num1, num2), actual)


if __name__ == '__main__':
	unittest.main()