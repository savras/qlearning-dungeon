from enums import *
import random

class Dunkard:
    def __init__(self):
        self.q_table = None

    def get_next_action(self, state):
        return FORWARD if random.random() < 0.5 else BACKWARD

    def update(self, old_position, new_position, action, reward):
        pass # I'm drunk
