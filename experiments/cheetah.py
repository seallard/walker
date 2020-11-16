import gym
import numpy as np
from sklearn.preprocessing import normalize
from neat.genetic_algorithm import GeneticAlgorithm


class Environment:

    def __init__(self):
        self.evals = 0
        self.env = gym.make('Walker2d-v3')

    def evaluate(self, genome):

        raw_observation = self.env.reset()
        observation = normalize(raw_observation[:,np.newaxis], axis=0).ravel()

        network = genome.network()
        total_reward = 0

        for i in range(2000):

            self.env.render()

            action = network.activate(observation, stabilize=False)

            raw_observation, reward, done, info = self.env.step(action=np.array(action))
            observation = normalize(raw_observation[:,np.newaxis], axis=0).ravel()

            total_reward += reward

        self.evals += 1
        print(self.evals)

        return total_reward, False

    def fitness(self, final_observation):
        print(final_observation[0])
        return final_observation[0] # Distance traveled.


ga = GeneticAlgorithm(config_filename = "configs/cheetah.json", environment=Environment())
ga.run()
