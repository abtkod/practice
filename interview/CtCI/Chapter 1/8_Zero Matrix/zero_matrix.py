# O(MxN) time
# O(MxN) space --> use hash for reduce space to O(N)

import unittest

def zero_matrix(matrix):
	M, N = len(matrix), len(matrix[0])
	changed = [[False] * N] * M

	for i in range(M):
		for j in range(N):
			if matrix[i][j] == 0 and not changed[i][j]:
				for k in range(N):
					matrix[i][k] = 0
					changed[i][k] = True
				for k in range(M):
					matrix[k][j] = 0
					changed[k][j] = True
				continue
	return matrix

class Test(unittest.TestCase):
	matrix = [[1,2,3,4], [1,2,0,4], [1,2,3,4]]
	correct = [[1,2,0,4], [0,0,0,0], [1,2,0,4]]

	def test_zero_matrix(self):
		actual = zero_matrix(self.matrix)
		for i in range(len(actual)):
			for j in range(len(actual[0])):
				self.assertEqual(actual[i][j], self.correct[i][j])

if __name__ == "__main__":
	unittest.main()