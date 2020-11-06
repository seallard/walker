import gym
import numpy as np
from neat.genetic_algorithm import GeneticAlgorithm


class Environment:


    def __init__(self):
        self.env = gym.make('CartPole-v0')
        self.evals = 0

    def evaluate(self, genome):

        total_reward = 0
        done = False
        observation = self.env.reset()

        network = genome.network()


        while not done:

            if self.evals > 3000:
                self.env.render()
            action = network.activate(observation, stabilize=False)
            observation, reward, done, info = self.env.step(action=round(action[0]))
            total_reward += reward

        print(f"Total reward {total_reward}")
        self.evals += 1
        return total_reward, False


ga = GeneticAlgorithm(config_filename = "configs/pole_config.json", environment=Environment())
ga.run()
