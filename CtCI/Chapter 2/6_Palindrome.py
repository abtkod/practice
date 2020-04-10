import unittest
from LinkedList import LinkedList


def palindrome(ll):
	tail = ll.tail
	current = ll.head
	size = len(ll)
	middle = size // 2

	for i in range(middle):
		p = tail.next
		tail.next = current
		n = current.next
		current.next = p
		current = n

	if size % 2 != 0:
		current = current.next

	tail = tail.next
	while tail:
		if current.value != tail.value:
			return False
		current = current.next
		tail = tail.next
	return True

class Test(unittest.TestCase):
	dataT = [list('aaabbcbbcbbaaa'), list('abcba')]
	dataF = [list('ababcabab'), list('aaaacaaa')]

	def test_palindrome(self):
		for l in self.dataT:
			ll = LinkedList()
			ll.add_multiple(l)
			self.assertTrue(palindrome(ll))
		for l in self.dataF:
			ll = LinkedList()
			ll.add_multiple(l)
			self.assertFalse(palindrome(ll))

if __name__ == "__main__":
	unittest.main()

