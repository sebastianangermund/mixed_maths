from collatz import Collatz

c = Collatz()

n = 177
while True:
    print(n)
    n = c.collatz_step_compact(n)
    if n == 1:
        print(n)
        break
