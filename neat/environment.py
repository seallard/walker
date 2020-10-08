import gym


class Environment:


    def __init__(self):
        self.read_config()
        self.env = gym.make(self.name)
        self.env.reset()

    def evaluate(self, network):

        for step in self.time:
            obs, reward, done, info = self.env.step(env.action_space.sample())

    def read_config(self):
        self.name = 'BipedalWalker-v3'
        self.time = 1000
