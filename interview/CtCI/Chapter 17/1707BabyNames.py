import unittest

def baby_names(frequencies, equivalents):	
	equi = {}
	for name1, name2 in equivalents:
		collection = set((name1, name2))
		if name1 in equi:
			collection.union(equi[name1])
		if name2 in equi:
			collection.union(equi[name2])
		for name in collection:
			equi[name] = collection
	for name in equi:
		equi[name] = min(equi[name])
	output = {x:0 for x in equi.values()}
	for name, freq in frequencies:
		output[equi[name]] += freq
	return list(output.items())

def baby_names_optimized(names, synonyms):
	counts = {x:f for x,f in names}
	for name1, name2 in synonyms:
		lookup1 = name1
		counts.setdefault(lookup1, 0)
		while not str.isdigit(str(counts[lookup1])):			
			lookup1 = counts[lookup1]			
		lookup2 = name2
		counts.setdefault(lookup2, 0)
		while not str.isdigit(str(counts[lookup2])):			
			lookup2 = counts[lookup2]			
		cnt = counts[lookup1] + counts[lookup2]
		deleg = min(lookup1, lookup2)
		counts[deleg] = cnt
		if deleg != name1:
			counts[name1] = deleg
		if deleg != name2:
			counts[name2] = deleg
	for name in list(counts.keys()):
		if not str.isdigit(str(counts[name])):
			del(counts[name])
	return list(counts.items())
		

class Test(unittest.TestCase):
	names = [('John', 15), ('Jon', 12), ('Chris', 13), ('Kris', 4), ('Christopher', 19)]
	synonyms = [('Jon', 'John'), ('John', 'Johnny'), ('Chris', 'Kris'), ('Chris', 'Christopher')]
	
	def test_baby_names(self):
		self.assertEqual(baby_names(self.names, self.synonyms), [('John', 27), ('Chris', 36)])
	
	def test_baby_names_optimized(self):
		self.assertEqual(baby_names_optimized(self.names, self.synonyms), [('John', 27), ('Chris', 36)])


if __name__ == '__main__':
	unittest.main()