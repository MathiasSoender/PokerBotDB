from Tree.data2 import Data
import math
import random
from Tree.Identifier import Identifier
import copy


class Node:

    __slots__ = 'children', 'identifier', 'data'

    def __init__(self, identifier: Identifier, data: Data, parent=None):
        self.children = []
        self.identifier = identifier
        self.data = data

    """ Finds a rooted subtree of node """

    def subtree(self):
        from Tree.Tree import Tree

        new_root = copy.copy(self)

        T = Tree(new_tree=True, root=new_root)
        child_list = [new_root]


        while len(child_list) > 0:
            node = child_list.pop()
            for c in node.children:
                child_list.append(c)
            T.nodes[node.identifier.name] = node

        return T

    def find_distribution(self, win_probability, thresh=150):

        def find_denom(n, c=0.998):
            return (c ** n - 1) / (c - 1)

        softmax_sum = 0
        softmax_distribution = []

        for child in self.children:
            child_split = child.data.find_split(win_probability)
            if child.data.N[child_split] > thresh:
                beta = 1
            else:
                beta = child.data.N[child_split] / thresh

            if child.data.fold_node:
                softmax_sum += math.exp(child.data.c_reward[child_split] * beta)

            else:

                if child.data.N[child_split] != 0:
                    softmax_sum += math.exp((child.data.c_reward[child_split] /
                                             find_denom(child.data.N[child_split])) * beta)
                else:
                    softmax_sum += 1

        for child in self.children:
            child_split = child.data.find_split(win_probability)
            if child.data.N[child_split] > thresh:
                beta = 1
            else:
                beta = child.data.N[child_split] / thresh

            if child.data.fold_node:
                softmax_distribution.append((child,
                                             math.exp(child.data.c_reward[child_split] * beta) /
                                             softmax_sum))
            else:
                if child.data.N[child_split] == 0:
                    softmax_distribution.append((child, 1 / softmax_sum))

                else:

                    softmax_distribution.append((child, math.exp((child.data.c_reward[child_split] /
                                                 find_denom(child.data.N[child_split])) * beta) / softmax_sum))

        return softmax_distribution

    def select_child(self, win_probability, greedy=True, LOG=None, prob=25):
        # Zips the distribution into: Children, distribution values
        dis = self.find_distribution(win_probability)
        Children, distribution = zip(*dis)

        # Some probability of being epsilon-greedy:
        if greedy and random.randint(0, prob) == 1:
            child = random.choice(Children)

            if LOG is not None:
                LOG.log("E-greedy child selection")

            return child, 1 / len(Children)

        # Otherwise use the soft-max distribution
        if LOG is not None:
            LOG.children_log(dis)
        child = random.choices(population=Children, weights=distribution, k=1)[0]

        return child, distribution[Children.index(child)]

    def is_leaf(self):
        if len(self.children) == 0:
            return True
        else:
            return False

    def add_child(self, new_node):
        self.children.append(new_node)

    def local_node(self):
        children = []
        for c in self.children:
            children.append(copy.copy(c))

        new_node = copy.copy(self)
        new_node.children = children
        for c in new_node.children:
            c.children = []

        return new_node

    def __str__(self):
        return str((self.identifier.name, self.data.__str__()))
