from action import *
import random

class Accountant:
    def __init__(self):
        self.q_table = [[0,0,0,0,0,], [0,0,0,0,0,]]

    def get_next_action(self, position):
        if self.q_table[FORWARD][position] > self.q_table[BACKWARD][position]:
            return FORWARD

        elif self.q_table[BACKWARD][position] > self.q_table[FORWARD][position]:
            return BACKWARD

        return FORWARD if random.random() < 0.5 else BACKWARD

    def update(self, old_position, new_position, action, reward):
        self.q_table[action][old_position] += reward
