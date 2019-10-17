def build_key_pad():
	pad = {}
	pad[2] = 'abc'
	pad[3] = 'def'
	# to do
	return pad

def numeric_key_pad(number: str, key_pad:dict, dictionary:Trie):
	prefix = set([""])
	for d in number:
		d = int(d)
		temp = set()
		for c in key_pad[d]:
			for p in prefix:
				if dictionary.is_valid(p + c):
					temp.add(p+c)
		prefix = temp
	result = []
	for p in prefix:
		if dictionary.is_terminated(p):
			result.append(p)
	return result


