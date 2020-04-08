class Trie:
	class TrieNode:
		pass
	
	def __init__(self, words):
		self.head = TrieNode('')
		for word in words:
			self.insert(word)

	def insert(self, word):
		pass

	def nextnode(self, letter, current_node=None):
		pass

def group_by_length(words):
	groups = {}
	for w in words:
		groups.setdefault(len(w), [])
		groups[len(w)].append(w)
	return groups

from itertools import product, permutations
def permutations(words, n, with_replacement=True):
	if with_replacement:
		return product(words, repeat=n)
	else:
		return permutations(words, n)

def build_rectangle(words):
	trie = Trie(words)
	l = len(words[0])	
	for lwords in permutations(words, l):
		trienodes = [None] * l
		rectangle = []
		isvalid = True
		for word in lwords:
			for li, lt in enumerate(word):
				trienodes[li] = trie.nextnode(lt, current_node=trienodes[li])				
				if trienodes[li] is None:
					isvalid = False
					break
				rectangle.append(word)
			if not isvalid:
				break
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