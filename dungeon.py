from action import *
import random

class Dungeon:
    def __init__(self, length = 5, inverse = 0.1, backward_payout = 2, forward_payout = 10):
        self.length = length
        self.inverse = inverse
        self.backward_payout =  backward_payout
        self.forward_payout = forward_payout
        self.current_position = 0

    # Determine if the action takes the agent backward or forward depending on whether
    # the dungeon is inverted. A forward action will take the agen backwards if the dungeon is inverted.
    def take_action(self, action):
        if random.random() < self.inverse:
            action = not action
        if action == BACKWARD:
            reward = self.backward_payout
            self.current_position = 0
        elif action == FORWARD:
            # If the agent hasn't reached the end of the dungeon, move the agent forward.
            if self.current_position < self.length - 1:
                self.current_position += 1
                reward = 0 # There is no reward for moving forward unless its reaches the end of the dungeon.
            else:
               # Give forward payout
               reward = self.forward_payout
        return self.current_position, reward

    def reset(self):
        self.current_position = 0
        return self.current_position
