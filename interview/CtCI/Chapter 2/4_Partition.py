import unittest
from LinkedList import LinkedList as LL


def partition(ll, x):	
	right = current = ll.head	
	while current:
		if current.value >= x:			
			while right.value >= x:
				right = right.next				
				if right is None:
					return
			temp = current.value
			current.value = right.value
			right.value = temp			
		current = current.next		
		

ll = LL()
ll.generate(10, 0, 99)
print(ll)
partition(ll, ll.head.value)
print(ll)