"""
Convert a number from any base between 2-36 to any other base between base 2-36

"""

sign_list = [
	'0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
	'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
	'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
	'U', 'V', 'W', 'X', 'Y', 'Z',
]

def base_10_to_base_A(integer=0, base_to=2, exponent_list=None):
	if not exponent_list:
		exponent_list = list()
	next_exponent = integer // base_to
	if next_exponent > base_to - 1:
		exponent_list.append(integer % base_to) 
		return_list = base_10_to_base_A(next_exponent, base_to, exponent_list)
	else:
		exponent_list.append(integer % base_to)
		exponent_list.append(next_exponent)
		return_list = []
		for i in range(1, len(exponent_list)+1):
			return_list.append(sign_list[exponent_list[-i]])
	return ''.join(return_list)


def base_A_to_base_10(int_string='0', base_from=2, exponent_list=None):
	if not exponent_list:
		exponent_list = list()
	int_list = list(int_string)
	reverse_int_list = int_list[::-1]
	base_10_list = []
	exponent = 0
	for i in reverse_int_list:
		base_10_list.append(sign_list.index(i) * base_from**(exponent))
		exponent += 1
	return sum(base_10_list)


def base_A_to_base_B(integer='0', base_from=2, base_to=10):
	if type(integer == int) and base_from == 10:
		pass
	else:
		integer = str(integer)

	if base_from == 10:
		return(base_10_to_base_A(integer, base_to, []))
	elif base_to == 10:
		return(base_A_to_base_10(integer, base_from, []))
	else:
		base_10 = base_A_to_base_10(integer, base_from, [])
		base_B = base_10_to_base_A(int(base_10), base_to, [])
		return(base_B)


print(base_A_to_base_B(integer=127, base_from=10, base_to=2))

