import unittest

def volume_of_histogram(bars_arr): # O(nlog(n))
	def histogram_volume(bars, left, right):
		if len(bars) == 0:
			return 0
		(b, h) = bars.pop()
		if left[0] < b < right[0]:			
			return -h + histogram_volume(bars, left, right)
		if b < left[0]:
			volume = (left[0] - b - 1) * h
			return volume + histogram_volume(bars, (b, h), right)
		if b > right[0]:
			volume = (b - right[0] - 1) * h
			return volume + histogram_volume(bars, left, (b, h))
			
		
	bars = [(i, h) for i, h in enumerate(bars_arr) if  h != 0]
	bars.sort(key=lambda x: x[1])
	(b1, h1) = bars.pop()
	(b2, h2) = bars.pop()
	if b1 < b2:
		left, right = (b1, h1), (b2, h2)
	else:
		left, right = (b2, h2), (b1, h1)
	return (right[0] - left[0] - 1) * h2 + histogram_volume(bars, left, right)


class Test(unittest.TestCase):
	bars = [0, 0, 4, 0, 0, 6, 0, 0, 3, 0, 5, 0, 1, 0, 0, 0]
	def test_volume_of_histogram(self):
		self.assertEqual(volume_of_histogram(self.bars), 26)


if __name__ == '__main__':
	unittest.main()	