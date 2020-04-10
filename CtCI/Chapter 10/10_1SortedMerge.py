def shift_to_end(arr, count):
	p = len(arr) - count - 1
	for i in range(len(arr)-count):
		arr[-i-1] = arr[p-i]
		arr[p-i] = None
	return arr
	

def sorted_merge(arrA, arrB):
	arrA = shift_to_end(arrA, len(arrB))	
	pA = len(arrB)
	p = pB = 0
	while pB != len(arrB):
		if arrA[pA] < arrB[pB]:
			arrA[p] = arrA[pA]
			pA += 1			
		else:
			arrA[p] = arrB[pB]
			pB += 1
		p += 1
		while pA == len(arrA) and pB != len(arrB):
			arrA[p] = arrB[pB]
			p += 1
			pB +=1

arrB = list(range(1, 11, 2))
arrA = list(range(1, 21, 3)) + [None] * len(arrB)
print(arrA)
print(arrB)
sorted_merge(arrA, arrB)
print(arrA)

