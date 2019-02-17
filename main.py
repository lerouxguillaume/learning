# q learning with table
import numpy as np
import matplotlib.pyplot as plt
import time
from game import Game
from trainer import Trainer
from IPython.core.debugger import set_trace

def train(episodes, trainer, wrong_action_p, alea, collecting=False, snapshot=5000):
    batch_size = 32
    g = Game(4, 4, wrong_action_p, alea=alea)
    counter = 1
    scores = []
    global_counter = 0
    losses = [0]
    epsilons = []

    # we start with a sequence to collect information, without learning
    if collecting:
        collecting_steps = 10000
        print("Collecting game without learning")
        steps = 0
        while steps < collecting_steps:
            state = g.reset()
            done = False
            while not done:
                steps += 1
                action = g.get_random_action()
                next_state, reward, done, _ = g.move(action)
                trainer.remember(state, action, reward, next_state, done)
                state = next_state

    print("Starting training")
    global_counter = 0
    for e in range(episodes+1):
        state = g.generate_game()
        state = np.reshape(state, [1, 64])
        score = 0
        done = False
        steps = 0
        while not done:
            steps += 1
            global_counter += 1
            action = trainer.get_best_action(state)
            trainer.decay_epsilon()
            next_state, reward, done, _ = g.move(action)
            next_state = np.reshape(next_state, [1, 64])
            score += reward
            trainer.remember(state, action, reward, next_state, done)
            state = next_state
            if global_counter % 100 == 0:
                l = trainer.replay(batch_size)
                losses.append(l.history['loss'][0])
            if done:
                scores.append(score)
                epsilons.append(trainer.epsilon)
            if steps > 200:
                break
        if e % 200 == 0:
            print("episode: {}/{}, moves: {}, score: {}, epsilon: {}, loss: {}"
                  .format(e, episodes, steps, score, trainer.epsilon, losses[-1]))
        if e > 0 and e % snapshot == 0:
            trainer.save(id='iteration-%s' % e)
    return scores, losses, epsilons

trainer = Trainer('OSS', learning_rate=0.001, epsilon_decay=0.999995)
scores, losses, epsilons = train(100000, trainer, 0.05, True, snapshot=2500)
trainer.save()

def smooth(vector, width=30):
    return np.convolve(vector, [1/width]*width, mode='valid')

sc = smooth(scores, width=500)
fig, ax1 = plt.subplots()
ax1.plot(sc)
ax2 = ax1.twinx()
ax2.plot(epsilons, color='r')
ax1.set_ylabel('Score')
ax2.set_ylabel('Epsilon', color='r')
ax2.tick_params('y', colors='r')
plt.title("Score, and Epsilon over training")
ax1.set_xlabel("Episodes")
plt.figure()
plt.show()
