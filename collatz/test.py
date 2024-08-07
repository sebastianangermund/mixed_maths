# from collatz import Collatz

# c = Collatz()

# n = 177
# while True:
#     print(n)
#     n = c.collatz_step(n)
#     if n == 1:
#         print(n)
#         break


# plotting

X = [i for i in range(10)]

y = 0
Y = [y]
for _ in X:
    y = (3*y + 1)/2
    Y.append(y)

print(Y)