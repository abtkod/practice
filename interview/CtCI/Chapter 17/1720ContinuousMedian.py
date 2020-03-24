import unittest


class Heap:
	def __init__(self, type='min'):
		pass


def continuous_median(random_generator):
	if len(random_generator) == 1 or len(random_generator) == 2:
		numbers = [num for num in random_generator]
		return numbers, numbers[0]

	minh = Heap('min')
	maxh = Heap('max')
	numbers = []
	for i, num in enumerate(random_generator):
		numbers.append(num)
		if i == 0:
			minh.insert(num)
			continue
		if i == 1:
			maxh.insert(num)
			continue

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
	median = maxh.top if len(maxh) >= len(minh) else minh.top
	return numbers, median


class Test(unittest.TestCase):
	def test_continuous_median(self):
		import random
		gen = (random.randint(1, 99) for _ in range(7))
		numbers, median = continuous_median(gen)
		mm = sorted(numbers)[len(numbers) // 2]
		self.assertEqual(median, mm)


if __name__ == '__main__':
	unittest.main()