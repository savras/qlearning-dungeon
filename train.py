import random
import json
import argparse
import time
from drunkard import Drunkard
from dungeon import Dungeon

def main():
    parser = argparser.ArgumentParser()
    parser.add_argument('--agent', type = str, default = 'GAMBLER', help = 'Pick an agent to use. Pick from GAMBLER, ACCOUNTANT, or DRUNKARD')
    parser.add_argument('--learning_rate', type = float, default = 0.1, help = 'How quickly the agent learns')
    parser.add_argument('--discount', type = float, default = 0.95, help = 'Specify the discount for estimated future action')
    parser.add_argument('--iterations', type = int, default = 2000, help = 'The number of iterations to train')

    FLAGS, unparsed = parser.parse_known_args()

    if FLAGS.agent == 'GAMBLER':
        agent = Gambler(learning_rate = FLAGS.learning_rate, 
                        discount = FLAGS.discount,
                        iterations = FLAGS.interations)
        
        dungeon = Dungeon()
        dungeon.reset()
        total_reward = 0

        for step in range(FLAGS.iterations):
            old_position = dungeon.current_position
            action = agent.get_next_action(old_state)
            new_position, reward = dungeon.take_action(action)
            agent.update(old_state, new_state, action, reward)
        
        total_reward += reward

        print_progress(step)


    print('Final Q-table', agent.q_table)

    def print_progress(step):
        print(json.dumps({'step': step,
                          'total_reward': total_reward}))

        time.sleep(0.001) # Avoid spamming stdout

    # ?? Whatzdiz? 
    if __name__ == "__main__":
        main() 
