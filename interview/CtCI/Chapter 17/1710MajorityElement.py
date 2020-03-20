import unittest

def majority_element(A):
	majority = None
	countmajority = subarraysize = 0
	for e in A:
		if majority is None:
			majority = e
			countmajority = subarraysize = 0
		subarraysize += 1
		if e == majority:
			countmajority += 1
		if countmajority <= subarraysize//2:
			majority = None
			countmajority = 0
	if majority:
		countmajority = 0
		for e in A:
			if e == majority:
				countmajority += 1
	return majority if countmajority > len(A) // 2 else -1


class Test(unittest.TestCase):
	data = [1, 2, 5, 9, 5, 9, 5, 5, 5]
	ans = 5
	def test_majority_element(self):
		self.assertEqual(self.ans, majority_element(self.data))


if __name__ == '__main__':
	unittest.main()	