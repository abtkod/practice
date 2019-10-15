import unittest
from LinkedList import LinkedList as LL


def sum_backward(ll1, ll2):
	result = LL()
	current1 = ll1.head
	current2 = ll2.head
	c = 0
	while current1 and current2:
		added_value = (current1.value + current2.value + c) % 10
		result.add(added_value)		
		c = (current1.value + current2.value + c) // 10
		current1, current2 = current1.next, current2.next
	if current1 is not None:
		while current1:
			result.add((current1.value+c)%10)
			c = (current1.value+c)//10
			current1 = current1.next
	elif current2 is not None:
		while current2:
			result.add((current1.value+c)%10)
			c = (current1.value+c)//10
			current2 = current2.next
	elif c != 0:
		result.add(c)

	return result


def sum_digit(current1, current2, output):
	if current1.next is None and current2.next is None:
		c, s = (current1.value + current2.value)//10, (current1.value + current2.value)%10
		output.add(s)		
		return c
	c = sum_digit(current1.next, current2.next, output)
	c, s = (current1.value + current2.value + c)//10, (current1.value + current2.value + c)%10
	output.add_to_beginning(s)
	return c


def sum_forward(ll1, ll2):
	output = LL()
	if len(ll1) < len(ll2):
		for i in range(len(ll2)-len(ll1)):
			ll1.add_to_beginning(0)
	if len(ll2) < len(ll1):
		for i in range(len(ll1)-len(ll2)):
			ll2.add_to_beginning(0)

	c = sum_digit(ll1.head, ll2.head, output)		
	if c > 0:
		output.add_to_beginning(c)
	return output


if __name__ == "__main__":
	ll1, ll2, result = LL(), LL(), LL()
	ll1.add_multiple([7, 1, 6])
	ll2.add_multiple([5, 9, 2])
	print(ll1)
	print(ll2)
	print("summing backward:", sum_backward(ll1, ll2))
	print("summing forward:", sum_forward(ll1, ll2))
