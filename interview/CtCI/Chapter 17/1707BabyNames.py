import unittest

def baby_names(frequencies, equivalents):	
	equi = {}
	for name1, name2 in equivalents:
		collection = set([name1, name2])
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


class Test(unittest.TestCase):
	names = [('John', 15), ('Jon', 12), ('Chris', 13), ('Kris', 4), ('Christopher', 19)]
	synonyms = [('Jon', 'John'), ('John', 'Johnny'), ('Chris', 'Kris'), ('Chris', 'Christopher')]
	
	def test_baby_names(self):
		self.assertEqual(baby_names(self.names, self.synonyms), [('John', 27), ('Chris', 36)])


if __name__ == '__main__':
	unittest.main()