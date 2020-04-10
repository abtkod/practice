import unittest

def quick_sort(arr, left=0, right=None):
	if right is None:
		right = len(arr) - 1
	index = partition(arr, left, right)
	if left < index-1:
		quick_sort(arr, left, index-1)
	if right > index:
		quick_sort(arr, index, right)

def partition(arr, left, right):
	pivot = arr[(left + right) // 2]
	while left <= right:
		while arr[left] < pivot:
			left += 1
		while arr[right] > pivot:
			right -= 1
		if left <= right:
			temp = arr[left]
			arr[left] = arr[right]
			arr[right] = temp
			left += 1
			right -= 1
	return left


class Test(unittest.TestCase):
	data = list('helloworld')	
	
	def test_quick_sort(self):		
		sorted_data = sorted(self.data)
		quick_sort(self.data)
		self.assertEqual(self.data, sorted_data)


if __name__ == "__main__":
	unittest.main()