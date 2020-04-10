class Node:
	
	def __init__(self, value, left=None, right=None):
		self.value = value
		self.left = left
		self.right = right

	def __str__(self):		
		return f'({str(self.left)}:L V:{self.value} R:{self.right})'

def minimal_tree(arr):
	if len(arr) == 1:
		return Node(arr[0])
	if len(arr) == 2:
		return Node(arr[1], Node(arr[0]))
	if len(arr) == 3:
		return Node(arr[1], Node(arr[0]), Node(arr[2]))

	mid = len(arr) // 2
	return Node(arr[mid], minimal_tree(arr[:mid]), minimal_tree(arr[mid+1:]))


print(minimal_tree(list(range(1,7))))