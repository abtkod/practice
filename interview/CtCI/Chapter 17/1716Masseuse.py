import unittest

def the_masseuse(appointments): # O(n) time, O(n) space
	def optimal(apps, start, memo={}):
		if start in memo:
			return memo[start]
		
		if start >= len(apps):
			memo[start] = [0]
		elif start == len(apps) - 1:
			memo[start] = [apps[start]]
		else:
			sub1 = optimal(apps, start+1, memo)
			sub2 = optimal(apps, start+2, memo)			
			if sum(sub1) > sum(sub2) + apps[start]:
				memo[start] = sub1
			else:
				memo[start] = [apps[start]] + sub2
		return memo[start]
	return optimal(appointments, 0)

def the_masseuse_iterative(appointments): # O(n) time, O(1) space
	one_away = two_away = 0
	for i in range(len(appointments)-1, -1, -1):
		bestwith = appointments[i] + two_away
		bestwithout = one_away
		current = max(bestwith, bestwithout)
		two_away = one_away
		one_away = current
	return one_away


class Test(unittest.TestCase):
	data = [30, 15, 60, 75, 45, 15, 15, 45]
	def test_the_masseuse(self):
		seq = the_masseuse(self.data)
		print(seq)
		self.assertEqual(sum(seq), 180)
	def test_the_masseuse_iterative(self):
		self.assertEqual(the_masseuse_iterative(self.data), 180)

if __name__ == '__main__':
	unittest.main()
		