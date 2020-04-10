import unittest

def merge_sort(arr, helper=None, low=0, high=None,):
	if high is None:
		high = len(arr) - 1
	if helper is None:
		helper = [None] * len(arr)
	
	if low >= high:
		return
	middle = (low+high) // 2
	merge_sort(arr, helper, low, middle)
	merge_sort(arr, helper, middle+1, high)
	merge(arr, helper, low, middle, high)

def merge(arr, helper, low, middle, high):
	for i in range(low, high+1):
		helper[i] = arr[i]
	current = left = low
	right = middle+1
	while left <= middle and right <= high:
		if helper[left] <= helper[right]:
			arr[current] = helper[left]
			left += 1			
		else:
			arr[current] = helper[right]
			right += 1
		current += 1			
	while left <= middle:
		arr[current] = helper[left]
		current += 1
		left += 1

from random import shuffle
class Test(unittest.TestCase):
	data = list(range(1,15))
	shuffle(data)
	data_sorted = sorted(data)
	
	def test_merge_sort(self):		
		merge_sort(self.data)	
		self.assertEqual(self.data, self.data_sorted)


if __name__ == "__main__":
	unittest.main() 