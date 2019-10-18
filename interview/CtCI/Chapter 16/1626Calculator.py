import unittest

def calculator(equation):	
	stack = []
	operators = ['+', '-', '*', '/']
	current = ''
	res = 1
	prev_op = '+'
	equation = equation + '+'
	for e in equation:
		if e not in operators:
			current += e
		else:
			number = int(current)
			current = ''			

			if e == '+' or e == '-':
				if prev_op == '*':
					number = res * number
				elif prev_op == '/':
					number = res / number
				
				stack.append(number)
				stack.append(e)
				res = 1
			else:
				if prev_op in ['+', '-']:
					res = number
				if prev_op == '*':
					res *= number
				elif prev_op == '/':
					res /= number

			prev_op = e						
		
	res = stack[0]
	for i in range(1, len(stack)-1, 2):		
		if stack[i] == '+':
			res += stack[i+1]
		else:
			res -= stack[i+1]
	return res


def calc(left, op, right):
	if op == '+':
		return left + right
	if op == '-':
		return left - right
	if op == '*':
		return left * right
	if op == '/':
		return left / right

def calculator_two_stack(equation):
	stack_num = []
	stack_opr = [None]
	operators = ['+', '-', '*', '/']
	current = ''
	equation = equation + '+'	
	for i, e in enumerate(equation):		
		if e not in operators:
			current += e
		else:
			number = int(current)
			current = ''		
			
			if stack_opr[-1] in ['*', '/']:
				prev_num = stack_num.pop()
				op = stack_opr.pop()
				num = calc(prev_num, op, number)
				stack_num.append(num)
			else:
				stack_num.append(number)
			stack_opr.append(e)
			
	stack_opr = stack_opr[1:-1] # to remove initial None and last +	
	assert len(stack_num)-1 == len(stack_opr), 'Error'
	result = stack_num[0]
	stack_num = stack_num[1:]

	for i, n in enumerate(stack_num):
		result = calc(result, stack_opr[i], stack_num[i])
	return result

class Test(unittest.TestCase):
	data = [('2*3+5/6*3+15', 23.5), ('5*5*3/6-12+14/2*3', 21.5), ('3*6/5+564-25*25', -57.4)]

	def test_calculator(self):
		for input, actual in self.data:
			self.assertEqual(round(calculator(input), 1), actual)			

	def test_calculator_two_stack(self):
		for input, actual in self.data:
			self.assertEqual(round(calculator_two_stack(input), 1), actual)

if __name__ == '__main__':
	unittest.main()