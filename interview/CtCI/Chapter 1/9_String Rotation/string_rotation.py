# O(s1 + s2)

import unittest

def string_rotation(s1, s2, isSubstring):
	if len(s1) != len(s2):
		return False
	s = s2 + s2 + s2 + s2[-1::-1] + s2[-1::-1]
	return isSubstring(s1, s)

def is_substring(short, long):
	return long.find(short) != -1
	# return short in long

class Test(unittest.TestCase):
	data = [
        ('waterbottle', 'erbottlewat', True),
        ('water', 'retaw', True),
        ('foo', 'bar', False),
        ('foo', 'foofoo', False)
    ]

	def test_rotation(self):
		for s1, s2, actual in self.data:
			self.assertEqual(string_rotation(s1, s2, is_substring), actual)

if __name__ == "__main__":
	unittest.main()