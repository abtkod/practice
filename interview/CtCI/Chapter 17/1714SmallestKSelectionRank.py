import random
import unittest

def smallest_k(A, k):
	def selection_rank(A, start, end, m):
		rnd = random.randint(start, end)
		pivot = A[rnd]
		lp = start
		hp = end
		while lp <= hp:
			while A[lp] < pivot:
				lp += 1
			while A[hp] > pivot:
				hp -= 1
			if lp <= hp:
				tmp = A[lp]
				A[lp] = A[hp]
				A[hp] = tmp
				lp += 1
				hp -= 1
		if lp - start == m:
			return lp
		if lp - start > m:
			return selection_rank(A, start, lp - 1,  m)
		else:
			return selection_rank(A, lp, end, m - lp + start)			
	ix = selection_rank(A, 0, len(A)-1, k)
	return sorted(A[:ix])
			

class Test(unittest.TestCase):
	data = [22,99,16,7,3,9,10,5,2,1,17]
	
	def test_smallest_k(self):
		self.assertEqual(smallest_k(self.data, 4), [1,2,3,5])

if __name__ == '__main__':
	unittest.main()