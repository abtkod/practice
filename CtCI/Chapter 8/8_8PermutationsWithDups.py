def permutations_with_dups(string):
	if len(string) == 1:
		return set([string])

	first_char = string[0]
	perms = permutations_with_dups(string[1:])
	result = set()
	for p in perms:
		for i in range(len(p)+1):
			result.add(p[:i] + first_char + p[i:])
	return result


if __name__ == "__main__":
	import sys
	string = sys.argv[1]
	perms = permutations_with_dups(string)
	print(f'string: {string} \npermutations: {len(perms)}')
	print(sorted(perms))
