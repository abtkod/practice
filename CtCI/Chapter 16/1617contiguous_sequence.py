from random import randint

def contiguous_sum(num_list):
	max_sum = [num_list[0], 0, 0]
	cur_sum = [num_list[0], 0, 0]
	for i, v in enumerate(num_list[1:], start=1):
		if v >= 0:
			if cur_sum[0] > 0:
				cur_sum[0] += v
				cur_sum[2] = i
			else:
				cur_sum[0] = v
				cur_sum[1] = cur_sum[2] = i
		
		elif v + cur_sum[0] > 0:
			cur_sum[0] += v
			cur_sum[2] = i
			
		elif v > max_sum[0]:
			max_sum[0] = v
			max_sum[1] = max_sum[2] = i
			cur_sum = max_sum[:]
		else:
			cur_sum[0] = v
			cur_sum[1] = cur_sum[2] = i
		
		if cur_sum[0] > max_sum[0]:
			max_sum = cur_sum[:]

	return max_sum

numbers = [randint(-10, 10) for _ in range(20)]
print(numbers)
res = contiguous_sum(numbers)
print(f'max_sum = {res[0]}, from_index:{res[1]}({numbers[res[1]]}) to_index:{res[2]}({numbers[res[2]]})')