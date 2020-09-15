from neat.genome import Genome
from neat.enums.node_types import NodeType
import pytest

@pytest.fixture(name='genome')
def initialised_genome():
    """Fully connected, no hidden layers. """
    num_inputs = 10
    num_outputs = 10
    genome_id = 1
    genome = Genome(genome_id, num_inputs, num_outputs)
    return genome

@pytest.fixture
def loopable_genome(genome):
    """Unrealistic genome in which each node is loopable. """
    for node in genome.nodes:
        node.node_type = NodeType.HIDDEN
    return genome

@pytest.fixture
def unconnectable_genome(genome):
    """Unrealistic genome in which no node is loopable. """
    for node in genome.nodes:
        node.node_type = NodeType.BIAS
    return genome

@pytest.fixture
def connectable_genome(genome):
    for node in genome.nodes:
        node.node_type = NodeType.HIDDEN
    return genome


def test_node_initialisation(genome):
    inputs = genome.num_inputs
    outputs = genome.num_outputs
    assert len(genome.nodes) == inputs + outputs, "correct number of nodes"
    assert [x.id for x in genome.nodes] == [x for x in range(inputs + outputs)], "correct node innovation ids"
    assert [x.node_type for x in genome.nodes[:inputs]] == [NodeType.INPUT for x in range(inputs)], "correct type for inputs"
    assert [x.node_type for x in genome.nodes[inputs:]] == [NodeType.OUTPUT for x in range(outputs)], "correct type for outputs"


def test_link_initialisation(genome):
    inputs = genome.num_inputs
    outputs = genome.num_outputs
    assert len(genome.links) == inputs * outputs, "correct number of links"

    ids = [x.innovation_id for x in genome.links]
    expected_ids = [x for x in range(inputs + outputs, inputs * outputs + inputs + outputs)]
    assert ids == expected_ids, "correct link innovation ids"

    assert True not in [x.recurrent for x in genome.links], "no initial link is recurrent"
    assert False not in [x.enabled for x in genome.links], "all initial links are enabled"


def test_possible_loop(loopable_genome):
    original_number_of_links = len(loopable_genome.links)
    loop_gene = loopable_genome.add_loop(tries=1)

    assert len(loopable_genome.links) == original_number_of_links + 1, "one link gene has been added"
    assert loop_gene.from_node.recurrent == True, "the node has been marked as recurrent"
    assert loop_gene.recurrent == True, "the link has been marked as recurrent"
    assert loop_gene.from_node == loop_gene.to_node, "link is a loop"

def test_impossible_loop(unconnectable_genome):
    original_number_of_links = len(unconnectable_genome.links)
    result = unconnectable_genome.add_loop(tries=10)
    new_number_of_links = len(unconnectable_genome.links)
    assert result is None, "no link gene is returned"
    assert original_number_of_links == new_number_of_links, "no link gene has been added"

def test_add_non_recurrent_link(connectable_genome):
    original_number_of_links = len(connectable_genome.links)
    tries = 50 # Ensure that it won't fail due to picking the same node.
    new_gene = connectable_genome.add_non_recurrent_link(tries)
    new_number_of_links = len(connectable_genome.links)

    assert new_gene, "new gene is not None"
    assert new_number_of_links == original_number_of_links + 1, "one new link added"
    assert new_gene.from_node != new_gene.to_node, "from and to nodes are not the same"

def test_impossible_add_non_recurrent(unconnectable_genome):
    original_number_of_links = len(unconnectable_genome.links)
    result = unconnectable_genome.add_non_recurrent_link(tries=10)
    new_number_of_links = len(unconnectable_genome.links)
    assert result is None, "no link gene is returned"
    assert original_number_of_links == new_number_of_links, "no link gene has been added"