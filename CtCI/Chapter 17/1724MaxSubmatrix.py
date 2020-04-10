import unittest


def calc_sum(topleft, bottomright, subsums):
	tlx, tly = topleft
	brx, bry = bottomright
	toprow = subsums[(tlx-1, bry)] if tlx-1 >= 0 else 0
	leftcol = subsums[(brx, tly-1)] if tly-1 >= 0 else 0
	common = subsums[(tlx-1, tly-1)] if tlx-1 >= 0 and tly-1 >= 0 else 0
	return subsums[(brx, bry)] - toprow - leftcol + common

def max_submatrix(matrix): # O(n^4)
	subsums = {}
	maxsub = None
	for i in range(len(matrix)):
		for j in range(len(matrix[0])):
			r = subsums[(i-1, j)] if i-1 >= 0 else 0
			c = subsums[(i, j-1)] if j-1 >= 0 else 0
			z = subsums[(i-1, j-1)] if i-1 >= 0 and j-1 >= 0 else 0
			subsums[(i, j)] = matrix[i][j] + r + c - z	
	maxsum, maxmat = calc_sum((0, 0), (len(matrix)-1, len(matrix[0])-1), subsums), matrix
	for i in range(len(matrix)):
		for j in range(len(matrix[0])):
			for k in range(i, len(matrix)):
				for l in range(j, len(matrix[0])):
					val = calc_sum((i, j), (k, l), subsums)
					if val > maxsum:
						maxsum = val
						maxmat = [[matrix[a][b] for b in range(j, l+1)] for a in range(i, k+1)]
	return maxsum, maxmat
					

class Test(unittest.TestCase):
	matrix = [[-20, 4, -6, 3], [3, -5, 100, -2], [-15, 50, -5, 0], [1, 4, -10, 2]]

	def test_max_submatrix(self):
		maxsum, maxmat = max_submatrix(self.matrix)
		m, M = '', ''
		for r in self.matrix:
			M += ' '.join(map(str, r))
			M += '\n'
		for r in maxmat:
			m += ' '.join(map(str, r))
			m += '\n'
		print(M)
		print('-'*10)
		print(m)
		self.assertEqual(maxsum, 140)


if __name__ == '__main__':
	unittest.main()