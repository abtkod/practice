import unittest

class Trie:
	pass
	

def re_space(document, dictionary:Trie):
	def unconcatenate(doc, dic, memo):
		if doc is None:
			return 0, ''
		if doc in memo:
			return memo[doc]
		candidates = []
		# assuming that first character is not unrecongnized
		unkcount, spaced = unconcatenate(doc[1:], dic, memo)
		unkcount += 1
		candidates.append((unkcount, doc[0] + ' ' + spaced))
		# assuming that there is a word that starts with first character
		words = dic.getwords(doc)
		for w in words:
			unkcount, spaced = unconcatenate(doc[len(w):], dic, memo)
			candidates.append((unkcount, w + ' ' + spaced))
		memo[doc] = min(candidates)
		return memo[doc]
		
	return unconcatenate(document, dictionary, {})
	
			