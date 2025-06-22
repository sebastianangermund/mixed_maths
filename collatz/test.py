
class Collatz:
    def __init__(self):
        self.cache = {1: 0}
        self.hit_list = []
        self.hit_list_progression = []

    @staticmethod
    def collatz_step(n):
        if n % 2 == 0:
            return n // 2
        else:
            return 3*n + 1

    @staticmethod
    def collatz_step_compact(n):
        if n % 2 == 0:
            print('Even step:', n // 2)
            return n // 2
        else:
            print('Odd step:', (3*n + 1) // 2)
            return (3*n + 1) // 2

    def run_collatz(self, n):
        return_value = self.collatz_step(n)
        if return_value in self.cache.keys():
            self.cache[return_value] += 1
            return
        else:
            self.hit_list.append(return_value)
            return self.run_collatz(return_value)

    def iterate_collatz(self, loop_to, loop_from=1):
        for i in range(loop_from, loop_to+1):
            self.hit_list_progression.append(len(self.hit_list))
            if i in self.cache.keys():
                self.cache[i] += 1
                continue
            else:
                self.hit_list.append(i)
            self.run_collatz(i)
            # print(i, self.hit_list)
            for el in self.hit_list:
                self.cache[el] = 1


if __name__ == "__main__":
    c = Collatz()

    n = 255
    while True:
        print(n)
        n = c.collatz_step_compact(n)
        if n == 1:
            print(n)
            break
