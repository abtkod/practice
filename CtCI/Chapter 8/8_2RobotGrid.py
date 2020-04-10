def mask(grid, direction):
	masked = []
	if direction == 'r':
		for row in grid:
			masked.append(row[1:])
	elif direction == 'd':
		masked = grid[1:]
	return masked

def robot_in_grid(grid, m={}):	
	r = len(grid)
	c = len(grid[0])
	if r == 1 and c == 2:
		return 'r.'
	if r == 2 and c == 1:
		return 'd.'

	if m.get((r,c), -1) != -1 and m.get((r,c), -1) != 'fail':
		return m[(r,c)]
	if m.get((r,c), -1) == 'fail':
		return 'fail'
	if m.get((r,c), -1) == -1:
		if c > 0:
			if grid[0][1]:
				sol = robot_in_grid(mask(grid, 'r'), m)
				if sol != 'fail':
					return 'r'+sol
		if r > 0:
			if grid[1][0]:
				sol = robot_in_grid(mask(grid, 'd'), m)
				if sol != 'fail':
					return 'd'+sol
	return 'fail'


if __name__ == "__main__":
	grid = [[True, True, False, False], 
			[False, True, True, False], 
			[True, False, True, False], 
			[True, False, True, False], 
			[True, False, True, True]] 	
	print(robot_in_grid(grid))
