form LinkedList import LinkedList

def intersect(ll1, ll2):
	if ll1.tail is not ll2.tail:
		return None

	h1 = ll1.head
	h2 = ll2.head
	s1, s2 = len(ll1), len(ll2)
	
	if s1 < s2:
		for i in range(s2-s1):
			h2 = h2.next
	elif s2 < s1:
		for i in range(s1-s2):
			h1 = h1.next

	while h1 is not h2:
		h1 = h1.next
		h2 = h2.next

	return h1


