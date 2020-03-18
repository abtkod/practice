def random_set(m, st, random_function):	
	assert (m <= len(st)), 'm is greater than n'
	for i in range(m):
		ix = random_function(i, len(st)-1)
		tmp = st[ix]
		st[ix] = st[i]
		st[i] = tmp
	return set(st[:m])


import sys
if __name__ == "__main__":
	m, n = int(sys.argv[1]), int(sys.argv[2])
	from random import randint	
	print(random_set(m, list(range(n)), randint))
