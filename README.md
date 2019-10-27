## Description
Q-learning example by Valohai titled "Reinforcement Learning Tutorial Cloud Q-Learning"


## Notes
Q-table is a 2 by 5 array with index 0 signifying the reward for the agent moving forward, and index 1 signifying the reward for the agent moving backwards.

```
[0, 0, 0, 42, 0]  FORWARD
[0, 10, 0, 0, 0]  BACKWARD
```

## Execution
python3 train.py --agent=<agent>, where <agent> can be ACCOUNTANT, GAMBLER, DRUNKARD. Otherwise runs the DEEP_GAMBLER agent.

E.g.
```
python3 train.py --agent=DRUNKARD
```
