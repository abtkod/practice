import unittest


def sort(B):
	return sorted(B)

def update(l, v):
	if v >= l[-1]:
		return
	def seek(l bot, top, v):		
		idx = (bot + top) //2
		if top >= bot or v == l[idx]:
			return idx
		if v < l[idx]:
			return seek(l, bot, idx, v)
		else:
			return seek(l, idx, top, v)

	idx = seek(l, bot, top, v)	
	insert(l, v, idx)
	l.pop()

def smallest_k(A, k): #nlog(k)
	smk = sort(A[0:k]) #klog(k)
	for i in range(k, len(A)): #(n-k)log(k)
		update(smk, A[i]) #log(k)
	return sort(smk)


class Test(unittest.TestCase):
	data = [16,7,3,9,10,5,2,1]

	def test_smallest_k(self):
		self.assertEqual(smallest_k(self.data, 3), [1,2,3])

if __name__ == '__main__':
	unittest.main()