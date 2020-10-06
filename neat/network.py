

class Network:

    def __init__(self):
        pass

    def update(self, inputs):
        """Propagate signals one node forward in the network. """

        # Initialise input nodes with inputs.
        for i, node in enumerate(self.nodes[:self.num_inputs]):
            node.output = inputs[i]

        outputs = []

        for node in self.nodes[self.num_inputs:]:
            node.activate()

            if node.is_output():
                outputs.append(node.output)

        return outputs

    def draw(self):
        pass
