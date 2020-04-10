import unittest

def word_distance_non_repeated(w1, w2, file):
	assert w1 != w2, 'words are the same'
	w1index, w2index = -1 * len(file), len(file)
	w1best, w2best = -1 * len(file), len(file)
	for i, word in enumerate(file, start=1):
		if word != w1 and word != w2:
			continue
		if word == w1:
			w1index = i
		else:
			w2index = i
		if abs(w1index - w2index) < abs(w1best - w2best):
			w1best = w1index
			w2best = w2index
	return abs(w1best - w2best) if abs(w1best - w2best) < len(file) else False

def word_distance_repeated(w1, w2, file):
	assert w1 != w2, 'words are the same'
	windex = {}
	for i, w in enumerate(file, start=1):
		windex.setdefault(w, [])
		windex[w].append(i)	
	if w1 not in windex or w2 not in windex:
		return False

	bestw1, bestw2 = windex[w1][0], windex[w2][0]
	i = j = 0
	while i < len(windex[w1]) and j < len(windex[w2]):
		if abs(bestw1 - bestw2) > abs(windex[w1][i] - windex[w2][j]):
			bestw1, bestw2 = windex[w1][i], windex[w2][j]
		if windex[w1][i] < windex[w2][j]:
			i = i+1
		else:
			j = j+1
	return abs(bestw1 - bestw2)


class Test(unittest.TestCase):
	data = 'abcabcbdbvdskdabvajnjdsbvsbssaabefphfxkjhdsabb'
	def test_word_distance_non_repeated(self):
		self.assertEqual(word_distance_non_repeated('a', 'x', self.data), 6)
	def test_word_distance_repeated(self):
		self.assertEqual(word_distance_repeated('a', 'x', self.data), 6)


if __name__ == '__main__':
	unittest.main()

	
			 
			