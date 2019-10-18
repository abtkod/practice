def pond_sizes(matrix):
	def get_previous_cells(i, j, matrix):
		prevs = []
		if i-1>= 0 and j-1 >= 0:
			prevs.append((i-1, j-1))
		if i-1 >= 0:
			prevs.append((i-1, j))
		if i-1 >= 0 and j+1 < len(matrix[0]):
			prevs.append((i-1, j+1))
		if j-1 >= 0:
			prevs.append((i, j-1))
		return prevs

	def build_ponds(zeros, ponds):		
		ponds_list = {}
		for x, y in zeros[-1::-1]:			
			if ponds_list.get((x,y), -1) == -1:
				ponds_list[(x,y)] = []
			
			this_pond = ponds_list[(x,y)]
			this_pond.append((x,y))			

			attached = ponds[(x,y)]
			for ax, ay in attached:
				if ponds_list.get((ax, ay), -1) == -1:
					ponds_list[(ax, ay)] = this_pond
				else:					
					ponds_list[(ax, ay)].extend(this_pond)
					this_pond = ponds_list[(ax, ay)]

			if len(this_pond) > 1:
				# this cell is not the source of pond
				del(ponds_list[(x,y)])
		
		output = []		
		for pond in ponds_list.values():
			# remove duplicated cells
			output.append(list(set(pond)))
		return output

	################################################
	zeros = []
	ponds = {}

	for i, row in enumerate(matrix):
		for j, cell in enumerate(row):
			if cell != 0:
				continue

			zeros.append((i, j))
			prevs_xy = get_previous_cells(i, j, matrix)
			
			ponds[(i, j)] = []
			for px, py in prevs_xy:
				if	matrix[px][py] == 0:
					ponds[(i, j)].append((px, py))
	
	ponds_list = build_ponds(zeros, ponds)
	return list(map(len, ponds_list)), list(ponds_list)


################################################################
def pond_sizes_recursive(matrix):
	def pond(np, i, j, matrix, visit):		
		for m in [i-1, i, i+1]:
			for k in [j-1, j, j+1]:
				if visit.get((m,k), False):
					visit[(m,k)] = False
					np.append((m,k))
					pond(np, m, k, matrix, visit)	

	visit = {}
	for i in range(len(matrix)):
		for j in range(len(matrix[0])):
			visit[(i,j)] = True if matrix[i][j] == 0 else False

	ponds = []
	for i, j in visit:
		if visit[(i, j)]:
			visit[(i,j)] = False
			np = [(i, j)]
			pond(np, i, j, matrix, visit)
			ponds += [np]

	pond_sizes = []
	for p in ponds:
		pond_sizes += [len(p)]
	return pond_sizes, ponds


if __name__ == '__main__':
	import sys
	from random import randint

	x, y = int(sys.argv[1]), int(sys.argv[2])
	matrix = [[randint(0,2) for _ in range(y)] for _ in range(x)]
	print(matrix)
	psize, ponds = pond_sizes(matrix)
	print(sorted(psize))
	print(sorted(ponds))
	psize, ponds = pond_sizes_recursive(matrix)	
	print(sorted(psize))
	print(sorted(ponds))

	print('First approach does not work for:')
	print('[[0, 0, 0, 0],[0,1,0,0],[0,1,0,0],[0,1,0,0]]')