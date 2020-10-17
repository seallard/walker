from neat.genome import Genome
from neat.enums.node_types import NodeType
import pytest
from unittest.mock import Mock


def test_node_initialisation(genome):
    inputs = genome.config.num_inputs
    outputs = genome.config.num_outputs
    assert len(genome.nodes) == inputs + outputs, "correct number of nodes"

    node_numbers = [x.id for x in genome.nodes]
    assert node_numbers == [x for x in range(inputs + outputs)], "correct node innovation ids"

    node_input_types = [x.type for x in genome.nodes[:inputs]]
    assert node_input_types == inputs*[NodeType.INPUT], "correct type for inputs"

    node_output_types = [x.type for x in genome.nodes[inputs:]]
    assert node_output_types == outputs*[NodeType.OUTPUT], "correct type for outputs"


def test_add_single_node(standard_config, tracker):
    genome = Genome(id=1, config=standard_config, tracker=tracker)
    original_number_of_nodes = len(genome.nodes)
    original_number_of_links = len(genome.links)
    genome.mutate_add_node()
    new_node = genome.nodes[-1]
    new_in = genome.links[-2]
    new_out = genome.links[-1]

    assert len(genome.nodes) == original_number_of_nodes + 1, "one node added"
    assert len(genome.links) == original_number_of_links + 2, "two links added"
    disabled_links = [link for link in genome.links if not link.enabled]
    assert len(disabled_links) == 1, "one link disabled"
    assert disabled_links[0].from_node == genome.nodes[0], "correct from node for disabled link"
    assert disabled_links[0].to_node == genome.nodes[1], "correct to node for disabled link"
    assert new_in.to_node == new_node, "new link into new node"
    assert new_out.from_node == new_node, "new link out of new node"
    assert new_in.weight == 1, "weight of new in link is 1"
    assert new_node.depth == 0.5, "depth of new single hidden node is 0.5"


def test_add_multiple_nodes(standard_config, tracker):
    genome = Genome(id=1, config=standard_config, tracker=tracker)
    genome.mutate_add_node()
    genome.mutate_add_node() # Avoid disabled link

    assert len(genome.nodes) == 4, "two nodes added"
    assert len(genome.links) == 5, "four new links added"

    disabled_links = [link for link in genome.links if not link.enabled]
    assert len(disabled_links) == 2, "two links disabled"
    assert not genome.links[0].enabled, "original link disabled"

    recurrent_links = [link for link in genome.links if link.recurrent]
    assert len(recurrent_links) == 0, "no link is marked as recurrent"


def test_impossible_add_node(standard_config):
    genome = Genome(id=1, config=standard_config)
    genome.links[0].enabled = False # Disable the only existing link
    genome.mutate_add_node()

    assert len(genome.nodes) == 2, "no new node added"
    assert len(genome.links) == 1, "no new link added"


def test_copy_node(genome):
    original = genome.nodes[0]
    copy = original.copy()

    assert copy is not original, "copy is not the same object"
    assert copy.id == original.id
    assert copy.type == original.type
    assert copy.depth == original.depth
