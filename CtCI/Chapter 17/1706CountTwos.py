import unittest


def twos_count(n):
	count = 0
	x = 0
	increase = 1
	rate = {1:0}	
	while x != n:
		x += increase		
		if x <= n:
			count += rate[increase]
			if x // increase == 2:
				count += increase			
			if x // increase == 10:
				increase *= 10
				rate[increase] = count
		else:
			if n // increase == 2:
				count += (n % increase) + 1
			if (x - increase) // increase == 2:
				count -= increase
			n %= increase
			x = 0
			increase //= 10
	return count


class Test(unittest.TestCase):
	n = 14228

	def test_twos_count(self):		
		count = 0
		for i in range(self.n+1):
			i = str(i)
			for d in i:
				if d == '2':
					count += 1
		self.assertEqual(twos_count(self.n), count)

import sys
if __name__ == '__main__':
	unittest.main()