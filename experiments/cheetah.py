import gym
import numpy as np
from sklearn.preprocessing import normalize
from neat.genetic_algorithm import GeneticAlgorithm


class Environment:

    def __init__(self):
        self.env = gym.make('HalfCheetah-v2')
        self.evals = 0

    def evaluate(self, genome):

        total_reward = 0
        done = False
        observation = self.env.reset()
        observation = normalize(observation[:,np.newaxis], axis=0).ravel()
        print(observation)

        network = genome.network()


        for i in range(10000):
            action = network.activate(observation, stabilize=False)
            observation, reward, done, info = self.env.step(action=np.array(action))
            observation = normalize(observation[:,np.newaxis], axis=0).ravel() # Normalise.
            print(observation)
            total_reward += reward

        print(f"Total reward {total_reward}")
        self.evals += 1
        return total_reward, False


ga = GeneticAlgorithm(config_filename = "configs/cheetah.json", environment=Environment())
ga.run()
