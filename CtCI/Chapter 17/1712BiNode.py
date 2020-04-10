class BiNode:
	def __init__(self, data, nodel=None, noder=None):
		self.data = data
		self.nodel = nodel
		self.noder = noder
	
	def __str__(self):
		return str(self.data)

	def linkedlist_representation(self):
		if self.noder is None:
			return str(self)
		return f'{str(self)} -> {self.noder.linkedlist_representation()}'

	def tree_representation(self):
		left = right = '_'
		if self.nodel is not None:
			left = self.nodel.tree_representation()
		if self.noder is not None:
			right = self.noder.tree_representation()
		return f'({left} {str(self)} {right})'

def bst_to_linkedlist(root):
	def inorder(current):
		if current.nodel is None:
			smallest_left = current
		else:
			smallest_left, greatest_left = inorder(current.nodel)
			greatest_left.noder = current
			current.nodel = greatest_left
		if current.noder is None:
			greatest_right = current
		else:
			smallest_right, greatest_right = inorder(current.noder)
			smallest_right.nodel = current
			current.noder = smallest_right
		return smallest_left, greatest_right
	head, tail = inorder(root)
	return head, tail


if __name__ == '__main__':
	nodes = [BiNode(i) for i in range(12)]
	nodes[1].noder = nodes[2]
	nodes[3].nodel = nodes[1]
	nodes[4].nodel = nodes[3]
	nodes[4].noder = nodes[8]
	nodes[8].nodel = nodes[6]
	nodes[6].noder = nodes[7]
	nodes[8].noder = nodes[10]
	nodes[10].nodel = nodes[9]
	
	print(nodes[4].tree_representation())
	head, tail = bst_to_linkedlist(nodes[4])
	print(head.linkedlist_representation())