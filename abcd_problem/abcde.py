"""ORIGINAL PROBLEM:

ABCD * E = DCBA

Replace letters with digits and have the sum be true.
A, B, C, D and E must all be different digits.

"""

from time import perf_counter

elapsed_time = []

print('THREE DIGITS')
start = perf_counter()
for abcd in range(102, 498):  # 102: Biggest unique number with 3 digits. 498: Biggest unique number X s.t. for all E >= 2, E*X is a 3 digit number (2*498 = 996)
    dcba = 0
    while dcba <= 987: # All 3 digit numbers greater that 987 are not unique
        for e in range(2, 11):
            dcba = e * abcd
            if f'{dcba}'[::-1] == f'{abcd}':    # Checks that ABC = BCA
                print(abcd, dcba, e)
stop = perf_counter()
elapsed_time.append(stop - start)
print("Elapsed time :", stop - start)

print('FOUR DIGITS (ORIGINAL)')
start = perf_counter()
for abcd in range(1023, 4987):  # 1023: Biggest unique number with 4 digits. 4987: Biggest unique number X s.t. for all E >= 2, E*X is a four digit number (2*4987 = 9974)
    dcba = 0
    while dcba <= 9876: # All 4 digit numbers greater that 9876 are not unique
        for e in range(2, 11):
            dcba = e * abcd
            if f'{dcba}'[::-1] == f'{abcd}':    # Checks that ABCD = BCAD
                print(abcd, dcba, e)
stop = perf_counter()
elapsed_time.append(stop - start)
print("Elapsed time :", stop-start)

print('FIVE DIGITS')
start = perf_counter()
for abcd in range(10234, 49876):  # 10234: Biggest unique number with 5 digits. 49876: Biggest unique number X s.t. for all E >= 2, E*X is a 5 digit number (2*49876 = 99752)
    edcb = 0
    while edcb <= 98765: # All 5 digit numbers greater that 98765 are not unique
        for f in range(2, 11):
            edcb = f * abcd
            if f'{edcb}'[::-1] == f'{abcd}':    # Checks that ABCDE = EBCAD
                print(abcd, edcb, f)
stop = perf_counter()
elapsed_time.append(stop - start)
print("Elapsed time :", stop-start)

print('SIX DIGITS')
start = perf_counter()
for abcd in range(102345, 498765):  # 102345: Biggest unique number with 6 digits. 498765: Biggest unique number X s.t. for all E >= 2, E*X is a 6 digit number (2*498765 = 997530)
    edcb = 0
    while edcb <= 987654: # All 6 digit numbers greater that 987654 are not unique
        for f in range(2, 11):
            edcb = f * abcd
            if f'{edcb}'[::-1] == f'{abcd}':    # Checks that ABCDE = EBCAD
                print(abcd, edcb, f)
stop = perf_counter()
elapsed_time.append(stop - start)
print("Elapsed time :", stop-start)

print('SEVEN DIGITS')
start = perf_counter()
for abcd in range(1023456, 4987654):  # 1023456: Biggest unique number with 7 digits. 4987654: Biggest unique number X s.t. for all E >= 2, E*X is a 7 digit number (2*4987654 = 9975308)
    edcb = 0
    while edcb <= 9876543: # All 7 digit numbers greater that 9876543 are not unique
        for f in range(2, 11):
            edcb = f * abcd
            if f'{edcb}'[::-1] == f'{abcd}':    # Checks that ABCDE = EBCAD
                print(abcd, edcb, f)
stop = perf_counter()
elapsed_time.append(stop - start)
print("Elapsed time :", stop-start)

print('EIGHT DIGITS')
start = perf_counter()
for abcd in range(10234567, 49876543):
    edcb = 0
    while edcb <= 98765432:
        for f in range(2, 11):
            edcb = f * abcd
            if f'{edcb}'[::-1] == f'{abcd}':
                print(abcd, edcb, f)
stop = perf_counter()
elapsed_time.append(stop - start)
print("Elapsed time :", stop-start)


# The time factor per step is calculated by:
for index, time in enumerate(elapsed_time[1:], start=0):
    print(time/elapsed_time[index])
