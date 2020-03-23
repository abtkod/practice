import unittest

def shortest_supersequence(short, long):
	track = {v:-len(long) for v in short}
	shortest, res = len(long), (0, len(long))
	for i, v in enumerate(long):
		if v in track.keys():
			track[v] = i
			indices = track.values()
			minix, maxix = min(indices), max(indices)
			if maxix - minix < shortest:
				shortest = maxix - minix
				res = (minix, maxix)
	return res


class Test(unittest.TestCase):
	short = [1, 5, 9]
	long  = [7, 5, 9, 0, 2, 1, 3, 5, 7, 9, 1, 1, 5, 8, 8, 9, 7]
	
	def test_shortest_supersequence(self):
		self.assertEqual(shortest_supersequence(self.short, self.long), (7, 10))


if __name__ == '__main__':
	unittest.main()