import random
import json
import argparse
import time
from deep_gambler import DeepGambler
from drunkard import Drunkard
from dungeon import Dungeon
from gambler import Gambler
from accountant import Accountant

def print_progress(step, total_reward):
    performance = (total_reward - last_total) / 250.0
    print(json.dumps({'step': step,
                      'total_reward': total_reward,
                      'performance': performance}))
    last_total = total_reward
    time.sleep(0.001) # Avoid spamming stdout

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--agent', type = str, default = 'DEEP_GAMBLER', help = 'Pick an agent to use. Pick from GAMBLER, ACCOUNTANT, or DRUNKARD')
    parser.add_argument('--learning_rate', type = float, default = 0.1, help = 'How quickly the agent learns')
    parser.add_argument('--discount', type = float, default = 0.95, help = 'Specify the discount for estimated future action')
    parser.add_argument('--iterations', type = int, default = 2000, help = 'The number of iterations to train')

    FLAGS, unparsed = parser.parse_known_args()

    if FLAGS.agent == 'GAMBLER':
        print('::Gambler::')
        agent = Gambler(learning_rate = FLAGS.learning_rate, 
                        discount = FLAGS.discount,
                        iterations = FLAGS.iterations)
    elif FLAGS.agent == 'ACCOUNTANT':
        print('::Accountant::')
        agent = Accountant()
    elif FLAGS.agent == 'DRUNKARD':
        print('::Drunkard::')
        agent = Drunkard()
    else:
        print ('::DEEP GAMBLER::')
        agent = DeepGambler(learning_rate = FLAGS.learning_rate, 
                            discount = FLAGS.discount, 
                            iterations = FLAGS.iterations)

    dungeon = Dungeon()
    dungeon.reset()
    total_reward = 0
    last_total = 0

    for step in range(FLAGS.iterations):
        old_position = dungeon.current_position
        action = agent.get_next_action(old_position)
        new_position, reward = dungeon.take_action(action)
        agent.update(old_position, new_position, action, reward)
        
        total_reward += reward

        #  print_progress(step, total_reward, last_total)
        if step % 250 == 0: 
            performance = (total_reward - last_total) / 250.0
            print(json.dumps({'step': step,
                              'total_reward': total_reward,
                              'performance': performance}))
            last_total = total_reward
        time.sleep(0.001) # Avoid spamming stdout


    # print('Final Q-table', agent.q_table)

# Python2 interpreter will set __name__ to have value of '__main__' causing the if statement to evaluate to True
#if __name__ == "__main__":
#    main()

# Since we are running python3, we only need to call main()
main()
