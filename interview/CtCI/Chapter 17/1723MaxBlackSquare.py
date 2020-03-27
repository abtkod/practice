import unittest


class Border:
	def __init__(self, sx, sy, ex, ey):
		self.sx, self.sy, self.ex, self.ey = sx, sy, ex, ey

	def __repr__(self):
		return str(((self.sx, self.sy), (self.ex, self.ey)))


def assign_cell_to_borders(matrix):
	cells = {}
	for i in range(len(matrix)):
		curborder = None
		for j in range(len(matrix[0])):
			if matrix[i][j] == 'B':
				if curborder is None:
					curborder = Border(i, j, i, j)
				else:
					curborder.ex, curborder.ey = i, j
				cells.setdefault((i, j), [None, None])
				cells[(i, j)][0] = curborder
	for j in range(len(matrix[0])):
		curborder = None
		for i in range(len(matrix)):
			if matrix[i][j] == 'B':
				if curborder is None:
					curborder = Border(i, j, None, None)
				else:
					curborder.ex, curborder.ey = i, j
				cells.setdefault((i, j), [None, None])
				cells[(i, j)][1] = curborder			
	return cells
			
def max_black_square(matrix):
	assert (len(matrix) == len(matrix[0])), 'matrix is not square'
	borders = assign_cell_to_borders(matrix)

	for size in range(len(matrix), 0, -1):
		for r in range(0, len(matrix) - size + 1):
			for c in range(0, len(matrix) - size + 1):
				cel1, cel2, cel3, cel4 = (r, c), (r, c+size-1), (r+size-1, c), (r+size-1, c+size-1)
				check = all(cell in borders for cell in (cel1, cel2, cel3, cel4))
				if not check:
					continue
				if borders[cel1][0] is borders[cel2][0] and borders[cel3][0] is borders[cel4][0] and \
					borders[cel1][1] is borders[cel3][1] and borders[cel2][1] is borders[cel4][1]:
					return (cel1, cel2, cel3, cel4)

class Test(unittest.TestCase):
	matrix = [['W', 'W', 'W', 'B', 'B'], ['W', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'W', 'B'], ['W', 'B', 'B', 'W', 'B'], ['B', 'B', 'B', 'B', 'B']]
	
	def test_max_black_square(self):
		self.assertEqual(max_black_square(self.matrix), ((1, 1), (1, 4), (4, 1), (4, 4)))


if __name__ == '__main__':
	unittest.main()