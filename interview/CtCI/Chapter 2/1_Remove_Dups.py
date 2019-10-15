import unittest
from LinkedList import LinkedList as LL


def remove_dups(ll):
	if len(ll) <= 1:
		return

	dups = {}
	prev = None
	for current in ll:
		v = current.value
		if dups.get(v, False) is False:
			dups[v] = True
			prev = current
		else:
			prev.next = current.next


def remove_dups_followup(ll):
	if len(ll) <= 1:
		return
	
	current = ll.head
	while current:
		val = current.value
		prev = current
		runner = current.next
		while runner:
			if runner.value == val:
				prev.next = runner.next
			else:
				prev = runner
			runner = runner.next
		current = current.next


class Test(unittest.TestCase):
	data = [('abcaabacda', 'abcd')]
	def test_remove(self):
		for dp, rm in self.data:
			dpl, rml = LL(), LL()
			dpl.add_multiple(list(dp))
			rml.add_multiple(list(rm))
			remove_dups(dpl)			
		self.assertEqual(str(dpl), str(rml))

	def test_remove_followup(self):
		for dp, rm in self.data:
			dpl, rml = LL(), LL()
			dpl.add_multiple(list(dp))
			rml.add_multiple(list(rm))			
			remove_dups_followup(dpl)
		self.assertEqual(str(dpl), str(rml))

if __name__ == "__main__":
	unittest.main()