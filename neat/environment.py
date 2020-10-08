import gym


class Environment:


    def __init__(self):
        self.read_config()
        self.env = gym.make(self.name)
        self.env.reset()

    def evaluate(self, network):

        for step in range(self.time):
            obs, reward, done, info = self.env.step(self.env.action_space.sample())

    def read_config(self):
        self.name = 'BipedalWalker-v3'
        self.time = 1000
