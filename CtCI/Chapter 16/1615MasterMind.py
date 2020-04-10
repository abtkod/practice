import unittest

def master_mind(solution, guess):
	hits = 0
	sol = {}
	gue = {}
	for slot in zip(guess, solution):
		if slot[0] == slot[1]:
			hits += 1
		else:
			sol.setdefault(slot[0], 0)
			gue.setdefault(slot[1], 0)
			sol[slot[0]] += 1
			gue[slot[1]] += 1
	pseudohits = 0
	for c in sol:		
		gue.setdefault(c, 0)
		pseudohits += min(sol[c], gue[c])
	return hits, pseudohits

class Test(unittest.TestCase):
	data = [(('RRGB', 'RBRR'), (1,2)), (('RYGB', 'YBRG'), (0,4)), (('RGBY', 'RGBY'), (4,0))]

	def test_master_mind(self):
		for ((solution, guess), (hits, pseudohits)) in self.data:
			self.assertEqual(master_mind(solution, guess), (hits, pseudohits))

if __name__ == '__main__':
	unittest.main()