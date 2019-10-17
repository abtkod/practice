def sum_swap(l1, l2):
	sum1 = 0
	sum2 = 0
	swapable1 = {}
	for e in l1:
		sum1 += e
	for e in l2:
		sum2 += e
	if sum1 == sum2:
		return (-1, -1)

	diff = abs(sum1 - sum2)
	
	if diff%2 != 0:
		return False
	
	for i, e in enumerate(l1):
		if sum1 < sum2:
			swapable1[e + diff/2] = i
		else:
			swapable1[e - diff/2] = i
	for i, e in enumerate(l2):
		if sum1 < sum2 and e in swapable1:
			l2[i] = l1[swapable1[e]]
			l1[swapable1[e]] = e
			return (swapable1[e], i)
		elif sum1 > sum2 and (e) in swapable1:
			l2[i] = l1[swapable1[e]]
			l1[swapable1[e]] = e
			return (swapable1[e], i)
	return False

if __name__ == "__main__":
	from random import randint
	l1 = [randint(1,20) for _ in range(10)]
	l2 = [randint(1,20) for _ in range(10)]
	print(f'list1: sum={sum(l1)}, list= {l1}')
	print(f'list2: sum={sum(l2)}, list= {l2}')
	success = sum_swap(l1, l2)
	if not success:
		print('Not swapable')
	else:
		print('Equal summation') if success == (-1, -1) else\
								print(f'swapped l1[{success[0]}] with l2[{success[1]}]')
		print(f'new_list1: sum={sum(l1)}, list= {l1}')
		print(f'new_list2: sum={sum(l2)}, list= {l2}')