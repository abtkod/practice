import unittest

def word_transformer(word1, word2, dictionary):
	visited = {word1: None}
	wordstovisit = [word1]
	while len(wordstovisit) != 0:
		for w in wordstovisit:
			newwords = []
			for i in range(len(w)):
				if w[i] != word2[i] and (w[:i] + word2[i] + w[i+1:]) in dictionary:
					visited[w[:i] + word2[i] + w[i+1:]] = w
					newwords += [w[:i] + word2[i] + w[i+1:]]
				if w == word2:
					path = []
					while w:
						path += [w]
						w = visited[w]
					return path[::-1]
		wordstovisit = newwords			


class Test(unittest.TestCase):
		dictionary = set(['DUKE', 'DATE', 'DAMP', 'LAMP', 'LIKE', 'SUN', 'SAKE', 'SALE', 'TALE', 'LIMP',
				'LIME', 'LOSE', 'LOST', 'LATE', 'BIKE', 'FAKE', 'BUKE', 'BULL', 'BALL'])
		def test_word_transformer(self):
			path = word_transformer('DAMP', 'LIKE', self.dictionary)
			self.assertEqual(path, ['DAMP', 'LAMP', 'LIMP', 'LIME', 'LIKE'])


if __name__ == '__main__':
	unittest.main()
				