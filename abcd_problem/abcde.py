"""ORIGINAL PROBLEM:

Let | be the concatenate operator. Now find all relations

A|B|C|D * E = D|C|B|A

such that A,B,C,D \in {0,1,2,3,4,5,6,7,8,9}.

GENERALIZED:

Find all relations
K_1|K_2|...|K_n * K_{n+1} = K_n|K_{n-1}|...|K_1
s.t. K_i \in {0,..,9}

"""
from time import perf_counter


def find_palindromes(lower, upper, stop):
    solutions = {
                    'Range': f'{lower} - {stop}',
                    'Solutions': []
                }
    start = perf_counter()
    for abcd in range(lower, upper):
        dcba = 0
        while dcba <= stop:
            for e in range(2, 10):
                dcba = e * abcd
                if f'{dcba}'[::-1] == f'{abcd}':    # Checks that ABC = BCA
                    solutions['Solutions'].append((abcd, dcba, e))
    stop = perf_counter()
    elapsed_time = stop - start
    return solutions, elapsed_time


if __name__ == '__main__':
    times = []
    print('THREE DIGITS')
    # 102: Biggest unique number with 3 digits. 498: Biggest unique number X s.t. for all E >= 2, E*X is a 3 digit number (2*498 = 996)
    # All 3 digit numbers greater that 987 are not unique
    solutions, elapsed_time = find_palindromes(102, 498, 987)
    times.append(elapsed_time)
    print(solutions, f'elapsed_time: {elapsed_time}')

    print('FOUR DIGITS (ORIGINAL)')
    # 1023: Biggest unique number with 4 digits. 4987: Biggest unique number X s.t. for all E >= 2, E*X is a four digit number (2*4987 = 9974)
    # All 4 digit numbers greater that 9876 are not unique
    solutions, elapsed_time = find_palindromes(1023, 4987, 9876)
    times.append(elapsed_time)
    print(solutions, f'elapsed_time: {elapsed_time}')

    print('FIVE DIGITS')
    # 10234: Biggest unique number with 5 digits. 49876: Biggest unique number X s.t. for all E >= 2, E*X is a 5 digit number (2*49876 = 99752)
    # All 5 digit numbers greater that 98765 are not unique
    solutions, elapsed_time = find_palindromes(10234, 49876, 98765)
    times.append(elapsed_time)
    print(solutions, f'elapsed_time: {elapsed_time}')

    print('SIX DIGITS')
    solutions, elapsed_time = find_palindromes(102345, 498765, 987654)
    times.append(elapsed_time)
    print(solutions, f'elapsed_time: {elapsed_time}')

    print('SEVEN DIGITS')
    solutions, elapsed_time = find_palindromes(1023456, 4987654, 9876543)
    times.append(elapsed_time)
    print(solutions, f'elapsed_time: {elapsed_time}')

    print('EIGHT DIGITS')
    solutions, elapsed_time = find_palindromes(10234567, 49876543, 98765432)
    times.append(elapsed_time)
    print(solutions, f'elapsed_time: {elapsed_time}')

    # The time factor per step is calculated by:
    for index, time in enumerate(times[1:], start=0):
        print(time/times[index])
