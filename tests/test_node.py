from neat.genome import Genome
from neat.enums.node_types import NodeType
import pytest


def test_node_initialisation(genome):
    inputs = genome.num_inputs
    outputs = genome.num_outputs
    assert len(genome.nodes) == inputs + outputs, "correct number of nodes"
    assert [x.innovation_number for x in genome.nodes] == [x for x in range(inputs + outputs)], "correct node innovation ids"
    assert [x.node_type for x in genome.nodes[:inputs]] == [NodeType.INPUT for x in range(inputs)], "correct type for inputs"
    assert [x.node_type for x in genome.nodes[inputs:]] == [NodeType.OUTPUT for x in range(outputs)], "correct type for outputs"


def test_add_single_node():
    genome = Genome(id=1, num_inputs=1, num_outputs=1)
    original_number_of_nodes = len(genome.nodes)
    original_number_of_links = len(genome.links)
    innovations = genome.mutate_add_node(tries=1)
    new_node = innovations[0].gene
    new_in = innovations[1].gene
    new_out = innovations[2].gene

    assert len(genome.nodes) == original_number_of_nodes + 1, "one node added"
    assert len(genome.links) == original_number_of_links + 2, "two links added"
    assert False in [x.enabled for x in genome.links], "one link disabled"
    assert new_in.to_node == new_node, "new link into new node"
    assert new_out.from_node == new_node, "new link out of new node"
    assert new_in.weight == 1, "weight of new in link is 1"
    assert new_node.depth == 0.5, "depth of new single hidden node is 0.5"


def test_add_multiple_nodes():
    pass
