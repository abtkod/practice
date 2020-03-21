import unittest
import string

class Trie:
	class Node:
		def __init__(self, data):
			self.data = data
			self.children = {}			
	
	def __init__(self):
		self.root = self.Node(data = '')
		self._max_length = 0

	def __str__(self):
		def read(words, prefix, node):
			if node.data == '*':
				words.append(prefix)
			else:
				for nd in node.children.values():
					read(words, prefix + node.data, nd)
		words = []
		read(words, '', self.root)
		return '\n'.join(words)

	def max_length(self):
		return self._max_length
			

	def add_word(self, word):
		assert word.isalpha(), 'invalid word'
		word = word.lower()
		if self._max_length < len(word):
			self._max_length = len(word)
		node = self.root
		for ch in word:
			if ch not in node.children:
				node.children[ch] = self.Node(data=ch)
			node = node.children[ch]
		node.children['*'] = self.Node('*')
	
	def getwords(self, text):
		assert text.isalpha(), 'invalid word'
		text = text.lower()
		output = []
		node = self.root
		for i, ch in enumerate(text):
			if ch not in node.children:
				break
			node = node.children[ch]
			if '*' in node.children:
				output.append(text[:i+1])			
		return output

def re_space(document, dictionary:Trie):
	max_word_size = dictionary.max_length()
	def unconcatenate(start, doc, dic, memo):
		if start >= len(doc):
			return 0, ''
		if memo[start] is not None:
			return memo[start]
		candidates = []
		# assuming that first character is not unrecongnized
		unkcount, spaced = unconcatenate(start + 1, doc, dic, memo)
		unkcount += 1
		candidates.append((unkcount, doc[start] + ' ' + spaced))
		# assuming that there is a word that starts with first character
		words = dic.getwords(doc[start: start + max_word_size])
		for w in words:
			unkcount, spaced = unconcatenate(start + len(w), doc, dic, memo)
			candidates.append((unkcount, w + ' ' + spaced))
		memo[start] = min(candidates)
		return memo[start]
		
	return unconcatenate(0, document, dictionary, [None]*len(document))
	


if __name__ == '__main__':
	dictionary = Trie()
	for w in ['hello', 'hellow', 'helloworld', 'hi', 'hacker', 'boy', 'world']:
		dictionary.add_word(w)
	print(dictionary)
	print(dictionary.getwords('helloworldthisis'))
	
	dictionary = Trie()
	for w in ['looked', 'just', 'like', 'her', 'brother', 'I', 'reset', 'the', 'computer', 'It', 'still', 'didnt', 'boot']:
		dictionary.add_word(w)
	print(re_space('jesslookedjustliketimherbrother', dictionary))
	print(re_space('iresetthecomputeritreiostillvfsddidntdfgdboot', dictionary))