class Collatz:
    def __init__(self):
        self.cache = {1: 0}
        self.hit_list = []
        self.hit_list_progression = []

    @staticmethod
    def collatz_step(n):
        if n % 2 == 0:
            return int(n / 2)
        else:
            return 3*n + 1

    def run_collatz(self, n):
        return_value = self.collatz_step(n)
        if return_value in self.cache.keys():
            self.cache[return_value] += 1
            return
        else:
            self.hit_list.append(return_value)
            return self.run_collatz(return_value)

    def iterate_collatz(self, loop_to):
        for i in range(1, loop_to+1):
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


class CollatzNumbers:
    def __init__(self, multiplier, constant, parent):
        self.multiplier = multiplier
        self.constant = constant
        self.parent = parent
        self.child_even = None
        self.child_odd = None

    def __str__(self):
        return f'{self.multiplier}n + {self.constant}'

    def _get_child_ab(self, a, b, even):
        if even:
            return (a//2, b//2)
        else:
            return (3*a, 3*b + 1)

    def get_children(self):
        if self.child_even or self.child_odd:
            return self.child_even, self.child_odd
        multiplier_even = self.multiplier % 2 == 0
        constant_even = self.constant % 2 == 0
        if multiplier_even and constant_even:
            child_ab = self._get_child_ab(a=self.multiplier, b=self.constant, even=True)
            child_even = CollatzNumbers(child_ab[0], child_ab[1], self)
            self.child_even = child_even
            return child_even, None
        elif multiplier_even and (not constant_even):
            child_ab = self._get_child_ab(a=self.multiplier, b=self.constant, even=False)
            child_odd = CollatzNumbers(child_ab[0], child_ab[1], self)
            self.child_odd = child_odd
            return None, child_odd
        elif (not multiplier_even) and constant_even:
            child_even_ab = self._get_child_ab(a=2*self.multiplier, b=self.constant, even=True)
            child_odd_ab = self._get_child_ab(a=2*self.multiplier, b=self.constant+self.multiplier, even=False)
            child_even = CollatzNumbers(child_even_ab[0], child_even_ab[1], self)
            child_odd = CollatzNumbers(child_odd_ab[0], child_odd_ab[1], self)
            self.child_even = child_even
            self.child_odd = child_odd
            return child_even, child_odd
        elif (not multiplier_even) and (not constant_even):
            child_even_ab = self._get_child_ab(a=2*self.multiplier, b=self.constant+self.multiplier, even=True)
            child_odd_ab = self._get_child_ab(a=2*self.multiplier, b=self.constant, even=False)
            child_even = CollatzNumbers(child_even_ab[0], child_even_ab[1], self)
            child_odd = CollatzNumbers(child_odd_ab[0], child_odd_ab[1], self)
            self.child_even = child_even
            self.child_odd = child_odd
            return child_even, child_odd