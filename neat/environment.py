import gym
import numpy as np


class Environment:


    def __init__(self):
        self.read_config()
        self.env = gym.make(self.name)
        self.evaluations = 0

    def evaluate(self, network):

        total_reward = 0
        observation = self.env.reset()

        for step in range(self.time):
            if self.evaluations > 500:
                self.env.render()
            action = network.activate(observation, stabilize=False)
            observation, reward, done, info = self.env.step(action=np.array(action))
            total_reward += reward

        self.evaluations += 1

        print(f"Total reward {total_reward}")
        return total_reward

    def read_config(self):
        self.name = 'BipedalWalker-v3'
        self.time = 300
