def sub_sort(array):
	low = high = 0
	for i in range(1, len(array)):
		if array[i] < array[i-1]:
			low = i-1
			break
	for i in range(len(array)-2, 0, -1):		
		if array[i] > array[i+1]:
			high = i+1
			break
	
	if low >= high:
		return (-1, -1)
	if high - low == 1:
		min_val = array[high]
		max_val = array[low]
	else:
		min_val = min(array[low+1:high])
		max_val = max(array[low+1:high])
	
	sort_range = [None, None]
	for i in range(low, -1, -1):
		if array[i] <= min_val:
			sort_range[0] = i+1
			break
	for i in range(high, len(array)):
		if array[i] >= max_val:
			sort_range[1] = i-1
			break

	return tuple(sort_range)


if __name__ == '__main__':
	from random import randint
	array = list(range(1, 10, 2)) + [randint(4, 16) for _ in range(5)] + list(range(15, 25, 2))
	print(array)
	print(sub_sort(array))

