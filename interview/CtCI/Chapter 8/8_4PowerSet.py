def powerset(input):
	output = []
	output.append(set())
	for e in input:
		e_added = []		
		for sb in output:
			e_added.append(sb.union(set([e])))
		output += e_added
	return output

def powerset_recursive(input):
	if len(input) == 0 :
		return [set()]
	e = input.pop()
	subsets = powerset_recursive(input)
	e_add = []
	for sb in subsets:
		e_add.append(sb.union(set([e])))
	return subsets + e_add

test_set = set([1,2,3])
print(powerset(test_set))
print(powerset_recursive(test_set))