import unittest

def is_sorted(arr):
	return all(arr[i] <= arr[i+1] for i in range(len(arr)-1))

def bs(x, arr, left, right):	
	if left > right:
		return False
	middle = (left + right) // 2
	if x == arr[middle]:
		return middle
	if x < arr[middle]:
		return bs(x, arr, left, middle-1)
	elif x > arr[middle]:
		return bs(x, arr, middle+1, right)


def binary_search(arr, x):
	assert (is_sorted(arr)), 'array is not sorted'
	return bs(x, arr, 0, len(arr)-1)


class Test(unittest.TestCase):
	dataT = list(range(11))
	dataF = list(range(11, 20))

	def test_binary_search(self):
		self.assertEqual(binary_search(self.dataT, 5), 5)
		self.assertFalse(binary_search(self.dataF, 5))


if __name__ == "__main__":
	unittest.main()
