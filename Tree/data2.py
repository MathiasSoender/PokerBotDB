import math
import random


class Data:
    __slots__ = 'N', 'split_probabilities', 'all_probabilities', 'c_reward', 'fold_node', 'total_splits'

    def __init__(self, pre_flop=False, fold_node=False, total_splits = 5):
        self.N = []
        self.split_probabilities = []
        self.all_probabilities = []
        self.c_reward = []

        self.fold_node = False
        self.total_splits = total_splits

        if fold_node:
            splits = [0]
            self.fold_node = True

        else:
            splits = list(range(0, self.total_splits))




        for split in splits:
            self.c_reward.append(0)
            self.N.append(0)
            if fold_node:
                self.split_probabilities.append(0)
                self.all_probabilities.append(0)
            else:
                if split != 0:
                    self.split_probabilities.append(1 / max(splits) * split)
                self.all_probabilities.append(1 / max(splits) * split)

    def __str__(self):

        return str(["Rewards: " + str(self.c_reward), "N: " + str(self.N),
                    "Split probabilities: " + str(self.split_probabilities)])

    def find_split(self, probability):
        if self.fold_node:
            return 0
        else:
            splits = list(range(0, self.total_splits-1))

        assigned_split = 0
        for split in reversed(splits):
            if self.split_probabilities[split] < probability:
                assigned_split = split + 1
                break
        return assigned_split

    def update_split(self, probability):
        if self.fold_node:
            threshold = 1
            splits = [0]
        else:
            threshold = 200
            splits = list(range(0, self.total_splits))


        if len(self.all_probabilities) > threshold:
            _ = self.all_probabilities.pop(random.randrange(len(self.all_probabilities)))

        else:
            self.all_probabilities.append(probability)

        parition_N = math.floor(len(self.all_probabilities) / len(splits))
        self.all_probabilities = sorted(self.all_probabilities)

        for split in list(range(0, self.total_splits - 1)):
            self.split_probabilities[split] = self.all_probabilities[split * parition_N: (split + 1) * parition_N][-1]

    def update_N(self, chosen_split):
        self.N[chosen_split] += 1

    def update(self, chosen_probability, reward):
        # Round to save space
        reward = round(reward, 2)
        chosen_probability = round(chosen_probability, 5)
        chosen_split = self.find_split(chosen_probability)
        self.update_reward(chosen_split, reward)
        self.update_N(chosen_split)

        if not self.fold_node:
            self.update_split(chosen_probability)

    def update_reward(self, chosen_split, reward):

        if self.fold_node:
            self.c_reward[chosen_split] = reward
        else:
            self.c_reward[chosen_split] = self.c_reward[chosen_split] * 0.998 + reward
