def pair_of_parentheses(n_pairs):
	if n_pairs == 1:
		return set(['()'])
	pairs = pair_of_parentheses(n_pairs-1)
	new_pairs = set()
	for p in pairs:
		new_pairs.add(f'(){p}')
		for i, ch in enumerate(p):
			if ch == '(':
				new_pairs.add(p[:i+1]+'()'+p[i+1:])		
	return new_pairs


def pair_of_parentheses_fast(output, remained_left, remained_right, substring=""):
	if remained_left == remained_right == 0:
		output.append(substring)
		return
	
	if remained_left > 0:
		pair_of_parentheses_fast(output, remained_left-1, remained_right, substring + '(')
	if remained_right > remained_left:
		pair_of_parentheses_fast(output, remained_left, remained_right-1, substring + ')')

if __name__ == '__main__':
	import sys, time
	pairs = int(sys.argv[1])
	s1 = time.time()
	out1 = pair_of_parentheses(pairs)
	e1 = time.time()	
	out2 = []
	s2 = time.time()
	pair_of_parentheses_fast(out2, pairs, pairs)
	e2 = time.time()
	# print(out1)
	# print(out2)		
	print(len(out1), len(out2))
	print(f'method-1 time: {e1-s1:.2f}s, method-2 time:{e2-s2:.2f}s')