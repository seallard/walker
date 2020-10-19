from random import choice


class xor:
    """xor environment for verification/testing of algorithm. """

    def evaluate(self, network):

        examples = self.generate_examples(4)

        total_diff = 0
        for example in examples:
            a, b, expected = example
            output = network.update([a, b])[0]

            if output >= 0.5:
                output = 1.0
            else:
                output = 0

            total_diff += abs(expected - output)

        # Make fitness higher for better networks.
        fitness = 4 - total_diff
        print(fitness)
        return fitness

    def generate_examples(self, number):
        examples = [(0, 0, 0),(1, 0, 1),(0, 1, 1),(1, 1, 0)]
        return examples

        examples = []

        for i in range(number):
            a = choice([0,1])
            b = choice([0,1])
            example = (a, b, a^b)
            examples.append(example)

        return examples
