import numpy as np
import matplotlib.pyplot as plt
import time
from IPython import display
from game import Game
from trainer import Trainer

g = Game(4, 4, 0.1, alea=True)
trainer = Trainer('OSS', learning_rate=0.001, epsilon_decay=0.999995)
state = g.reset()
state = g._get_state()
print("state")
print("  ")
g.print()
done = False
time.sleep(2)
while not done:
    time.sleep(1)
    display.clear_output(wait=True)
    print(trainer.model.predict(np.array(g._get_state())))
    action = trainer.get_best_action(g._get_state(), rand=False)
    print(Game.ACTION_NAMES[action])
    next_state, reward, done, _ = g.move(action)
    g.print()
print(reward)


