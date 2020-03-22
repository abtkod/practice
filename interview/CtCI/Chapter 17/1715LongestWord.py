import unittest


def splitword(w, words, mz, memo):
	if w in memo:
		return memo[w]
	if len(w) < 2*mz and w not in words:
		return False
	if w in words:		
		memo[w] = [w]
		return memo[w]
	gen = (i for i in range(mz, len(w)-mz) if w[:i] in words)
	for i in gen:
		splitted = splitword(w[i:], words, mz, memo)
		if splitted:
			return [w[:i]] + splitted
	

def longest_word(words):
	words = set(words)
	minsize = float('inf')
	maxsize = -1 * float('inf')
	zw = {}
	for w in words:
		zw.setdefault(len(w), [])
		zw[len(w)].append(w)
		if len(w) > maxsize:
			maxsize = len(w)
		if len(w) < minsize:
			minsize = len(w)
	gen = (size for size in range(maxsize, minsize-1, -1) if size in zw)
	memo = {}
	for size in gen:
		for word in zw[size]:
			words = words.difference([word])			
			splitted = splitword(word, words, minsize, memo)
			if splitted:
				print(splitted)
				return ''.join(splitted)
	return False


class Test(unittest.TestCase):
	data = ['cat', 'banana', 'dog', 'nana', 'walk', 'walker', 'nanacatnananbananawalker', 'bananananadogwalker']
	def test_longest_word(self):
		lg = longest_word(self.data)
		self.assertEqual(lg, 'bananananadogwalker')

if __name__ == '__main__':
	unittest.main()