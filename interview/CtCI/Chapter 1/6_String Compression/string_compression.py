import unittest
import string

def string_compression(s):
	cmps = list(".0")
	letters = set(string.ascii_letters)
	for c in s:
		assert c in letters, "invalid character"
		if cmps[-2] == c:
			cmps[-1] += 1
		else:
			cmps += [c, 1]
	return ''.join(str(x) for x in cmps[2:]) if len(cmps)-2 < len(s) else s

class Test(unittest.TestCase):
	data = (('aaaaabbBBcDaa', 'a5b2B2c1D1a2'), ('abcdeEa', 'abcdeEa'))
	def test_cmps(self):
		for s, cs in self.data:
			self.assertEqual(cs, string_compression(s))

if __name__ == '__main__':
	unittest.main()