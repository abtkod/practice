def pond_sizes(matrix):
	def get_zero_neighbours(i, j, matrix):
		neighbours = []
		for m in [i-1, i, i+1]:
			for k in [j-1, j, j+1]:
				if (m,k) == (i, j):
					continue
				if m < 0 or k < 0 or m >= len(matrix) or k >= len(matrix[0]):
					continue
				if matrix[m][k] == 0:
					neighbours.append((m, k))
		return neighbours

	def build_ponds(attached):		
		ponds = {}		
		for xy in attached.keys():			
			ponds.setdefault(xy, set([xy]))
			for nxy in attached[xy]:
				ponds.setdefault(nxy, set([nxy]))
				if ponds[xy] != ponds[nxy]:
					ponds[xy].update(ponds[nxy])
					ponds[nxy] = ponds[xy]
		
		for k in list(ponds.keys()):
			if k in ponds:
				for k2 in list(ponds[k]):
					if k2 in ponds and k2!=k:
						ponds[k].update(ponds[k2])
						del(ponds[k2])

		return list(map(list, ponds.values()))

		
	################################################	
	attached = {}	
	for i, row in enumerate(matrix):
		for j, cell in enumerate(row):
			if cell != 0:
				continue
						
			adj_xy = get_zero_neighbours(i, j, matrix)
			
			attached[(i, j)] = []
			for px, py in adj_xy:				
				attached[(i, j)].append((px, py))
	
	ponds_list = build_ponds(attached)	
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
	# print(sorted(ponds))
	psize, ponds = pond_sizes_recursive(matrix)	
	print(sorted(psize))
	# print(sorted(ponds))

	print('First method is faulty')