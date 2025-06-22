from math import gcd

from anytree import NodeMixin


FIRST = {}          # (a,b) ➜ (depth, alpha, beta, node)
SEEN = set()          # (a,b,depth)

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

    def __init__(self, multiplier, constant, parent, parent_parity, index_map=(1,0)):
        super(CollatzNumbers, self).__init__()
        self.multiplier = multiplier
        self.constant = constant
        self.parent = parent
        self.parent_parity = parent_parity
        self.index_map = index_map
        self.name = self.__str__()
        self._register_and_check()

    def __str__(self):
        return f'S({self.multiplier},{self.constant}) {self.parent_parity}\ni={self.index_map[0]}j + {self.index_map[1]}'

    def _get_child_ab(self, a, b, even):
        if even:
            return (a//2, b//2)
        else:
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
        #  ---- CRT test (uses only betas) ----
        from math import gcd
        mod = 2**k
        if (beta1 - beta0) % gcd(mod, mod) == 0 and (beta1 - self.constant) % gcd(mod, self.multiplier) == 0:
            print("** REAL CYCLE CANDIDATE **", f"depth {k}, {str(self)}")
        return False

    def generate_children(self):
        if self.multiplier == 1 and self.constant == 0 and self.depth>0: return
        if not should_expand(self):
            return
        if self.children:
            return self.children
        multiplier_even = self.multiplier % 2 == 0
        constant_even = self.constant % 2 == 0
        child_even_index_transform = None
        child_odd_index_transform = None
        if multiplier_even and constant_even:
            child_even_ab = self._get_child_ab(a=self.multiplier, b=self.constant, even=True)
            child_odd_ab = None
        elif multiplier_even and (not constant_even):
            child_even_ab = None
            child_odd_ab = self._get_child_ab(a=self.multiplier, b=self.constant, even=False)
        if (not multiplier_even) and constant_even:
            child_even_ab = self._get_child_ab(a=2*self.multiplier, b=self.constant, even=True)
            child_even_index_transform = self.index_transforms['T1']
            child_odd_ab = self._get_child_ab(a=2*self.multiplier, b=self.constant+self.multiplier, even=False)
            child_odd_index_transform = self.index_transforms['T2']
        elif (not multiplier_even) and (not constant_even):
            child_even_ab = self._get_child_ab(a=2*self.multiplier, b=self.constant+self.multiplier, even=True)
            child_even_index_transform = self.index_transforms['T2']
            child_odd_ab = self._get_child_ab(a=2*self.multiplier, b=self.constant, even=False)
            child_odd_index_transform = self.index_transforms['T1']
        self._get_babies(child_even_ab, child_even_index_transform, child_odd_ab, child_odd_index_transform)

    def _get_babies(self, child_even_ab, child_even_index_transform, child_odd_ab, child_odd_index_transform):
        babies = []
        if child_even_ab:
            # if child_even_ab in SEEN:
            #     print(f'CACHE HIT: {child_even_ab}, parent: {str(self)}')
            # else:
            if child_even_index_transform:
                index_map = (self.index_map[0]*child_even_index_transform[0],
                             self.index_map[0]*child_even_index_transform[1] + self.index_map[1])
            else:
                index_map = self.index_map  # use parents (no transformation)
            child_even = CollatzNumbers(child_even_ab[0], child_even_ab[1], self, self.parent_parity_mapping['EVEN'], index_map)
            babies.append(child_even)
        if child_odd_ab:
            # if child_odd_ab in SEEN:
            #     print(f'CACHE HIT: {child_odd_ab}, parent: {str(self)}')
            # else:
            if child_odd_index_transform:
                index_map = (self.index_map[0]*child_odd_index_transform[0],
                             self.index_map[0]*child_odd_index_transform[1] + self.index_map[1])
            else:
                index_map = self.index_map  # use parents (no transformation)
            child_odd = CollatzNumbers(child_odd_ab[0], child_odd_ab[1], self, self.parent_parity_mapping['ODD'], index_map)
            babies.append(child_odd)
        self.children = babies


def run_collatz_general(graph_depth, root):
    """Run the entire Collatz generation."""
    parents = [root]
    for i in range(graph_depth):
        children = []
        for parent in parents:
            parent.generate_children()
            for baby in parent.children:
                if baby.keep:
                    children.append(baby)
        if not children:
            print('HUH')
            break
        parents = children
    return root


if __name__ == "__main__":
    graph_depth = 22    # Do not use big values (> 6) when generating visualizations for the entire Collatz tree
    root_sequence = (1, 0)
    root_parent = None
    root = CollatzNumbers(root_sequence[0], root_sequence[1], root_parent, 'ROOT')
    tree = run_collatz_general(graph_depth, root)

    def generate_odd_even_children(self):
        if self.children:
            return self.children
        multiplier_even = self.multiplier % 2 == 0
        constant_even = self.constant % 2 == 0
        child_even_index_transform = None
        child_odd_index_transform = None
        child_odd_ab = None
        child_even_ab = None
        if (not multiplier_even) and constant_even:
            child_odd_ab = self._get_child_ab(a=2*self.multiplier, b=self.constant+self.multiplier, even=False)
            child_odd_index_transform = self.index_transforms['T2']
        self._get_babies(child_even_ab, child_even_index_transform, child_odd_ab, child_odd_index_transform)
