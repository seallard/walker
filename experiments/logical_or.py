from random import choice
from random import shuffle


class LogicalOr:

    def __init__(self):
        self.evals = 0

    def evaluate(self, genome):

        self.evals += 1

        # All possible inputs for XOR in random order.
        examples = [(0, 0, 0),(1, 0, 1),(0, 1, 1),(1, 1, 1)]
        shuffle(examples)

        total_diff = 0
        correct_answers = 0

        for example in examples:
            network = genome.network()
            a, b, expected = example
            output = network.activate([a, b])[0]

            if round(output) == expected:
                correct_answers += 1

            total_diff += abs(expected - output)

        if correct_answers == 4:
            print(f"Evaluation {self.evals}")
            print("Solved OR")
            print("Trying again...")

            examples = [(0, 0, 0),(1, 0, 1),(0, 1, 1),(1, 1, 1)]
            shuffle(examples)

            total_diff = 0
            correct_answers = 0

            for example in examples:
                network = genome.network()
                a, b, expected = example
                output = network.activate([a, b])[0]

                if round(output) == expected:
                    correct_answers += 1

                total_diff += abs(expected - output)

            if correct_answers == 4:
                print("Oops I did it again!")

            network.draw()

        # Make fitness higher for better networks.
        fitness = (4 - total_diff) ** 2

        return fitness
