import numpy as np

from anytree import NodeMixin



def check_loop_case_1(b_1, beta_1, ancestor):
    b_2 = ancestor.constant
    beta_2 = ancestor.index_map[1]
    if b_1 == b_2 and beta_1 == beta_2:
        if b_1 == 1 or b_1 == 2:    # node value 1 or 2 is a collatz end cycle
            # print("End cycle detected at ", str(ancestor).replace("\n", " "))
            return False    # we don't care about end cycles
        print("!! Cycle detected at ", str(ancestor).replace("\n", " "))
        return True
    return False


def check_loop_case_2(a_1, b_1, alpha_1, beta_1, ancestor):
    if ancestor.parent is None:
        return False
 
    a_2 = ancestor.multiplier
    alpha_2 = ancestor.index_map[0]

    denominator = a_1 * alpha_2 - a_2 * alpha_1
    if denominator == 0:
        print("## Zero denominator found")
        return False

    b_2 = ancestor.constant
    beta_2 = ancestor.index_map[1]

    x_numerator = a_2 * (beta_1 - beta_2) + alpha_2 * (b_2 - b_1)
    if x_numerator == 0:
        return check_loop_case_1(b_1, beta_1, ancestor)
    if x_numerator % denominator != 0:
        return False

    y_numerator = a_1 * (beta_1 - beta_2) + alpha_1 * (b_2 - b_1)
    if y_numerator % denominator != 0:
        return False

    if np.sign(denominator) == np.sign(x_numerator) and np.sign(denominator) == np.sign(y_numerator):
        # x and y are integers > 0, so we have a cycle
        return True

    return False


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
        self.parent = parent    # for ancestor+depth tracking done by anytree
        self.multiplier = multiplier
        self.constant = constant
        self.parent_parity = parent_parity
        self.index_map = index_map
        self.word = word
        self.cycle_detected, self.terminate_branch = self._register_and_check_cycle()
        self.name = self.__str__()

    def __str__(self):
        # self string used in anytree rendering
        return f'S({self.multiplier},{self.constant}) {self.parent_parity}\ni={self.index_map[0]}j + {self.index_map[1]}\n{self.word}'

    def _get_child_ab(self, a, b, even):
        if even:
            return (a//2, b//2)
        else:
            # ai + b -> 3(ai + b) + 1 = (3a)i + (3b + 1)
            new_a = 3*a
            new_b = 3*b + 1
            # return (new_a, new_b)
            # we know ai + b odd, so we can represent (ai + b) as (2n + 1)
            # Collatz step gives 3(2n + 1) + 1 = 6n + 3 + 1 = 2(3n + 2) which is even
            # so we might as well do the next step at once
            return self._get_child_ab(a=new_a, b=new_b, even=True)

    def _register_and_check_cycle(self):
        """ Attempth to find a cycle in the Collatz tree.

        Let current node be S(a_1,b_1) with index map alpha_1, beta_1 and depth d_1.
        Search in ancestors for a node S(a_2,b_2) with index map alpha_2, beta_2 and depth d_2
        such that:

        Case 1 (special case of Case 2):
        b_1 = b_2 := b and beta_1 = beta_2 := beta
        - Why is this a cycle?
            We can then set node index = 0 which results in same node value b and same seed value beta -> cycle

        Case 2 (general case):
        There exists x,y such that a_1*x + b_1 = a_2*y + b_2 and alpha_1*x + beta_1 = alpha_2*y + beta_2
        Solve for x and y:
            x = a_2(beta_1 - beta_2) + alfa_2(b_2 - b_1) / a_1*alpha_2 - a_2*alpha_1
            y = a_1(beta_1 - beta_2) + alpha_1(b_2 - b_1) / a_1*alpha_2 - a_2*alpha_1
        If x and y are integers, then we have a cycle.
        - Why is this a cycle?
            This means that the same node value in two related nodes are reached from the same seed

        """
        a_1 = self.multiplier
        b_1 = self.constant

        if a_1 == 1 and b_1 == 0:
            # root node, trivial cycle
            cycle_detected = True
            terminate_branch = True
            return cycle_detected, terminate_branch

        alpha_1 = self.index_map[0]
        beta_1 = self.index_map[1]

        terminate_branch = False

        for ancestor in self.ancestors:
            # Run special case
            # cycle_detected = check_loop_case_1(a_1, b_1, self)
            # Run general case
            cycle_detected = check_loop_case_2(a_1, b_1, alpha_1, beta_1, ancestor)
            if cycle_detected:
                print("!! Cycle detected: ", str(ancestor).replace("\n", " "), " -> ", str(self).replace("\n", " "))
                return cycle_detected, terminate_branch

        return cycle_detected, terminate_branch

    def generate_children(self):
        if self.children:
            return self.children

        multiplier_even = self.multiplier % 2 == 0
        constant_even = self.constant % 2 == 0
        child_even_index_transform = None
        child_odd_index_transform = None
        transform = False

        if multiplier_even and constant_even:
            print("This never happens")
            child_even_ab = self._get_child_ab(a=self.multiplier, b=self.constant, even=True)
            child_odd_ab = None
        elif multiplier_even and (not constant_even):
            print("This never happens")
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

        self._set_children(child_even_ab, child_even_index_transform, child_odd_ab, child_odd_index_transform, transform)

    def _set_children(self, child_even_ab, child_even_index_transform, child_odd_ab, child_odd_index_transform, transform):
        children = []
        if child_even_ab:
            if transform:
                index_map = (self.index_map[0]*self.index_transforms[child_even_index_transform][0],
                             self.index_map[0]*self.index_transforms[child_even_index_transform][1] + self.index_map[1])
                child_word = self.word + child_even_index_transform
            else:
                print("This never happens")
                index_map = self.index_map  # use parents map (no transformation)
                child_word = self.word
            child_even = CollatzNumbers(self, child_even_ab[0], child_even_ab[1], self.parent_parity_mapping['EVEN'], index_map, child_word)

            if not child_even.terminate_branch:
                children.append(child_even)

        if child_odd_ab:
            if child_odd_index_transform:
                index_map = (self.index_map[0]*self.index_transforms[child_odd_index_transform][0],
                             self.index_map[0]*self.index_transforms[child_odd_index_transform][1] + self.index_map[1])
                child_word = self.word + child_odd_index_transform
            else:
                print("This never happens")
                index_map = self.index_map  # use parents map (no transformation)
                clild_word = self.word
            child_odd = CollatzNumbers(self, child_odd_ab[0], child_odd_ab[1], self.parent_parity_mapping['ODD'], index_map, child_word)

            if not child_odd.terminate_branch:
                children.append(child_odd)

        self.children = children
