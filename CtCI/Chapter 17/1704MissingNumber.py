import unittest

def fetch(num, i):
	assert num >= 0, 'fetch does not work with negative numbers'
	return num >> i & 1


def missing_number(A, fetch, tracking=[]):
	if len(A) == 0:
		# building the missing number
		mnum = 0
		for i, x in enumerate(tracking):
			mnum += x*(2**i)
		return mnum
	
	zeros = []
	ones = []
	i = len(tracking)
	for num in A:
		zeros.append(num) if fetch(num, i) == 0 else ones.append(num)
	
	n = len(A)
	nth = fetch(n, 0)
	if len(zeros) > len(ones):
		tracking.append(1)
		return missing_number(ones, fetch, tracking)
	else:
		tracking.append(0)
		return missing_number(zeros, fetch, tracking)



class Test(unittest.TestCase):
	data = list(range(2)) + list(range(3, 10))
	def test_missing_number(self):
		return self.assertEqual(missing_number(self.data, fetch), 2)


if __name__ == '__main__':
	unittest.main()