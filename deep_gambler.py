from action import *
#from tensorflow.python.keras.layers import Input, Dense
#from keras.models import Sequential
import random
import numpy as np
import tensorflow as tf

class DeepGambler:
    def __init__ (self, learning_rate = 0.1, discount = 0.9, exploration_rate = 1.0, iterations = 10000):
        self.learning_rate = learning_rate
        self.discount = discount
        self.exploration_rate = 1.0
        self.exploration_delta = 1.0 / iterations

        self.input_count = 5 # Each representing the state/position of the agent in the dungeon
        self.output_count = 2 # Left or right

	#self.model = Sequential()
        self.session = tf.Session()
        self.define_model()
        self.session.run(self.initializer)

    def define_model(self):
        #self.model.add(Dense(16, 'sigmoid', kernel_initializer = tf.constant_initializer(np.zeros((self.input_count, 16)))))
	#self.model.add(Dense(16, 'sigmoid', kernel_initializer = tf.constant_initializer(16, np.zeros((self.output_count)))))
        #self.model.compile(loss, self.optimizer)

        self.model_input = tf.placeholder(dtype = tf.float32, shape = [None, self.input_count])

        ##        
        # Hidden layers
        ##
        # 16 neurons with sigmoid activation
        fc1 = tf.layers.dense(self.model_input, 16, activation = tf.sigmoid, kernel_initializer = tf.constant_initializer(np.zeros((self.input_count, 16))))
        fc2 = tf.layers.dense(fc1, 16, activation = tf.sigmoid, kernel_initializer = tf.constant_initializer(np.zeros((16, self.output_count))))

        self.model_output = tf.layers.dense(fc2, self.output_count)

        self.target_output = tf.placeholder(dtype = tf.float32, shape = [None, self.output_count])

        loss = tf.losses.mean_squared_error(self.target_output, self.model_output)

        self.optimizer = tf.train.GradientDescentOptimizer(learning_rate = self.learning_rate).minimize(loss)

        self.initializer = tf.global_variables_initializer()

    def get_Q(self, state):
        return self.session.run(self.model_output, feed_dict = { self.model_input: self.to_one_hot(state) })[0]
    
    def to_one_hot(self, current_state):
        one_hot = np.zeros((1,self.input_count))
        one_hot[0, [current_state]] = 1
        print(f"One hot:: {one_hot.shape}")
        return one_hot

    def get_next_action(self, state):
        if random.random() > self.exploration_rate:
            return self.greedy_action(state)
        else:
            return self.random_action()

    def greedy_action(self, state):
        return np.argmax(self.get_Q(state))

    def random_action(self):
        return FORWARD if random.random() < 0.5 else BACKWARD

    def train(self, old_state, action, reward, new_state):
        old_state_Q_values = self.get_Q(old_state)
        new_state_Q_values = self.get_Q(new_state)
        old_state_Q_values[action] = reward + self.discount * np.amax(new_state_Q_values)

        training_input = self.to_one_hot(old_state)
        target_output = [old_state_Q_values]
        training_data = { self.model_input: training_input, self.target_output: target_output }

        self.session.run(self.optimizer, feed_dict = training_data)

    def update(self, old_state, new_state, action, reward):
        self.train(old_state, action, reward, new_state)

        if self.exploration_rate > 0:
            self.exploration_rate -= self.exploration_delta
