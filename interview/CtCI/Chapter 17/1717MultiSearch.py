import unittest
import string

def multi_search(bigstr, arrstr):
	ltos = {}
	minsize = len(bigstr) + 1
	maxsize = 0
	strindex = {st:[] for st in arrstr}
	for st in arrstr:
		ltos.setdefault(st[0], [])
		ltos[st[0]].append(st)
		if len(st) > maxsize:
			maxsize = len(st)
		if len(st) < minsize:
			minsize = len(st)
	for index in range(len(bigstr) - minsize + 1):
		letter = bigstr[index]
		if letter not in ltos:
			continue
		for st in ltos[letter]:
			if bigstr[index: index + len(st)] == st:
				strindex[st].append((index, index + len(st)))
	return strindex

class Test(unittest.TestCase):
	b = 'doghelloboyboycatcarcartbobobobdogwalkergomissingbabyocat'
	T = ['dog', 'dogwalker', 'hello', 'boy', 'cat', 'car', 'can', 'bob']
	def test_multi_search(self):
		res = multi_search(self.b, self.T)
		print(res)
		for word in res:
			for startindex, endindex in res[word]:				
				self.assertEqual(word, self.b[startindex:endindex])

if __name__ == '__main__':
	unittest.main()