from action import *
import random

class Gambler:
    def __init__(self, learning_rate = 0.1, discount = 0.95, exploration_rate = 1.0, iterations = 1000):
        self.q_table = [[0,0,0,0,0], [0,0,0,0,0]]
        self.learning_rate = learning_rate
        self.discount = discount
        self.exploration_rate = exploration_rate
        self.exploration_delta = 1.0 / iterations

    def get_next_action(self, position):
        if random.random() > self.exploration_rate:
            return FORWARD
        else:
            return self.random_action()

    def greedy_action(self, position):
        if self.q_table[FORWARD][position] > self.q_table[BACKWARD][position]:
            return FORWARD
        elif self.q_table[BACKWARD][position] > self.q_table[FORWARD][position]:
            return BACKWARD
        else:
            return FORWARD if random.random() < 0.5 else BACKWARD

    def random_action(self):
        return FORWARD if random.random() < 0.5 else BACKWARD

    def update(self, old_position, new_position, action, reward):
        future_action = self.greedy_action(new_position)
        future_reward = self.q_table[future_action][new_position]

        old_value = self.q_table[action][old_position]
        new_value = old_value + self.learning_rate * (reward + self.discount * future_reward - old_value)
        self.q_table[action][old_position] = new_value

        if self.exploration_rate > 0:
            self.exploration_rate -= self.exploration_delta
