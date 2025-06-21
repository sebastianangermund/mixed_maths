from anytree import NodeMixin


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
            return n // 2
        else:
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


class CollatzNumbers(NodeMixin):
    cache = []
    parent_handed_mapping = {
        'ROOT': 'root',
        'EVEN': 'e',
        'ODD': 'o'
    }
    root_transforms = {
        'EVEN': (2, 0),
        'ODD': (2, 1)
    }

    def __init__(self, multiplier, constant, parent, parent_handed, root_transform=(1,0)):
        super(CollatzNumbers, self).__init__()
        if self.init_check(multiplier, constant):
            return None
        self.multiplier = multiplier
        self.constant = constant
        self.parent = parent
        self.parent_handed = parent_handed
        self.root_transform = root_transform
        self.name = self.__str__()

    @classmethod
    def init_check(cls, a, b):
        if (a, b) in cls.cache:
            print(f'CACHE HIT: {(a, b)}')
            return True
        cls.cache.append((a, b))
        return False

    def __str__(self):
        return f'S({self.multiplier},{self.constant}) {self.parent_handed}\ni={self.root_transform[0]}j + {self.root_transform[1]}'

    def _get_child_ab(self, a, b, even):
        if even:
            return (a//2, b//2)
        else:
            # ai + b => 3(ai + b) + 1 = (3a)i + (3b + 1)
            new_a = 3*a
            new_b = 3*b + 1
            self.cache.append((new_a, new_b))
            # return (new_a, new_b)
            # we know ai + b odd, so we can represent (ai + b) as (2n + 1)
            # Collatz step gives 3(2n + 1) + 1 = 6n + 3 + 1 = 2(3n + 2) which is even
            # so we might as well do the next step at once
            return self._get_child_ab(a=new_a, b=new_b, even=True)

    def generate_children(self):
        if self.children:
            return self.children
        multiplier_even = self.multiplier % 2 == 0
        constant_even = self.constant % 2 == 0
        child_even_rt = None
        child_odd_rt = None
        if multiplier_even and constant_even:
            child_even_ab = self._get_child_ab(a=self.multiplier, b=self.constant, even=True)
            child_odd_ab = None
        elif multiplier_even and (not constant_even):
            child_even_ab = None
            child_odd_ab = self._get_child_ab(a=self.multiplier, b=self.constant, even=False)
        if (not multiplier_even) and constant_even:
            child_even_ab = self._get_child_ab(a=2*self.multiplier, b=self.constant, even=True)
            child_even_rt = self.root_transforms['EVEN']
            child_odd_ab = self._get_child_ab(a=2*self.multiplier, b=self.constant+self.multiplier, even=False)
            child_odd_rt = self.root_transforms['ODD']
        elif (not multiplier_even) and (not constant_even):
            child_even_ab = self._get_child_ab(a=2*self.multiplier, b=self.constant+self.multiplier, even=True)
            child_even_rt = self.root_transforms['ODD']
            child_odd_ab = self._get_child_ab(a=2*self.multiplier, b=self.constant, even=False)
            child_odd_rt = self.root_transforms['EVEN']
        self._get_babies(child_even_ab, child_even_rt, child_odd_ab, child_odd_rt)

    def generate_odd_even_children(self):
        if self.children:
            return self.children
        multiplier_even = self.multiplier % 2 == 0
        constant_even = self.constant % 2 == 0
        child_even_rt = None
        child_odd_rt = None
        child_odd_ab = None
        child_even_ab = None
        if (not multiplier_even) and constant_even:
            child_odd_ab = self._get_child_ab(a=2*self.multiplier, b=self.constant+self.multiplier, even=False)
            child_odd_rt = self.root_transforms['ODD']
        self._get_babies(child_even_ab, child_even_rt, child_odd_ab, child_odd_rt)

    def _get_babies(self, child_even_ab, child_even_rt, child_odd_ab, child_odd_rt):
        babies = []
        if child_even_ab:
            if child_even_ab in self.cache:
                print(f'CACHE HIT: {child_even_ab}')
            else:
                if child_even_rt:
                    root_transform = (self.root_transform[0]*child_even_rt[0], self.root_transform[0]*child_even_rt[1] + self.root_transform[1])
                else:
                    root_transform = self.root_transform
                child_even = CollatzNumbers(child_even_ab[0], child_even_ab[1], self, self.parent_handed_mapping['EVEN'], root_transform)
                babies.append(child_even)
        if child_odd_ab:
            if child_odd_ab in self.cache:
                print(f'CACHE HIT: {child_odd_ab}')
            else:
                if child_odd_rt:
                    root_transform = (self.root_transform[0]*child_odd_rt[0], self.root_transform[0]*child_odd_rt[1] + self.root_transform[1])
                else:
                    root_transform = self.root_transform
                child_odd = CollatzNumbers(child_odd_ab[0], child_odd_ab[1], self, self.parent_handed_mapping['ODD'], root_transform)
                babies.append(child_odd)
        self.children = babies
