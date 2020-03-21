import unittest
import string

class Trie:
	def __init__(self):
		pass
	

def re_space(document, dictionary:Trie):
	max_word_size = dictionary.max_length()
	def unconcatenate(start, doc, dic, memo):
		if doc is None:
			return 0, ''
		if doc in memo:
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
	
			