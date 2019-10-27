from action import *
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical
import random
import numpy as np
import tensorflow as tf
import tensorflow.keras as keras

class DeepGambler:
    def __init__ (self, learning_rate = 0.1, discount = 0.9, exploration_rate = 1.0, iterations = 10000):
        self.learning_rate = learning_rate
        self.discount = discount
        self.exploration_rate = 1.0
        self.exploration_delta = 1.0 / iterations

        self.input_count = 5 # Each representing the state/position of the agent in the dungeon
        self.output_count = 2 # Left or right

        self.define_model()

    # Defines the Keras model.
    def define_model(self):
        self.model = Sequential()
        self.model.add(Dense(16, activation="sigmoid", input_shape=(5, ))) # Takes a 2D array with indexer ranging from 0 to 4.
        self.model.add(Dense(16, activation="sigmoid"))
        self.model.add(Dense(2))
        self.model.compile(loss="binary_crossentropy", optimizer="rmsprop", metrics=["accuracy"]) 

    # Gets the prediction which is a 1 x 2 array. E.g. [[0.23423 0.345434]]
    def get_Q(self, state):
        one_hot = self.to_one_hot(state)
        to_categorical(one_hot)
        # result is a 1 x 2 array, signifying [Backward, Forward] q-values
        # print(f"one_hot:: {one_hot}") 
        # print(f"shape:: {one_hot.shape}")        

        result = self.model.predict(one_hot)
        #print(f"result:: {result}")
        return result

    # Creates a 2D array of 1 x 5 elements. E.g. [[0 0 0 0 0]]
    def to_one_hot(self, current_state):
        one_hot = np.zeros((1, self.input_count))

        one_hot[0, current_state] = 1
        return one_hot

    # Pick either a random action or an action with the greatest reward
    def get_next_action(self, state):
        if random.random() > self.exploration_rate:
            return self.greedy_action(state)
        else:
            return self.random_action()

    # Returns the index of the action with the greatest reward
    def greedy_action(self, state):
        # BACKWARD == 1, FORWARD == 0
        return np.argmax(self.get_Q(state))

    def random_action(self):
        return FORWARD if random.random() < 0.5 else BACKWARD

    def train(self, old_position, action, reward, new_position):
        old_position_Q_values = self.get_Q(old_position)
        new_position_Q_values = self.get_Q(new_position)

        # print(f"old_position:: {old_position_Q_values}")
        # print(f"new_position:: {new_position_Q_values}")
        # print(f"action:: {action}")
        old_position_Q_values[0, [action]] = reward + self.discount * np.amax(new_position_Q_values)

        training_input = self.to_one_hot(old_position)
        target_output = old_position_Q_values

        # print(f"training_input:: training_input")
        # print(f"shape:: training_input.shape")        
        self.model.fit(training_input, target_output, batch_size=32, epochs=10, verbose=0)

    def update(self, old_state, new_state, action, reward):
        self.train(old_state, action, reward, new_state)

        if self.exploration_rate > 0:
            self.exploration_rate -= self.exploration_delta
