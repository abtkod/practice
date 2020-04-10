import unittest


class Trie:
	class TrieNode:
		def __init__(self, value):
			self.value = value
			self.children = {}

		def nextnode(self, value):
			return self.children.get(value, None)

		def terminated(self):
			return True if '*' in self.children else False

	
	def __init__(self, words):
		self.head = self.TrieNode('')
		for word in words:
			self.insert(word)

	def insert(self, word):
		node = self.head
		for letter in word:
			node.children.setdefault(letter, self.TrieNode(letter))
			node = node.children[letter]
		node.children['*'] = self.TrieNode('*')

	def next(self, letter, current_node=None):
		assert (current_node is None or type(current_node) is self.TrieNode), 'invalid current node'
		return self.head if current_node is None else current_node.nextnode(letter)

def group_by_length(words):
	groups = {}
	for w in words:
		groups.setdefault(len(w), [])
		groups[len(w)].append(w)
	return groups

def permutate(words, n, with_replacement):
	from itertools import product, permutations
	if with_replacement:
		return product(words, repeat=n)
	else:
		return permutations(words, n)

def build_rectangle(words):
	trie = Trie(words)
	l = len(words[0])	
	for lwords in permutate(words, l, with_replacement=False):		
		trienodes = [trie.head] * l
		rectangle = []
		isvalid = True		
		for wi in range(len(lwords)-1, -1, -1):
			word = lwords[wi] # improve chance by reading permutations in reverse direction
			for li, lt in enumerate(word):
				trienodes[li] = trie.next(lt, current_node=trienodes[li])				
				if trienodes[li] is None:
					isvalid = False
					break			
			if not isvalid:
				break
			rectangle.append(word)
		if len(rectangle) == l:
			return rectangle
	return False
	
def word_rectangle(words_list):
	groups = group_by_length(words_list)
	for size in sorted(groups.keys(), reverse = True):
		rect = build_rectangle(groups[size])
		if rect:
			return rect
	return False


class Test(unittest.TestCase):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		import string, random
		words = set(['mind', 'idea', 'neat', 'data'])
		needed = 20
		for size in range(2, 6):			
			c = 0
			while c != needed:
				word = random.sample(string.ascii_lowercase, size)
				word = ''.join(word)
				if word in words:
					continue
				words.add(word)
				c += 1						
		self.words_list = list(words)
		self.words_list.sort()
		self.words_list.sort(key= lambda x: len(x))
		print(self.words_list)

	def test_word_rectangle(self):
		rectangle = word_rectangle(self.words_list)
		self.assertTrue(rectangle)		
		inv = [''] * len(rectangle)
		for i in range(len(rectangle)):			
			for j in range(len(rectangle[0])):
				inv[j] += rectangle[i][j]
		print('\n'.join(rectangle))
		print('-'*5)
		print('\n'.join(inv))
		wordset = set(self.words_list)
		for w in rectangle:
			self.assertTrue(w in wordset)
		for w in inv:
			self.assertTrue(w in wordset)


if __name__== '__main__':
	unittest.main()
