import unittest

def sort_function(A, index):
	A.sort(key=lambda x: x[index])

def circus_tower(people, sortf=sort_function):
	sortf(people, 0)
	sortf(people, 1)
	tower = []
	base = 0
	people.append((-1, -1))	
	for i in range(1, len(people)):
		if people[i][0] <= people[i-1][0] or people[i][1] <= people[i-1][1]:			
			if i-base > len(tower):
				tower = (base, i)
			base = i	
	return people[tower[0]: tower[1]]



class Test(unittest.TestCase):
	people = [(65, 100), (70, 150), (56, 90), (75, 190), (60, 95), (68, 110), (66, 90)]
	output = [(60, 95), (65, 100), (68, 110), (70, 150), (75, 190)]
	def test_circus_tower(self):
		self.assertEqual(self.output, circus_tower(self.people))


if __name__ == '__main__':
	unittest.main()