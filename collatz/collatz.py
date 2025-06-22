from math import gcd

from anytree import NodeMixin


# --- DEBUG switch: make S(6,1) loop back to itself after one step ---
DEBUG_SELF_LOOP = False
SELF_A, SELF_B = 6, 1           # arbitrary odd a, even b works well
# --- DEBUG switch end ---
FIRST = {}      # (a,b) ➜ (depth, alpha, beta, node)
SEEN = set()    # (a,b,depth)


def should_expand(node):
    key = (node.multiplier, node.constant, node.depth)
    if key in SEEN:
        return False
    SEEN.add(key)
    return True


class CollatzNumbers(NodeMixin):
    parent_parity_mapping = {
        'EVEN': 'e',
        'ODD': 'o'
    }
    index_transforms = {
        'T1': (2, 0),
        'T2': (2, 1)
    }

    def __init__(self, parent, multiplier, constant, parent_parity, index_map=(1,0), word=''):
        super(CollatzNumbers, self).__init__()
        self.parent = parent
        self.multiplier = multiplier
        self.constant = constant
        self.parent_parity = parent_parity
        self.index_map = index_map
        self.word = word
        self.name = self.__str__()
        self._register_and_check()

    def __str__(self):
        # self string used in anytree rendering
        return f'S({self.multiplier},{self.constant}) {self.parent_parity}\ni={self.index_map[0]}j + {self.index_map[1]}\n{self.word}'

    def _get_child_ab(self, a, b, even):
        if even:
            return (a//2, b//2)
        else:

            # >>> DEBUG: force a self-loop on S(6,1)
            if DEBUG_SELF_LOOP and a == SELF_A and b == SELF_B:
                return (a, b)   # immediate duplicate
            # >>> END DEBUG

            # ai + b => 3(ai + b) + 1 = (3a)i + (3b + 1)
            new_a = 3*a
            new_b = 3*b + 1
            # return (new_a, new_b)
            # we know ai + b odd, so we can represent (ai + b) as (2n + 1)
            # Collatz step gives 3(2n + 1) + 1 = 6n + 3 + 1 = 2(3n + 2) which is even
            # so we might as well do the next step at once
            return self._get_child_ab(a=new_a, b=new_b, even=True)

    def _register_and_check(self):
        key = (self.multiplier, self.constant)
        if key not in FIRST:
            FIRST[key] = (self.depth, *self.index_map, self)
            return  True
        # second hit ➜ potential cycle
        k  = self.depth
        k0, alpha0, beta0, node0 = FIRST[key]
        alpha1, beta1 = self.index_map
        #  CRT test
        from math import gcd
        mod = 2**k
        if (beta1 - beta0) % gcd(mod, mod) == 0 and (beta1 - self.constant) % gcd(mod, self.multiplier) == 0:
            print("** REAL CYCLE CANDIDATE **", f"depth {k}, {str(self).replace('\n', ' ')}")
        return False

    def generate_children(self):
        if self.multiplier == 1 and self.constant == 0 and self.depth>0:
            return  # to not expand the root node further
        if not should_expand(self):
            return
        if self.children:
            return self.children

        multiplier_even = self.multiplier % 2 == 0
        constant_even = self.constant % 2 == 0
        child_even_index_transform = None
        child_odd_index_transform = None
        transform = False

        if multiplier_even and constant_even:
            child_even_ab = self._get_child_ab(a=self.multiplier, b=self.constant, even=True)
            child_odd_ab = None
        elif multiplier_even and (not constant_even):
            child_even_ab = None
            child_odd_ab = self._get_child_ab(a=self.multiplier, b=self.constant, even=False)
        elif (not multiplier_even) and constant_even:
            transform = True
            child_even_index_transform = 'T1'
            child_odd_index_transform = 'T2'
        elif (not multiplier_even) and (not constant_even):
            transform = True
            child_even_index_transform = 'T2'
            child_odd_index_transform = 'T1'
        else:
            raise ValueError("Unexpected case: both multiplier and constant are odd.")

        if transform:
            child_even_ab = self._get_child_ab(a=self.index_transforms[child_even_index_transform][0]*self.multiplier,
                                            b=self.constant + self.index_transforms[child_even_index_transform][1]*self.multiplier,
                                            even=True)
            child_odd_ab  = self._get_child_ab(a=self.index_transforms[child_odd_index_transform][0]*self.multiplier,
                                            b=self.constant + self.index_transforms[child_odd_index_transform][1]*self.multiplier,
                                            even=False)

        self._get_babies(child_even_ab, child_even_index_transform, child_odd_ab, child_odd_index_transform, transform)

    def _get_babies(self, child_even_ab, child_even_index_transform, child_odd_ab, child_odd_index_transform, transform):
        babies = []
        if child_even_ab:
            if child_even_index_transform:
                index_map = (self.index_map[0]*self.index_transforms[child_even_index_transform][0],
                             self.index_map[0]*self.index_transforms[child_even_index_transform][1] + self.index_map[1])
            else:
                index_map = self.index_map  # use parents map (no transformation)
            child_word = self.word + child_even_index_transform if transform else self.word
            child_even = CollatzNumbers(self, child_even_ab[0], child_even_ab[1], self.parent_parity_mapping['EVEN'], index_map, child_word)
            babies.append(child_even)
        if child_odd_ab:
            if child_odd_index_transform:
                index_map = (self.index_map[0]*self.index_transforms[child_odd_index_transform][0],
                             self.index_map[0]*self.index_transforms[child_odd_index_transform][1] + self.index_map[1])
            else:
                index_map = self.index_map  # use parents map (no transformation)
            child_word = self.word + child_odd_index_transform if transform else self.word
            child_odd = CollatzNumbers(self, child_odd_ab[0], child_odd_ab[1], self.parent_parity_mapping['ODD'], index_map, child_word)
            babies.append(child_odd)
        self.children = babies
