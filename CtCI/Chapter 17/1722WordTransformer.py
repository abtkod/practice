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

from collections import deque
def word_transformer_optimal(word1, word2, dictionary):
	def get_groups(word):
		groups = []
		for i in range(len(word)):
			groups.append(word[:i] + '_' + word[i+1:])
		return groups

	def get_adjacent_groups(group, grouptowords):
		adjgroups = set()
		for word in grouptowords[group]:
			adjgroups.update(get_groups(word))
		adjgroups.remove(group)
		return adjgroups

	def transformation(path, group):
		def fill_gaps(w1, w2):
			ix = w1.find('_')
			return w1.replace('_', w2[ix])			

		while path[group][0]:
			gp = group
			group = path[group][0]
			path[group][1] = gp		
		transform = []
		while path[group][1]:
			word = fill_gaps(group, path[group][1])
			transform += [word]
			group = path[group][1]
		return transform

	gptoword = {}
	gen = (word for word in dictionary if len(word) == len(word1))
	for word in gen:
		for gp in get_groups(word):
			gptoword.setdefault(gp, [])
			gptoword[gp].append(word)
	tovisit1, tovisit2 = deque(get_groups(word1)), deque(get_groups(word2))
	path = {**{gp: [word1, None] for gp in tovisit1}, 
			**{gp: [None, word2] for gp in tovisit2}}
	path[word1], path[word2] = [None, None], [None, None]
	while len(tovisit1) != 0 or len(tovisit2) != 0:
		if len(tovisit1) != 0:			
			group = tovisit1.popleft()
			for gp in get_adjacent_groups(group, gptoword):
				path.setdefault(gp, [None, None])
				if path[gp][0] is None:
					path[gp][0] = group
					tovisit1.append(gp)
				if path[gp][1] is not None:
					return transformation(path, gp)
		if len(tovisit2) != 0:			
			group = tovisit2.popleft()
			for gp in get_adjacent_groups(group, gptoword):				
				path.setdefault(gp, [None, None])
				if path[gp][1] is None:
					path[gp][1] = group
					tovisit2.append(gp)
				if path[gp][0] is not None:
					return transformation(path, gp)	
	return False


class Test(unittest.TestCase):
		dictionary = set(['DUKE', 'DATE', 'DAMP', 'LAMP', 'LIKE', 'SUN', 'SAKE', 'SALE', 'TALE', 'LIMP',
				'LIME', 'LOSE', 'LOST', 'LATE', 'BIKE', 'FAKE', 'BUKE', 'BULL', 'BALL'])
		def test_word_transformer(self):
			path = word_transformer('DAMP', 'LIKE', self.dictionary)
			self.assertEqual(path, ['DAMP', 'LAMP', 'LIMP', 'LIME', 'LIKE'])

		def test_word_transformer_optimal(self):
			path = word_transformer_optimal('DAMP', 'LIKE', self.dictionary)
			self.assertEqual(path, ['DAMP', 'LAMP', 'LIMP', 'LIME', 'LIKE'])

if __name__ == '__main__':
	unittest.main()
				