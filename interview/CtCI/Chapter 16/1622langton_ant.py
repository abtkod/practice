from random import choice

def rotate_direction(xy, direction, is_clock_wise):
	clock_wise = {'r':'d', 'd':'l', 'l':'u', 'u':'r'}
	c_clock_wise = {'r':'u', 'u':'l', 'l':'d', 'd':'r'}
	xy_change = {'r':(1,0), 'l':(-1,0), 'u':(0,1), 'd':(0,-1)}

	new_direction = clock_wise[direction] if is_clock_wise else c_clock_wise[direction]
	change = xy_change[new_direction]
	xy = (xy[0] + change[0], xy[1] + change[1])	
	return xy, new_direction

def ant_k_moves(k):
	grid_before = {}
	grid_after = {}
	xy = (0, 0)
	direction = 'r'
	path = []
	for _ in range(k):		
		if xy not in grid_after:
			cur_cell_color = choice(['b', 'w'])
			grid_after[xy] = grid_before[xy] = cur_cell_color
		cur_cell_color = grid_after[xy]
		path.append((direction, xy, cur_cell_color))
		if cur_cell_color == 'w':
			grid_after[xy] = 'b'
			xy, direction = rotate_direction(xy, direction, is_clock_wise=True)
		else:
			grid_after[xy] = 'w'
			xy, direction = rotate_direction(xy, direction, is_clock_wise=False)
	
	grid_before = sorted(grid_before.items(), key=lambda x: x[0])
	grid_after = sorted(grid_after.items(), key=lambda x: x[0])
	return grid_before, grid_after, path


if __name__ == '__main__':
	import sys
	k = int(sys.argv[1])
	grid_before, grid_after, path = ant_k_moves(k)
	print('before:', grid_before)
	print('after: ', grid_after)
	print(path)
