"""
This script calculates the fraction representation of a repeating decimal number.
It takes a decimal number as input, identifies the repeating part,
and computes the fraction in its simplest form.
"""
from math import gcd


def find_pattern(tail, index, value):
    if index >= len(tail):
        return value, index
    value = tail[:index] == tail[index:2*index]
    if not value:
        return False, None
    return find_pattern(tail[index:], index, value)


def unpack(input):
    if ('.' not in input):
        print('not a decimal number')
        return None, None
    elif not input.endswith('..'):
        print('none repeating decimal detected')
        return input, '0'
    split = input.split('.')[:2]
    tail = split[1]
    if not tail:
        print('not a decimal number')
        return None, None
    print('repeating decimal indicated by user')
    return_list = []
    for index in range(1, len(tail)//2 + 1):
        value, return_index = find_pattern(tail, index, False)
        if value:
            print(f'Found pattern: {tail[:return_index]}\n')
            return input, tail[:return_index]
    print('no repeating decimal pattern detected')
    return input, '0'


def calculate(input):
    input, pattern = unpack(input)
    if not pattern:
        return
    input_list = input.split('.')
    potens = len(input_list[1])
    big_potens = potens + len(pattern)
    small_multiple = int(f'{input_list[0]}{input_list[1]}')
    big_multiple = int(f'{input_list[0]}{input_list[1]}{pattern}')
    # pi*(10**big_potens) - pi*(10**potens) = big_multiple - small_multiple => pi = (big_multiple - small_multiple)/(10**big_potens - 10**potens)
    nominator = big_multiple - small_multiple
    denominator = 10**big_potens - 10**potens
    gcd_ = gcd(nominator, denominator)
    while gcd_ > 1:
        nominator = nominator//gcd_
        denominator = denominator//gcd_
        gcd_ = gcd(nominator, denominator)
    print(f'{nominator}/{denominator} = ' \
        f'{nominator/denominator}')


if __name__ == '__main__':
    input = '3.334..'
    calculate(input)
