import unittest
from math import log


def radix_sort(arr, b): #using dictionary
	assert(all(type(e) is int for e in arr)), 'not integer numbers'	
	D = int(log(max(arr), b)) + 1
	s = {0:arr}
	for n in range(1, D+1):		
		t = s
		s = {}
		gen = (x for x in range(b) if x in t)
		for x in gen:
			for num in t[x]:
				d = nthdigit(n, num, 10)
				if d not in s:
					s[d] = []
				s[d].append(num)
	gen = (x for x in range(b) if x in s)
	current = 0
	for x in gen:
		for num in s[x]:
			arr[current] = num
			current += 1			

def nthdigit(n, num, base=10):
	return (num % (base ** n)) // (base ** (n-1))


from random import randint
class Test(unittest.TestCase):
	data = [randint(1, 100) for _ in range(100000)]
	sorted_data = sorted(data)
	
	def test_radix_sort(self):		
		data = self.data[:]
		radix_sort(data, 10)
		self.assertEqual(data, self.sorted_data)


if __name__ == '__main__':
	unittest.main()
	
	