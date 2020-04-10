def permutations(string):
	if len(string) == 1:
		return [string]

	first_char = string[0]
	perms = permutations(string[1:])
	result = []
	for p in perms:
		for i in range(len(p)+1):
			result.append(p[:i] + first_char + p[i:])
	return result

perms = permutations('abcd')
print(len(perms))
print(sorted(perms))