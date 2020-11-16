from random import choice
from random import shuffle
import numpy as np
from matplotlib import pyplot as plt

class LogicalXor:
    """XOR environment for verification/testing algorithm. """

    def __init__(self):
        self.limit = 20000
        self.evals = 0
        self.solution_networks = []
        self.solution_genomes = []
        self.fails = 0
        self.evals_until_solved = []

    def evaluate(self, genome):
        self.evals += 1

        if self.evals > self.limit:
            self.fails += 1
            self.evals = 0
            return 0, True

        # All possible inputs for XOR in random order.
        examples = [(0, 0, 0),(1, 0, 1),(0, 1, 1),(1, 1, 0)]
        shuffle(examples)

        total_diff = 0
        correct_answers = 0

        network = genome.network()

        for example in examples:
            a, b, expected = example

            output = network.activate([a, b], stabilize=True)[0]

            if round(output) == expected:
                correct_answers += 1

            total_diff += abs(expected - output)

            network.reset()


        # Make fitness higher for better networks.
        fitness = (4 - total_diff) ** 2

        if correct_answers == 4:

            print(f"Solved XOR at evaluation {self.evals}")

            self.solution_networks.append(network)
            self.solution_genomes.append(genome)
            self.evals_until_solved.append(self.evals)
            self.evals = 0

            return fitness, True

        return fitness, False

    def mean(self, data):
        total = 0
        for value in data:
            total += value
        return total/len(data)

    def population_std(self, data):
        mean = self.mean(data)
        total = 0
        for value in data:
            total += (value - mean) ** 2
        return (total/len(data))**0.5

    def stats(self):

        nodes = [len(network.nodes)-4 for network in self.solution_networks]
        links = [len(network.links) for network in self.solution_networks]

        mean_nodes = self.mean(nodes)
        std_nodes = self.population_std(nodes)

        print(f"Mean number of hidden nodes: {mean_nodes}")
        print(f"Std for hidden nodes: {std_nodes}")

        mean_links = self.mean(links)
        std_links = self.population_std(links)

        print(f"Mean number of links: {mean_links}")
        print(f"Std for links: {std_links}")

        mean_evals = self.mean(self.evals_until_solved)
        std_evals = self.population_std(self.evals_until_solved)

        print(f"Mean number of evaluations until solved: {mean_evals}")
        print(f"Std for evaluations: {std_evals}")

        print(f"Number of failures: {self.fails}")
        print(f"Worst performance: {max([x for x in self.evals_until_solved])}")

        print(f"Number of optimal solutions: {len([x for x in self.solution_networks if len(x.nodes) == 5])}")

        self.histogram(self.evals_until_solved)

        for network in self.solution_networks:
            if len(network.nodes) == 5:
                network.draw()

    def histogram(self, data):

        bins = np.arange(0, 20000, 1000) # fixed bin size
        plt.xlim([0, 20000])

        plt.hist(data, bins=bins, alpha=0.8, edgecolor='black', linewidth=1.2)
        plt.title('XOR experiment')
        plt.xlabel('networks evaluated')
        plt.ylabel('runs')

        plt.show()
