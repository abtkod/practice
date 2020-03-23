import unittest

def the_masseuse(appointments):
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


class Test(unittest.TestCase):
	data = [30, 15, 60, 75, 45, 15, 15, 45]
	def test_the_masseuse(self):
		seq = the_masseuse(self.data)
		print(seq)
		self.assertEqual(sum(seq), 180)


if __name__ == '__main__':
	unittest.main()
		