import unittest


def letters_and_numbers(string):
	letcount = numcount = 0
	for s in string:
		if str.isdigit(s):
			numcount += 1
		else:
			letcount += 1
	beg, end = 0, len(string) - 1
	check_func = str.isdigit if letcount < numcount else str.isalpha
	(small, big) = (letcount, numcount) if letcount < numcount else (numcount, letcount)	
	while small < big:
		if check_func(string[beg]):
			beg += 1
			big -= 1
		elif check_func(string[end]):
			end -= 1
			big -= 1
		else:
			big += 1
			small -= 1
	return string[beg:end+1]


class Test(unittest.TestCase):
	data = 'A1AAA111A1AA11AAAAAA'
	result = 'A1AAA111A1AA11'
	def test_letters_and_numbers(self):
		output = letters_and_numbers(self.data)
		print(output)
		self.assertEqual(len(output), len(self.result))

if __name__ == '__main__':
	unittest.main()