import string
from random import choice
def hash_char_function():
	hf = {}
	for i, c in enumerate(string.ascii_letters):
		hf[c] = pow(5, i)/10
	return hf

def hash_function(string):
	hf = hash_char_function()
	hash_key = 0
	for c in string:
		hash_key += hf[c]
	return hash_key

def rebuild_list(groups):
	l = []
	grps = groups.values()
	grps = sorted(grps, reverse=True, key=len)
	for gr in grps:
		for v in gr:
			l.append(v)
	return l

def group_anagrams(strlist):
	grouping = {}
	for st in strlist:
		hash_key = hash_function(st)
		if grouping.get(hash_key, -1) == -1:
			grouping[hash_key] = [st]
		else:
			grouping[hash_key].append(st)
	return rebuild_list(grouping)

def generate_strings(strlength, count):
	str_list = []
	for i in range(count):
		st = ""
		for _ in range(strlength):
			st += choice(string.ascii_lowercase)
		str_list.append(st)
	return str_list

strings = generate_strings(2, 30)
print(strings)
print(group_anagrams(strings))