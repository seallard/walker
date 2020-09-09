
class Genome:

    def __init__(self, id, nodes, connections):
        self.id = id
        self.nodes = nodes
        self.connections = connections
        self.raw_fitness = 0
        self.adjusted_fitness = 0
        self.number_of_offspring = 0

    def mutate_add_connection(self):
        """Random addition of a connection between two previously unconnected nodes. """
        pass

    def mutate_add_node(self):
        """Random insertion of a node between two previously connected nodes. """
        pass

    def mutate_weights(self):
        """Perturb or replace weights. """
        pass

    def compatibility_score(self, other):
        """Calculate compatibility score with other genome. """
        pass

    def crossover(self, other):
        """Create a child genome. """
        pass

    def duplicate_connection(self, from_node_id, to_node_id):
        """Check if connection is present in the genome. """
        pass

    def duplicate_node(self, node_id):
        """Check if node is present in the genome. """
        pass

    def get_index_of_node(self, node_id):
        """Find index of node in the list of nodes. """
        pass

