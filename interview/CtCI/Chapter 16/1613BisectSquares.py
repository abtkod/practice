class Square:	
	def __init__(self, p1, p2, p3, p4):
		p1, p2, p3, p4 = sorted([p1, p2, p3, p4], key=lambda p: (p[1], p[0]))
		# self.points = [p1, p3, p4, p2] # clockwise
		self.points = [p1, p2, p3, p4]
	
	def __str__(self):
		return str(tuple(self.points))


def find_bisect_lines(square):
	def build_line(point1, point2):
		slope = round((point2[1]-point1[1])/(point2[0]-point1[0]), 3)
		intercept = point1[1] - point1[0] * slope
		return slope, intercept

	bisect_lines = set()
	line = f'x = {(square.points[0][0] + square.points[1][0]) / 2}'
	bisect_lines.add(line)
	line = f'y = {(square.points[0][1] + square.points[2][1]) / 2}'
	bisect_lines.add(line)
	ln = build_line(square.points[0], square.points[3])
	line = f'y = {ln[0]}x + {ln[1]}'
	bisect_lines.add(line)
	ln = build_line(square.points[1], square.points[2])
	line = f'y = {ln[0]}x + {ln[1]}'
	bisect_lines.add(line)
	return bisect_lines

def bisect_squares(square1, square2):
	sq1_bsq = find_bisect_lines(square1)
	sq2_bsq = find_bisect_lines(square2)
	bisect_lines = set()
	for line in sq1_bsq:
		if line in sq2_bsq:
			bisect_lines.add(line)
	return False if len(bisect_lines) == 0 else bisect_lines

if __name__ == '__main__':	
	square1 = Square((0,0), (0,4), (4, 0), (4,4))
	square2 = Square((5,0), (5,4), (9, 0), (9,4))
	square3 = Square((0,5), (0,9), (4, 5), (4,9))
	square4 = Square((5,5), (5,9), (9, 5), (9,9))
	square5 = Square((3,3), (3,1), (1, 3), (1,1))	
	print(square1)
	print(square5)
	print(bisect_squares(square1, square5))	
	print(square2)
	print(bisect_squares(square1, square2))
	print(square3)
	print(bisect_squares(square1, square3))
	print(square4)
	print(bisect_squares(square1, square4))