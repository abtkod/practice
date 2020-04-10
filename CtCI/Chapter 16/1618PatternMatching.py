import unittest

def match_pattern(a, b, pattern, value, a_value, b_value):	
	aindex = bindex = 0
	for p in pattern:
		vindex = aindex * len(a_value) + bindex * len(b_value)
		if p == a:
			aindex += 1			
			if value[vindex: vindex + len(a_value)] != a_value:			
				return False
		else:			
			bindex += 1			
			if value[vindex: vindex + len(b_value)] != b_value:
				return False	
	return True

def pattern_matching(pattern, value):	
	a = pattern[0]
	b = None
	a_count = b_count = beginning_a = 0
	for p in pattern:
		if  b is None and p != a:			
			b = p
			beginning_a = a_count
		if p == a:
			a_count += 1
		else:
			b_count += 1
		
	for i in range(1, len(value)+1):
		a_value = value[:i]
		for j in range(beginning_a*i, len(value)):
			b_value = value[beginning_a*i: j+1]
			if len(a_value)*a_count + len(b_value) * b_count == len(value):
				matching = match_pattern(a, b, pattern, value, a_value, b_value)
				if matching:
					return True
	return False


class Test(unittest.TestCase):
	dataT = [('aabab', 'catcatgocatgo'), ('ab', 'catcatgocatgo'), ('abb', 'catcatgocatgo')]
	dataF = [('aabaa', 'catcatgocatgo'), ('abba', 'catcatgocatgo')]

	def test_pattern_matching(self):
		for pattern, value in self.dataT:
			self.assertTrue(pattern_matching(pattern, value))
		for pattern, value in self.dataF:
			self.assertFalse(pattern_matching(pattern, value))


if __name__ == "__main__":
	unittest.main()