class TrieNode:
	def __init__(self, value, terminate=False):
		self.value = value
		self.children = None if terminate else {}
	
	def __str__(self):
		def get_sub(node):
			if node.children is None:
				return [str(self.value)]
			substrings = []
			for childnode in node.children.values():
				substrings += get_sub(childnode)
			return [str(node.value) + sub for sub in substrings]
		return '\n'.join(get_sub(self))


class Trie:
	def __init__(self):
		self.root = TrieNode('')
	
	def insert(self, string):
		assert (string.isalpha()), 'invalid string'
		cur = self.root
		for ch in string:
			if ch not in cur.children:
				cur.children[ch] = TrieNode(ch)
			cur = cur.children[ch]
		cur.children['*'] = TrieNode('*', terminate=True)
	
	def has(self, string):
		assert (string.isalpha()), 'invalid string'		
		cur = self.root
		for ch in string:
			if ch not in cur.children:
				return False
			cur = cur.children[ch]
		return True if '*' in cur.children else False

	def __str__(self):
		return str(self.root)


if __name__ == '__main__':
	words = ['hi', 'hello', 'baby', 'boy', 'contain', 'combat', 'container']
	tr = Trie()
	for word in words:
		tr.insert(word)	
	for w in ['boy', 'contain', 'combat', 'container', 'cata', 'bay', 'boycombat']:
		print(w, tr.has(w))